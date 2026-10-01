"""HeatMap Node sizing calculations, HMN-CAL-001 v0.4 (TRL 3, HMN-DDR-002 and the design for construction HMN-DDR-003 applied).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md. Each line carries a tag such as
[A3] that the note cites. Geometry comes from cad/src/model.py (PARAMS, derived and the part
solids), the parts cost from bom/bom.csv and the budget from project.yaml. FieldNode figures
are quoted from FND-CAL-001 v0.4 in the FieldNode repo (hot-climate node with its sun shield, Rev P3). First-principles estimates for a
paper proof of concept; not a substitute for tests.
"""
import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "cad" / "src"))
from model import PARAMS as P, derived, build_parts  # noqa: E402

D = derived(P)
SIGMA = 5.67e-8


def tag(t, text):
    print(f"[{t}] {text}")


# ------------------------------------------------------------------ assumptions
EPS_G = 0.95            # globe emissivity (matte black paint)
DG = P["globe_d"] / 1000
RHO, CP = 1.18, 1005.0  # air near 35 degC
NU_AIR, K_AIR, PR = 1.65e-5, 0.0268, 0.71
LE = 0.85               # Lewis number, water vapour in air
LV = 2.42e6             # J/kg latent heat near 30 degC
P_ATM = 101325.0
WICK_D = 0.007          # m, notional natural wet-bulb wick used by the model (assumed)
EPS_W = 0.95
V_START = 0.8           # m/s anemometer start-up (typical low-cost class; unverified)
FN_ALLOW_W = 0.100      # W FieldNode design sensor allowance (FND-CAL-001 [A5]); 0.115 W published
FN_MASS = 2.61          # kg FieldNode hot-climate node with the sun shield (FND-CAL-001 v0.4 [F1b], after FND-DDR-003)
FN_COST = 148.00        # USD FieldNode base $139.00 plus the $9.00 sun shield, BOM line 14 (FND-CAL-001 v0.4, after FND-DDR-003)
FN_WIND_N = 52.2 + 36.3  # N panel plus shielded enclosure at 35 m/s (FND-CAL-001 v0.2 [D1], [D3b])
FN_RISE_SHIELD = 52.2 - 45.0   # K interior over ambient, dusty, worst sun position, with the shield (FND-CAL-001 v0.2, R2)
FN_RISE_BARE = 73.3 - 45.0     # K the same without the shield (FND-CAL-001 v0.1)
FN_REC_B = 32           # bytes per stored reading on FieldNode (FND-CAL-001 assumptions)
FN_AIRTIME_SF9 = 23.7   # s/day for a 20 B uplink every 15 min at SF9 (FND-CAL-001 [B1])
LOSS = 0.0102           # TwinKit uplink loss at SF9, 50 nodes at 5 min (TWK-CAL-001, worst case)
CALRIG_U = (0.14, 0.24)  # degC expanded reference uncertainty (CLR-CAL-001 [F1]), typical and max tolerance


def esat(t):
    """Saturation vapour pressure over water, Pa (Magnus form, Alduchov and Eskridge coefficients)."""
    return 610.94 * math.exp(17.625 * t / (t + 243.04))


def h_globe(tg, ta, v, d=DG):
    """ISO 7726 approach: larger of the forced and natural convection coefficients, W/m2K."""
    hf = 6.3 * v ** 0.6 / d ** 0.4
    hn = 1.4 * (abs(tg - ta) / d) ** 0.25
    return max(hf, hn), hf, hn


def mrt(tg, ta, v, d=DG, eps=EPS_G):
    h = h_globe(tg, ta, v, d)[0]
    x = (tg + 273.15) ** 4 + h / (eps * SIGMA) * (tg - ta)
    return x ** 0.25 - 273.15


def tg_from_mrt(tmrt, ta, v, d=DG, eps=EPS_G):
    lo, hi = ta - 20, tmrt + 20
    for _ in range(80):
        mid = (lo + hi) / 2
        if mrt(mid, ta, v, d, eps) < tmrt:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def h_wick(v):
    """Cylinder in cross flow (Hilpert, Re 40 to 4000): Nu = 0.683 Re^0.466 Pr^(1/3)."""
    re = max(v, 0.1) * WICK_D / NU_AIR
    return 0.683 * re ** 0.466 * PR ** (1 / 3) * K_AIR / WICK_D


def tnwb(ta, rh, tmrt, v):
    """Natural wet-bulb temperature from a wick energy balance: convection plus radiation from the
    environment seen by the globe equals evaporation (Chilton-Colburn analogy). Simplified stand-in
    for the Liljegren model, which the data server will use."""
    ea = rh / 100 * esat(ta)
    h = h_wick(v)
    k = h / (CP * LE ** (2 / 3)) * 0.622 * LV / P_ATM

    def f(tw):
        rad = EPS_W * SIGMA * ((tmrt + 273.15) ** 4 - (tw + 273.15) ** 4)
        return h * (ta - tw) + rad - k * (esat(tw) - ea)
    lo, hi = -10.0, ta + 30
    for _ in range(80):
        mid = (lo + hi) / 2
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def wbgt(ta, rh, tg, v):
    tm = mrt(tg, ta, v)
    tw = tnwb(ta, rh, tm, v)
    return 0.7 * tw + 0.2 * tg + 0.1 * ta, tw, tm


print("HeatMap Node sizing, HMN-CAL-001 v0.4")
print(f"Geometry from cad/src/model.py: arm at {P['arm_z']:.0f} mm, globe {P['globe_d']:.0f} mm, "
      f"shield {P['n_plates']} x {P['shield_d']:.0f} mm plates, pole {P['pole_od']} mm")

# ------------------------------------------------------------------ A. Mean radiant temperature (R3, R4, R5)
print("\nA. Mean radiant temperature from the globe")
TA, RH, TG, V = 35.0, 40.0, 50.0, 1.0
h, hf, hn = h_globe(TG, TA, V)
tm0 = mrt(TG, TA, V)
tag("A1", f"worked example Ta {TA:.0f} C, {RH:.0f} %RH, Tg {TG:.0f} C, {V:.1f} m/s: h forced {hf:.1f}, natural {hn:.1f} W/m2K; "
          f"forced coefficient 6.3/sigma = {6.3 / SIGMA:.3g}; MRT {tm0:.1f} C")
tag("A2", f"MRT with wind 0.5 / 1.5 / 3.0 m/s instead of 1.0: {mrt(TG, TA, 0.5):.1f} / {mrt(TG, TA, 1.5):.1f} / {mrt(TG, TA, 3.0):.1f} C")
tag("A3", f"MRT sensitivity at the example: Ta +1 C -> {mrt(TG, TA + 1, V) - tm0:+.2f} C; Tg +0.3 C -> {mrt(TG + 0.3, TA, V) - tm0:+.2f} C; "
          f"wind +0.5 m/s -> {mrt(TG, TA, 1.5) - tm0:+.1f} C")
v_cross = (1.4 * (abs(TG - TA) / DG) ** 0.25 * DG ** 0.4 / 6.3) ** (1 / 0.6)
tag("A4", f"natural convection governs below {v_cross:.2f} m/s at a 15 K globe excess")
tm_true = mrt(TG, TA, 0.5)
tm_zero = mrt(TG, TA, 0.0)
tag("A5", f"true wind 0.5 m/s, anemometer below its {V_START} m/s start-up reads 0: MRT {tm_zero:.1f} C instead of {tm_true:.1f} C "
          f"({tm_zero - tm_true:+.1f} C)")

# ------------------------------------------------------------------ B. Natural wet bulb and WBGT (R5)
print("\nB. Natural wet-bulb and WBGT")
tw_psy = tnwb(TA, RH, TA, V)
w0, tw0, _ = wbgt(TA, RH, TG, V)
tag("B1", f"psychrometric check (no radiant excess, MRT = Ta): wet bulb {tw_psy:.1f} C")
tag("B2", f"worked example: natural wet bulb {tw0:.1f} C; WBGT = 0.7 x {tw0:.1f} + 0.2 x {TG:.0f} + 0.1 x {TA:.0f} = {w0:.1f} C")
U_IN = {"Ta": 0.1, "RH": 1.0, "Tg": 0.3, "v": 0.5}   # sensor, SHT45 typical; R3; R4 at 1 m/s
steps = {"Ta": (1, 0, 0, 0), "RH": (0, 1, 0, 0), "Tg": (0, 0, 1, 0), "v": (0, 0, 0, 1)}
sens = {}
for k_, (a, b_, c, d) in steps.items():
    dx = 0.1 if k_ != "v" else 0.05
    sens[k_] = (wbgt(TA + a * dx, RH + b_ * dx, TG + c * dx, V + d * dx)[0] - w0) / dx
tag("B3", "WBGT sensitivity per unit input: " + ", ".join(f"{k_} {s:+.3f}" for k_, s in sens.items()))


def budget(shield_bias):
    u = dict(U_IN)
    u["Ta"] = math.hypot(U_IN["Ta"], shield_bias)
    terms = {k_: abs(sens[k_]) * u[k_] for k_ in u}
    return terms, math.sqrt(sum(t * t for t in terms.values())), sum(terms.values())


# shield bias from section C is needed; computed below and the budget printed there

# ------------------------------------------------------------------ C. Shield radiation error (R1)
print("\nC. Radiation error of the shield, passive and fan-aspirated")
ALPHA_P = 0.25          # solar absorptance of aged white ASA plates (assumed)
G = 1000.0              # W/m2 global irradiance on a horizontal surface, clear midday
ELEV = 60.0             # deg sun elevation
ALB = 0.15              # pavement albedo
ETA = 0.5               # share of absorbed heat that reaches the air passing the sensor (assumed)
K_VENT = 0.25           # air speed inside the stack as a share of the wind speed (assumed)
sr, hr = P["shield_d"] / 2000, P["plate_hole"] / 2000
stack = D["stack_h"] / 1000
a_top = math.pi * sr ** 2 * math.sin(math.radians(ELEV))
a_side = 2 * sr * stack * math.cos(math.radians(ELEV))
a_under = math.pi * (sr ** 2 - hr ** 2)
q_abs = ALPHA_P * (G / math.sin(math.radians(ELEV)) * 0.85 * (a_top + a_side) + ALB * G * a_under)
a_flow = 2 * hr * stack
tag("C1", f"sunlit areas: top {a_top * 1e4:.0f} cm2, side {a_side * 1e4:.0f} cm2, underside {a_under * 1e4:.0f} cm2; absorbed {q_abs:.2f} W; "
          f"through-flow area {a_flow * 1e4:.0f} cm2")


def shield_err(v, k=K_VENT):
    m = RHO * a_flow * k * v
    return ETA * q_abs / (m * CP)


errs = {v: shield_err(v) for v in (0.5, 1.0, 2.0, 3.0)}
tag("C2", "passive (fan off) air temperature error in full sun: " + ", ".join(f"{e:.2f} C at {v:.1f} m/s" for v, e in errs.items()))
v_05 = ETA * q_abs / (RHO * a_flow * K_VENT * CP * 0.5)
tag("C3", f"error falls to 0.5 C at {v_05:.1f} m/s; with half the assumed ventilation (k = {K_VENT / 2}) the error at 1 m/s is {shield_err(1.0, K_VENT / 2):.2f} C")
# Aspiration fan (HMN-DDR-002): 60 x 60 x 15 mm 5 V class fan drawing air up the center of the stack
FAN_W = 0.90            # W at 5 V (180 mA, typical of the class; assumed)
FAN_FREE = 6.6e-3       # m3/s free-air flow (about 14 CFM, typical of the class; assumed)
FAN_SHARE = 0.60        # share of the free-air flow delivered through the plate stack (assumed)
RAIL_EFF = 0.85         # FieldNode 5 V switched rail efficiency from the cell (assumed)
FAN_ON, T_CYCLE = 6.0, 180.0   # s the fan runs before each air reading; s between readings (firmware rule)
TAU_TH = 2.0            # s time constant of the T and RH sensor with its membrane cap (assumed, to be checked)
q_fan = FAN_FREE * FAN_SHARE
v_col = q_fan / (math.pi * (P["top_hole"] / 2000) ** 2)
e_fan_ss = ETA * q_abs / (RHO * q_fan * CP)
e_fan = e_fan_ss + (errs[1.0] - e_fan_ss) * math.exp(-FAN_ON / TAU_TH)
p_fan = FAN_W / RAIL_EFF * FAN_ON / T_CYCLE
tag("C4", f"fan {FAN_W:.2f} W, {q_fan * 1000:.1f} L/s through the stack ({FAN_SHARE * 100:.0f} % of {FAN_FREE * 1000:.1f} L/s free air), "
          f"{v_col:.1f} m/s up the {P['top_hole']:.0f} mm column: steady error {e_fan_ss:.2f} C; after {FAN_ON:.0f} s from the passive "
          f"1 m/s state (sensor time constant {TAU_TH:.0f} s) {e_fan:.2f} C, independent of wind")
tag("C5", f"fan energy: {FAN_ON:.0f} s every {T_CYCLE:.0f} s ({FAN_ON / T_CYCLE * 100:.1f} % duty), {FAN_W / RAIL_EFF:.2f} W from the cell "
          f"at {RAIL_EFF * 100:.0f} % rail efficiency: {p_fan * 1000:.1f} mW average; {86400 / T_CYCLE:.0f} aspirated air readings a day, "
          f"{900 / T_CYCLE:.0f} per 15 min mean")
FAN_ERR_TARGET = 0.5
q_need = ETA * q_abs / (RHO * CP * (FAN_ERR_TARGET - (errs[1.0] - e_fan_ss) * math.exp(-FAN_ON / TAU_TH)))
tag("C6", f"the {FAN_ERR_TARGET} C target of R1 needs at least {q_need * 1000:.1f} L/s through the stack "
          f"({q_need / FAN_FREE * 100:.0f} % of the assumed free-air flow)")

terms, rss, worst = budget(e_fan)
tag("B4", "WBGT error budget at the example with the fan-aspirated shield: " + ", ".join(f"{k_} {t:.2f}" for k_, t in terms.items())
    + f"; RSS {rss:.2f} C, worst case {worst:.2f} C (model error of the Liljegren method not included)")
terms_p, rss_p, worst_p = budget(errs[1.0])
tag("B5", f"for comparison, passive shield at 1 m/s: RSS {rss_p:.2f} C, worst case {worst_p:.2f} C")
w_zero = wbgt(TA, RH, TG, 0.0)[0]
w_half = wbgt(TA, RH, TG, 0.5)[0]
tag("B6", f"calm air: true wind 0.5 m/s read as 0: WBGT {w_zero:.1f} C instead of {w_half:.1f} C ({w_zero - w_half:+.1f} C)")

# ------------------------------------------------------------------ D. Globe response and probe (R3)
print("\nD. Globe response and probe accuracy")
RHO_CU, C_CU = 8960.0, 385.0
m_shell = math.pi * DG ** 2 * P["globe_wall"] / 1000 * RHO_CU
m_boss = 0.020
cap = (m_shell + m_boss) * C_CU
a_g = math.pi * DG ** 2
tag("D1", f"globe shell {m_shell * 1000:.0f} g copper at {P['globe_wall']} mm plus {m_boss * 1000:.0f} g boss: heat capacity {cap:.0f} J/K; area {a_g:.4f} m2")
for v in (0.3, 1.0, 3.0):
    hc = h_globe(50, 35, v)[0]
    hr_ = 4 * EPS_G * SIGMA * (50 + 273.15) ** 3
    tau = cap / ((hc + hr_) * a_g)
    tag("D2", f"wind {v:.1f} m/s: h conv {hc:.1f} + h rad {hr_:.1f} W/m2K; time constant {tau / 60:.1f} min; 90 % response {2.303 * tau / 60:.1f} min")
BEAD_D, BEAD_RHO, BEAD_C, H_IN = P["bead_d"] / 1000, 1800.0, 1000.0, 12.0   # epoxy bead; natural convection plus radiation inside
bead_cap = math.pi / 6 * BEAD_D ** 3 * BEAD_RHO * BEAD_C
tau_b = bead_cap / (H_IN * math.pi * BEAD_D ** 2)
tau_g1 = cap / ((h_globe(50, 35, 1.0)[0] + 4 * EPS_G * SIGMA * 323.15 ** 3) * a_g)
tag("D5", f"bead {bead_cap:.2f} J/K coupled to the shell at {H_IN:.0f} W/m2K: time constant {tau_b / 60:.1f} min; globe plus bead at 1 m/s "
          f"about {(tau_g1 + tau_b) / 60:.1f} min, 90 % response about {2.303 * (tau_g1 + tau_b) / 60:.0f} min (target 30 min)")
R25, BETA, RFIX, VREF, NBIT = 10e3, 3950.0, 10e3, 3.3, 12
rt = R25 * math.exp(BETA * (1 / 323.15 - 1 / 298.15))
dv_dt = VREF * RFIX / (rt + RFIX) ** 2 * rt * BETA / 323.15 ** 2
lsb = VREF / 2 ** NBIT
q_t = lsb / dv_dt
i_ntc = VREF / (rt + RFIX)
p_ntc = i_ntc ** 2 * rt
tag("D3", f"NTC at 50 C: {rt / 1000:.2f} kOhm; divider slope {dv_dt * 1000:.1f} mV/K; 12-bit step {q_t * 1000:.0f} mK; "
          f"self-heating power {p_ntc * 1000:.2f} mW while switched on (10 ms per reading)")
FIT = 0.05
for u_ref in CALRIG_U:
    u = math.sqrt(u_ref ** 2 + (2 * FIT) ** 2 + (q_t / math.sqrt(3) * 2) ** 2)
    tag("D4", f"probe expanded uncertainty with CalRig reference {u_ref:.2f} C: {u:.2f} C (target 0.3 C)")

# ------------------------------------------------------------------ E. Height and shading (R9, R3)
print("\nE. Measurement height and pole shading")
KAP, GRAV = 0.4, 9.81
Z0 = 0.1                 # m roughness length (assumed, open street)
H_FLUX = 250.0           # W/m2 sensible heat flux from sunlit pavement (assumed)
z_s = D["shield_zc"] / 1000


def psi_h(zeta):
    if zeta >= 0:
        return -5 * zeta
    x = (1 - 16 * zeta) ** 0.25
    return 2 * math.log((1 + x * x) / 2)


def psi_m(zeta):
    if zeta >= 0:
        return -5 * zeta
    x = (1 - 16 * zeta) ** 0.25
    return 2 * math.log((1 + x) / 2) + math.log((1 + x * x) / 2) - 2 * math.atan(x) + math.pi / 2


def profile(u_ref, h=H_FLUX, t=308.15):
    L = -1e9
    for _ in range(60):
        us = KAP * u_ref / (math.log(z_s / Z0) - psi_m(z_s / L))
        L = -us ** 3 * RHO * CP * t / (KAP * GRAV * h)
    th_star = -h / (RHO * CP * us)
    return us, L, th_star


for u_ref in (1.0, 3.0):
    us, L, ths = profile(u_ref)
    out = []
    for z in (1.1, 1.5, 2.0):
        dt = -(ths / KAP) * (math.log(z_s / z) - psi_h(z_s / L) + psi_h(z / L))
        out.append(f"{z:.1f} m {dt:+.2f} C")
    tag("E1", f"wind {u_ref:.0f} m/s at the sensor: u* {us:.2f} m/s, L {L:.1f} m; air at pedestrian height minus air at {z_s:.2f} m: " + ", ".join(out))
dx = P["globe_x"] / 1000
width = 2 * math.degrees(math.atan(D["r"] / 1000 / dx))
tag("E2", f"pole seen from the globe: {width:.1f} deg wide; with the arm pointing east or west the sun would pass behind it for about "
          f"{width / 15:.1f} h a day (15 deg/h mean azimuth rate, assumed); with the arm pointing toward the equator (HMN-DDR-002) "
          f"the pole is on the poleward side, which the sun reaches outside the polar regions only in the tropics, near noon and high in the sky")


def panel_shade(elev, azim, n=24):
    """Share of the FieldNode panel (world axes, facing +X) in the shadow of the shield with its cowl,
    the globe and the arm, for a sun at elevation elev and azimuth azim from +X (deg)."""
    e, a = math.radians(elev), math.radians(azim)
    d = (math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e))
    t = math.radians(P["fn_tilt"])
    w, sl = P["fn_panel"][0], P["fn_panel"][1]
    gc = (P["globe_x"], 0.0, D["globe_zc"]); gr = P["globe_d"] / 2
    sxc, srr, sz0, sz1 = P["shield_x"], P["shield_d"] / 2, D["shield_bot"], D["cowl_top"]
    box_lo = (D["arm_x0"], -P["arm_w"] / 2, D["arm_bot"]); box_hi = (D["arm_x1"], P["arm_w"] / 2, D["arm_top"])
    hit = 0
    for i in range(n):
        for j in range(n):
            s_ = (j + 0.5) / n * sl - sl / 2
            pt = (D["panel_cx_w"] + s_ * math.cos(t), (i + 0.5) / n * w - w / 2, D["panel_cz"] - s_ * math.sin(t))
            oc = [pt[k] - gc[k] for k in range(3)]
            bq = sum(oc[k] * d[k] for k in range(3)); cq = sum(o * o for o in oc) - gr * gr
            if bq * bq - cq > 0 and -bq + math.sqrt(bq * bq - cq) > 0:
                hit += 1; continue
            ox, oy = pt[0] - sxc, pt[1]
            A = d[0] ** 2 + d[1] ** 2; B = 2 * (ox * d[0] + oy * d[1]); C = ox * ox + oy * oy - srr * srr
            disc = B * B - 4 * A * C
            if A > 0 and disc > 0:
                t1, t2 = (-B - math.sqrt(disc)) / (2 * A), (-B + math.sqrt(disc)) / (2 * A)
                z1, z2 = pt[2] + t1 * d[2], pt[2] + t2 * d[2]
                if t2 > 0 and max(min(z1, z2), sz0) <= min(max(z1, z2), sz1):
                    hit += 1; continue
            tmin, tmax = 0.0, 1e9
            for k in range(3):
                if abs(d[k]) < 1e-12:
                    if not box_lo[k] <= pt[k] <= box_hi[k]:
                        tmin, tmax = 1, 0
                else:
                    ta, tb = (box_lo[k] - pt[k]) / d[k], (box_hi[k] - pt[k]) / d[k]
                    tmin, tmax = max(tmin, min(ta, tb)), min(tmax, max(ta, tb))
            if tmin <= tmax:
                hit += 1
    return hit / n / n


shade = {(el, az_): panel_shade(el, az_) for el in (30, 45, 60, 75) for az_ in (0, 30, 60)}
tag("E3", "share of the FieldNode panel shaded by the shield, cowl, globe and arm, core below the arm, both facing the equator: "
    + "; ".join(f"sun {el} deg high, {az_} deg off the arm azimuth {shade[(el, az_)] * 100:.0f} %" for el, az_ in shade))

# ------------------------------------------------------------------ F. Power (R7)
print("\nF. Sensor power")
e_sht = 3.3 * 0.4e-3 * 8.3e-3          # J per high-repeatability reading (assumed datasheet class)
e_ntc = VREF * i_ntc * 0.010
p_reed = 3.3 / 100e3 * 3.3             # W if the reed rests closed (worst case)
p_idle = 3.3 * 2e-6                    # W sleep of the T and RH sensor and pull-ups (assumed)
n_th = 86400 / T_CYCLE
p_avg = e_sht * n_th / 86400 + e_ntc * 1440 / 86400 + p_reed + p_idle
tag("F1", f"per reading: T/RH {e_sht * 1e6:.1f} uJ ({n_th:.0f} aspirated readings a day), NTC {e_ntc * 1e6:.1f} uJ (1,440 a day); "
          f"reed pull-up worst case {p_reed * 1000:.3f} mW")
tag("F2", f"sensor load without the fan {p_avg * 1000:.3f} mW; with the fan {(p_avg + p_fan) * 1000:.1f} mW, "
          f"{(p_avg + p_fan) / FN_ALLOW_W * 100:.0f} % of the {FN_ALLOW_W * 1000:.0f} mW FieldNode design allowance")

# ------------------------------------------------------------------ G. Data (R6)
print("\nG. Payload, airtime and storage")
FIELDS = [("air temperature mean", 2), ("air temperature max", 2), ("RH mean", 2), ("globe temperature mean", 2),
          ("globe temperature max", 2), ("wind mean", 2), ("wind gust", 2), ("calm share (below start-up)", 1),
          ("battery voltage", 2), ("status flags", 1), ("sequence number", 2)]
nbytes = sum(b_ for _, b_ in FIELDS)
tag("G1", f"payload {nbytes} B: " + ", ".join(f"{n} {b_}" for n, b_ in FIELDS))
store = 96 * 7 * FN_REC_B
tag("G2", f"96 uplinks a day, {FN_AIRTIME_SF9} s/day at SF9 (FND-CAL-001); 7 days stored at {FN_REC_B} B per record = {store / 1000:.1f} kB")
CALM_FLAG = 0.20
tag("G4", f"calm flag rule (HMN-DDR-002): the server marks MRT and WBGT as biased high in calm air for any interval whose calm share "
          f"(time below the {V_START} m/s start-up) is {CALM_FLAG * 100:.0f} % or more, that is {CALM_FLAG * 15:.0f} min of 15")
tag("G3", f"latency: sent at the end of each 15 min mean, at the gateway within about 16 min; share needing the next uplink (loss {LOSS * 100:.2f} %) "
          f"arrives at about 31 min")

# ------------------------------------------------------------------ H. Wind, arm and clamp (R11)
print("\nH. Wind load, arm and clamp")
q35, q20 = 0.5 * 1.225 * 35 ** 2, 0.5 * 1.225 * 20 ** 2
x0 = D["arm_x0"]
cup_r = P["cup_d"] / 2000
elems = [  # name, CdA (m2), x from the pole axis (m), z offset from the arm axis (m)
    ("globe", 0.5 * math.pi * (DG / 2) ** 2, P["globe_x"] / 1000, (D["globe_zc"] - P["arm_z"]) / 1000),
    ("shield", 1.2 * P["shield_d"] / 1000 * stack, P["shield_x"] / 1000, (D["shield_zc"] - P["arm_z"]) / 1000),
    ("anemometer", 1.4 * 2 * math.pi * cup_r ** 2 + 1.2 * P["mast_d"] / 1000 * P["mast_h"] / 1000 + 1.2 * 0.044 * 0.040,
     D["anemo_x"] / 1000, (D["hub_z"] - P["arm_z"]) / 1000),
    ("fan cowl", 1.2 * P["cowl"][0] / 1000 * P["cowl"][1] / 1000, P["shield_x"] / 1000,
     (D["shield_top"] + P["cowl"][1] / 2 - P["arm_z"]) / 1000),
]
arm_cda = 2.0 * P["arm_w"] / 1000 * P["arm_len"] / 1000
F35 = {n: q35 * c for n, c, _, _ in elems}
F35["arm"] = q35 * arm_cda
tag("H1", f"35 m/s gust ({q35:.0f} Pa), wind across the arm: " + ", ".join(f"{n} {f:.1f} N" for n, f in F35.items())
    + f"; head total {sum(F35.values()):.1f} N")
aw, at = P["arm_w"], P["arm_t"]
I = (aw ** 4 - (aw - 2 * at) ** 4) / 12 * 1e-12
Zs = I / (aw / 2000)
E_AL, FY = 69e9, 145e6
L_arm = P["arm_len"] / 1000


def root_moment(q):
    m = sum(q * c * (x - x0 / 1000) for _, c, x, _ in elems) + q * arm_cda * L_arm / 2
    return m


def tip_defl(q):
    d = 0.0
    for _, c, x, _ in elems:
        a = min(x - x0 / 1000, L_arm)
        d += q * c * a ** 2 * (3 * L_arm - a) / (6 * E_AL * I)
    d += q * arm_cda / L_arm * L_arm ** 4 / (8 * E_AL * I)
    return d


M35 = root_moment(q35)
tag("H2", f"arm 25 x 25 x 2 mm: I {I * 1e12:.0f} mm4, Z {Zs * 1e9:.0f} mm3; root moment {M35:.1f} N m at 35 m/s; stress {M35 / Zs / 1e6:.1f} MPa; "
          f"factor {FY / (M35 / Zs):.1f} on {FY / 1e6:.0f} MPa")
tag("H3", f"tip deflection across the wind at 20 m/s ({q20:.0f} Pa): {tip_defl(q20) * 1000:.2f} mm; at 35 m/s {tip_defl(q35) * 1000:.2f} mm (target under 10 mm at 20 m/s)")
torsion = sum(q35 * c * z for _, c, _, z in elems)
tag("H4", f"torsion on the arm from offset loads at 35 m/s: {torsion:.2f} N m")

# masses (needed for the clamp checks), from the constructable model's component volumes (HMN-DDR-003)
from model import build_components  # noqa: E402
COMP = build_components(P)
cm = lambda *ks: sum(COMP[k].shape.volume / 1e9 * COMP[k].density for k in ks)   # kg
m_arm = cm("arm", "plug", "sleeves")
m_clamp = cm("saddle", "trim", "cheeks", "bands", "clamp_bolts")
m_shield = cm("plates", "rods", "spacers")
m_globe = m_shell + m_boss + 0.010 + cm("hanger")           # paint, gland and the brass hanger tube with its nuts
m_probe, m_th, m_anemo = 0.010, 0.020, 0.30 + cm("mast_bolt")
m_harness = 2 * 1.5 * 0.08 + 0.03
m_lanyard, m_hw = 0.02, 0.03                                # hardware: cable ties, paint and sealant
m_fan = 0.035 + cm("cowl", "fan_screws")                    # fan (assumed 35 g) plus the ASA cowl and its screws
m_adapter = cm("vblocks", "ascrews", "abands")
head = {"arm": m_arm, "clamp": m_clamp, "shield": m_shield, "fan and cowl": m_fan, "T/RH sensor": m_th, "globe": m_globe, "probe": m_probe,
        "anemometer": m_anemo, "harness": m_harness, "lanyards": m_lanyard, "hardware": m_hw}
m_head = sum(head.values())
arm_side = m_arm + m_shield + m_fan + m_th + m_globe + m_probe + m_anemo + m_lanyard
x_cg = (m_arm * (x0 + P["arm_len"] / 2) + (m_shield + m_fan) * P["shield_x"] + m_th * P["shield_x"] + (m_globe + m_probe) * P["globe_x"]
        + m_anemo * D["anemo_x"] + m_lanyard * P["globe_x"]) / arm_side / 1000
PRELOAD, MU = 1000.0, 0.4          # N per band, friction coefficient (FND-CAL-001 assumptions)
fric = MU * PRELOAD * 2
t_wind = sum(F35[n] * x for n, _, x, _ in elems) + F35["arm"] * (x0 / 1000 + L_arm / 2)
t_cap = fric * D["r"] / 1000
m_g = arm_side * 9.81 * x_cg
pull = m_g / (2 * P["band_dz"] / 1000)
tag("H5", f"clamp: wind twists the arm about the pole with {t_wind:.1f} N m against {t_cap:.1f} N m of friction (factor {t_cap / t_wind:.1f}); "
          f"weight {arm_side:.2f} kg at {x_cg * 1000:.0f} mm pulls the upper band with {pull:.0f} N against {2 * PRELOAD:.0f} N; "
          f"slip down {arm_side * 9.81:.0f} N against {fric:.0f} N")
f_head = sum(F35.values())
m_pole = f_head * P["arm_z"] / 1000 + FN_WIND_N * (P["fn_z0"] + 200) / 1000
tag("H6", f"added load on the pole at 35 m/s: head {f_head:.0f} N plus FieldNode with its shield {FN_WIND_N:.0f} N; about {m_pole:.0f} N m at the pole base (for the pole owner)")

# ------------------------------------------------------------------ I. Outdoor temperatures (R8)
print("\nI. Outdoor temperatures")
tg_hot = tg_from_mrt(80.0, 50.0, 0.3)
tag("I1", f"globe at 50 C air, MRT 80 C, 0.3 m/s: {tg_hot:.1f} C; NTC epoxy bead and SHT45 are rated well above this (125 C class, assumed for the NTC)")
tag("I2", f"FieldNode interior rise, dusty and worst sun position: {FN_RISE_SHIELD:.1f} K with the sun shield (FND-CAL-001 v0.2), "
          f"{FN_RISE_BARE:.1f} K without; at 50 C air {50 + FN_RISE_SHIELD:.1f} C with the shield ({50 + FN_RISE_BARE:.1f} C without) "
          f"against a 70 C electronics rating")

# ------------------------------------------------------------------ J. Fit to poles and installation (R10)
print("\nJ. Fit and installation")
half = math.radians(P["v_angle"] / 2)
for d in (P["pole_range"][0], P["pole_od"], P["pole_range"][1]):
    tag("J1", f"pole {d:.0f} mm: V-saddle contacts at +/- {d / 2 * math.cos(half):.0f} mm (saddle notch half-width {D['notch_half']:.0f} mm, adapter V {P['adapter_vblock'][0] / 2:.0f} mm); "
              f"band length {math.pi * d + 150:.0f} mm")
TASKS = [("FieldNode core with the pole adapter", 15), ("arm clamp", 6), ("arm with shield, fan, globe and anemometer, pre-assembled", 4),
         ("harness and cable ties", 5), ("lanyards", 2), ("commissioning and photo record", 5)]
tag("J2", "tasks (min): " + ", ".join(f"{n} {t}" for n, t in TASKS) + f"; total {sum(t for _, t in TASKS)} min for two people working in turn from one lift")

# ------------------------------------------------------------------ K. Mass (R15)
print("\nK. Mass")
tag("K1", "sensor head: " + ", ".join(f"{n} {m * 1000:.0f} g" for n, m in head.items()) + f"; head {m_head:.2f} kg")
tag("K2", f"sensor head {m_head:.2f} kg against the 4.0 kg of R15 (sensor head only, HMN-DDR-002); for information, FieldNode core with "
          f"its sun shield {FN_MASS:.2f} kg (FND-CAL-001 v0.4) plus pole adapter {m_adapter:.2f} kg: complete node {m_head + FN_MASS + m_adapter:.2f} kg")
tag("K3", f"largest part other than the arm: FieldNode panel {P['fn_panel'][0]:.0f} mm; anemometer across the cups {2 * P['cup_arm'] + P['cup_d']:.0f} mm (limit 300 mm)")

# ------------------------------------------------------------------ L. Cost (R13)
print("\nL. Cost")
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
tot = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows)
core = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows if r["item"].split()[0] in ("1", "12"))
budget_usd = None
for line in (ROOT / "project.yaml").read_text().splitlines():
    if line.startswith("budget_usd:"):
        budget_usd = float(line.split(":")[1].split("#")[0])
head_cost = tot - core
tag("L1", f"BOM {len(rows)} lines; sensor head (lines 2 to 11 and 13) ${head_cost:.2f}; FieldNode core with its sun shield and the "
          f"pole adapter (lines 1 and 12, counted against FieldNode) ${core:.2f}; full node ${tot:.2f}")
tag("L2", f"value-engineering target (budget_usd) ${budget_usd:.0f} for the sensor head; estimated cost of the constructable design "
          f"${head_cost:.2f}, ${abs(budget_usd - head_cost):.2f} {'under' if head_cost <= budget_usd else 'over'} the target")
