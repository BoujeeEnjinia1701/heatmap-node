"""HeatMap Node sizing calculations, HMN-CAL-001 v0.1 (TRL 3).

Run from the repo root:  python docs/04-calcs/sizing.py
Prints every number quoted in docs/04-calcs/01-sizing.md. Each line carries a tag such as
[A3] that the note cites. Geometry comes from cad/src/model.py (PARAMS, derived and the part
solids), the parts cost from bom/bom.csv and the budget from project.yaml. FieldNode figures
are quoted from FND-CAL-001 v0.1 in the FieldNode repo. First-principles estimates for a
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
FN_MASS = 2.41          # kg FieldNode core (FND-CAL-001 [F1])
FN_COST = 126.00        # USD FieldNode core (FND-CAL-001 [F2])
FN_WIND_N = 81.0        # N FieldNode wind load at 35 m/s (FND-CAL-001, section D)
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


print("HeatMap Node sizing, HMN-CAL-001 v0.1")
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
print("\nC. Radiation error of the naturally ventilated shield")
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
tag("C2", "air temperature error in full sun: " + ", ".join(f"{e:.2f} C at {v:.1f} m/s" for v, e in errs.items()))
v_05 = ETA * q_abs / (RHO * a_flow * K_VENT * CP * 0.5)
tag("C3", f"error falls to 0.5 C at {v_05:.1f} m/s; with half the assumed ventilation (k = {K_VENT / 2}) the error at 1 m/s is {shield_err(1.0, K_VENT / 2):.2f} C")
FAN_V, FAN_W, FAN_DUTY = 3.0, 0.30, 0.10
e_fan = ETA * q_abs / (RHO * a_flow * FAN_V * CP)
tag("C4", f"option: fan-aspirated at {FAN_V:.0f} m/s inside the stack: {e_fan:.2f} C; fan {FAN_W:.2f} W at {FAN_DUTY * 100:.0f} % duty = {FAN_W * FAN_DUTY * 1000:.0f} mW")

terms, rss, worst = budget(errs[1.0])
tag("B4", "WBGT error budget at the example with the shield error at 1 m/s: " + ", ".join(f"{k_} {t:.2f}" for k_, t in terms.items())
    + f"; RSS {rss:.2f} C, worst case {worst:.2f} C (model error of the Liljegren method not included)")
terms_f, rss_f, worst_f = budget(e_fan)
tag("B5", f"same with a fan-aspirated shield: RSS {rss_f:.2f} C, worst case {worst_f:.2f} C; with wind known to 0.2 m/s and a fan: "
          f"RSS {math.sqrt(sum(t * t for k_, t in terms_f.items() if k_ != 'v') + (abs(sens['v']) * 0.2) ** 2):.2f} C")
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
tag("E2", f"pole seen from the globe: {width:.1f} deg wide; with the arm pointing east or west the sun passes behind it for about "
          f"{width / 15:.1f} h a day (15 deg/h mean azimuth rate, assumed)")

# ------------------------------------------------------------------ F. Power (R7)
print("\nF. Sensor power")
e_sht = 3.3 * 0.4e-3 * 8.3e-3          # J per high-repeatability reading (assumed datasheet class)
e_ntc = VREF * i_ntc * 0.010
p_reed = 3.3 / 100e3 * 3.3             # W if the reed rests closed (worst case)
p_idle = 3.3 * 2e-6                    # W sleep of the T and RH sensor and pull-ups (assumed)
p_avg = (e_sht + e_ntc) * 1440 / 86400 + p_reed + p_idle
tag("F1", f"per reading: T/RH {e_sht * 1e6:.1f} uJ, NTC {e_ntc * 1e6:.1f} uJ; 1,440 readings a day; reed pull-up worst case {p_reed * 1000:.3f} mW")
tag("F2", f"average sensor load {p_avg * 1000:.3f} mW, {p_avg / FN_ALLOW_W * 100:.2f} % of the {FN_ALLOW_W * 1000:.0f} mW FieldNode design allowance; "
          f"with the fan option {(p_avg + FAN_W * FAN_DUTY) * 1000:.0f} mW")

# ------------------------------------------------------------------ G. Data (R6)
print("\nG. Payload, airtime and storage")
FIELDS = [("air temperature mean", 2), ("air temperature max", 2), ("RH mean", 2), ("globe temperature mean", 2),
          ("globe temperature max", 2), ("wind mean", 2), ("wind gust", 2), ("calm share (below start-up)", 1),
          ("battery voltage", 2), ("status flags", 1), ("sequence number", 2)]
nbytes = sum(b_ for _, b_ in FIELDS)
tag("G1", f"payload {nbytes} B: " + ", ".join(f"{n} {b_}" for n, b_ in FIELDS))
store = 96 * 7 * FN_REC_B
tag("G2", f"96 uplinks a day, {FN_AIRTIME_SF9} s/day at SF9 (FND-CAL-001); 7 days stored at {FN_REC_B} B per record = {store / 1000:.1f} kB")
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

# masses (needed for the clamp checks)
parts = build_parts(P)
vol = lambda k: parts[k].volume / 1e9                       # m3
m_arm = vol("arm") * 2700
bands_m = 2 * 0.013 * 0.0007 * (math.pi * P["pole_range"][1] / 1000 + 0.15) * 7900
m_clamp = (vol("clamp") - 2 * 0.013 * 0.0015 * math.pi * P["pole_od"] / 1000) * 2700 + bands_m
rod_v = 3 * math.pi * (P["rod_d"] / 2000) ** 2 * stack
m_shield = (vol("shield") - rod_v) * 1070 + rod_v * 7900
m_globe = m_shell + m_boss + 0.010                          # paint and gland
m_probe, m_th, m_anemo = 0.010, 0.020, 0.30
m_harness = 2 * 1.5 * 0.08 + 0.03
m_lanyard, m_hw = 0.02, 0.05
m_adapter = vol("adapter") * 1070 * 0.9 + 2 * 0.013 * 0.0007 * (math.pi * P["pole_range"][1] / 1000 + 0.15) * 7900
head = {"arm": m_arm, "clamp": m_clamp, "shield": m_shield, "T/RH sensor": m_th, "globe": m_globe, "probe": m_probe,
        "anemometer": m_anemo, "harness": m_harness, "lanyards": m_lanyard, "hardware": m_hw}
m_head = sum(head.values())
arm_side = m_arm + m_shield + m_th + m_globe + m_probe + m_anemo + m_lanyard
x_cg = (m_arm * (x0 + P["arm_len"] / 2) + m_shield * P["shield_x"] + m_th * P["shield_x"] + (m_globe + m_probe) * P["globe_x"]
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
tag("H6", f"added load on the pole at 35 m/s: head {f_head:.0f} N plus FieldNode {FN_WIND_N:.0f} N; about {m_pole:.0f} N m at the pole base (for the pole owner)")

# ------------------------------------------------------------------ I. Outdoor temperatures (R8)
print("\nI. Outdoor temperatures")
tg_hot = tg_from_mrt(80.0, 50.0, 0.3)
tag("I1", f"globe at 50 C air, MRT 80 C, 0.3 m/s: {tg_hot:.1f} C; NTC epoxy bead and SHT45 are rated well above this (125 C class, assumed for the NTC)")
fn_rise = 73.3 - 45.0
tag("I2", f"FieldNode interior rise, dusty and worst sun position, no shield: {fn_rise:.1f} K (FND-CAL-001); at 50 C air {50 + fn_rise:.1f} C, "
          f"at 60 C air {60 + fn_rise:.1f} C against a 70 C electronics rating")

# ------------------------------------------------------------------ J. Fit to poles and installation (R10)
print("\nJ. Fit and installation")
half = math.radians(P["v_angle"] / 2)
for d in (P["pole_range"][0], P["pole_od"], P["pole_range"][1]):
    tag("J1", f"pole {d:.0f} mm: V-saddle contacts at +/- {d / 2 * math.cos(half):.0f} mm (saddle half-width {P['saddle'][0] / 2:.0f} mm); "
              f"band length {math.pi * d + 150:.0f} mm")
TASKS = [("FieldNode core with the pole adapter", 15), ("arm clamp", 6), ("arm with shield, globe and anemometer, pre-assembled", 4),
         ("harness and cable ties", 5), ("lanyards", 2), ("commissioning and photo record", 5)]
tag("J2", "tasks (min): " + ", ".join(f"{n} {t}" for n, t in TASKS) + f"; total {sum(t for _, t in TASKS)} min for two people working in turn from one lift")

# ------------------------------------------------------------------ K. Mass (R15)
print("\nK. Mass")
tag("K1", "sensor head: " + ", ".join(f"{n} {m * 1000:.0f} g" for n, m in head.items()) + f"; head {m_head:.2f} kg")
tag("K2", f"FieldNode core {FN_MASS:.2f} kg (FND-CAL-001) plus pole adapter {m_adapter:.2f} kg: complete node {m_head + FN_MASS + m_adapter:.2f} kg (target 4.0 kg)")
tag("K3", f"largest part other than the arm: FieldNode panel {P['fn_panel'][0]:.0f} mm; anemometer across the cups {2 * P['cup_arm'] + P['cup_d']:.0f} mm (limit 300 mm)")

# ------------------------------------------------------------------ L. Cost (R13)
print("\nL. Cost")
rows = list(csv.DictReader((ROOT / "bom" / "bom.csv").open()))
tot = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows)
core = sum(float(r["qty"]) * float(r["unit_cost_usd"]) for r in rows if r["item"].startswith("1 "))
budget_usd = None
for line in (ROOT / "project.yaml").read_text().splitlines():
    if line.startswith("budget_usd:"):
        budget_usd = float(line.split(":")[1].split("#")[0])
head_cost = tot - core
tag("L1", f"BOM {len(rows)} lines; sensor head (lines 2 to {len(rows)}) ${head_cost:.2f}; FieldNode core ${core:.2f}; full node ${tot:.2f}")
tag("L2", f"budget_usd ${budget_usd:.0f}: sensor head {'within' if head_cost <= budget_usd else 'over'} by ${abs(budget_usd - head_cost):.2f}; "
          f"full node over by ${tot - budget_usd:.2f}")
