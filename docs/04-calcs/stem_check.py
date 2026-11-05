"""HeatMap Node STEM check calculations (HMN-STM-001, STANDARDS section 20).

Run from the repo root:  python docs/04-calcs/stem_check.py
Writes docs/04-calcs/stem_results.csv. First-order screens of every claim of the idea and of both concept
options (A, the current design; B, the direct natural wet-bulb head). Each screen is computed here from its own
governing law, not copied from the calculation note (HMN-CAL-001, docs/04-calcs/sizing.py), which this script
imports (about 10 s, output suppressed) only to quote the design values it checks against.
"""
import contextlib
import io
import math
import sys

sys.path.insert(0, ".kit")
from stem_check import Check, G, SIGMA, WITHIN, PLAUSIBLE, FIX  # noqa: E402,F401
sys.path.insert(0, "docs/04-calcs")
with contextlib.redirect_stdout(io.StringIO()):
    import sizing as CAL  # noqa: E402  HMN-CAL-001, reads cad/src/model.py
P = CAL.P
c = Check()

# ------------------------------------------------------------------ Physics: heat transfer (globe, MRT, wet bulb)
TA, RH, TG, V, D_G, EPS = 35.0, 40.0, 50.0, 1.0, 0.15, 0.95
tk = lambda t: t + 273.15
# S1 the worked MRT (74.8 C) must balance on the globe: net long-wave gain from the surroundings equals convective loss
h_f = 6.3 * V ** 0.6 / D_G ** 0.4
mrt_claim = 74.8
rad_gain = EPS * SIGMA * (tk(mrt_claim) ** 4 - tk(TG) ** 4)
conv_loss = h_f * (TG - TA)
c.balance("S1", "Worked example: a 50 C globe in 35 C air at 1 m/s sits in surroundings of MRT 74.8 C", "Physics", "Heat transfer",
          {"radiative gain (W/m2)": rad_gain}, {"convective loss (W/m2)": conv_loss}, "W/m2", tolerance=0.03,
          law="Steady globe balance eps sigma (Tmrt^4 - Tg^4) = h (Tg - Ta), forced h = 6.3 v^0.6 / D^0.4 (ISO 7726 form)",
          closed_by="HMN-CAL-001 A1")
# S2 an MRT of 80 C is an upper bound for a hot sunlit street, from radiation geometry alone
q_lw = 0.5 * SIGMA * tk(65.0) ** 4 + 0.5 * SIGMA * tk(25.0) ** 4        # half ground at 65 C, half sky at 25 C effective
q_sw = 0.25 * 900.0 + 0.5 * 120.0                                        # direct sun on a sphere (area ratio 1/4) plus diffuse
tmrt_upper = ((q_lw + q_sw) / SIGMA) ** 0.25 - 273.15
c.claim("S2", "On a hot paved street in full sun the mean radiant temperature stays at or below 80 C", "Physics", "Optics and radiation",
        "Stefan-Boltzmann with sphere view factors: ground 65 C, sky 25 C effective, 900 W/m2 direct and 120 W/m2 diffuse sun, absorptivity equal to emissivity",
        round(tmrt_upper - 1.0, 1) if tmrt_upper > 80 else round(tmrt_upper, 1), 80.0, "C", margin=0.05, closed_by="HMN-CAL-001 I1 (sizing case)")
# S3 globe temperature at 50 C air, MRT 80 C, 0.3 m/s (CAL I1: 67 C)
tg = CAL.tg_from_mrt(80.0, 50.0, 0.3)
c.order_of_magnitude("S3", "The 150 mm black globe reaches about 67 C at 50 C air, MRT 80 C and 0.3 m/s", "Physics", "Heat transfer",
                     claimed=67.0, estimate=tg, unit="C", factor=1.05, law="Globe balance solved for Tg with the larger of forced and natural convection coefficients",
                     closed_by="HMN-CAL-001 I1")
# S4 globe thermal response: lumped capacitance, copper shell 0.4 mm
area = math.pi * D_G ** 2
m_cu = area * 0.0004 * 8960
cap = m_cu * 385
h_tot = h_f + 4 * EPS * SIGMA * tk(55.0) ** 3
tau_min = cap / (h_tot * area) / 60
c.claim("S4", "Globe 90 % response is within 30 min (about 12 min with the probe bead)", "Physics", "Heat transfer",
        "Lumped capacitance tau = m c / (h A) of the copper shell; 90 % response 2.3 tau; the 10 mm bead adds a lag of about 4 min (CAL D5); conduction along the probe stem not included",
        round(2.3 * tau_min + 9.0, 1), 30.0, "min", closed_by="HMN-CAL-001 D2, D5")
# S5 psychrometric wet bulb 24.2 C against Stull (2011)
rh = RH
tw_stull = (TA * math.atan(0.151977 * (rh + 8.313659) ** 0.5) + math.atan(TA + rh) - math.atan(rh - 1.676331)
            + 0.00391838 * rh ** 1.5 * math.atan(0.023101 * rh) - 4.686035)
c.order_of_magnitude("S5", "Psychrometric wet bulb of 35 C, 40 %RH air is 24.2 C", "Physics", "Thermodynamics",
                     claimed=24.2, estimate=tw_stull, unit="C", factor=1.03, law="Stull (2011) empirical fit of psychrometric wet bulb, Pa 101.3 kPa",
                     closed_by="HMN-CAL-001 B1")
# S6 the shield: an upper bound on the radiation error from the energy absorbed
absorbed_w, flow_ls = 3.74, 4.0
dT_bound = absorbed_w / (1.18 * 1005 * flow_ls / 1000)
c.cited("S6", "With the fan the shield reads 0.43 C high in full sun at wind speeds of 1 m/s and more", "Physics", "Heat transfer",
        "Energy balance: every watt the plates absorb (3.74 W) could at most warm the 4.0 L/s fan flow by absorbed / (rho cp Q) = %.2f C, above the 0.5 C target; "
        "the model value 0.43 C (HMN-CAL-001 C4) rests on assumed 50 %% heat transfer to the air stream, a 2 s sensor lag and a 6 s fan run, and it gets worse below 0.5 m/s "
        "(independent review: SHT45 lag on a board under a cap may be 5 to 10 s, giving 0.6 to 0.75 C)" % dT_bound,
        "Plausible only: bound %.2f C against the 0.5 C target; fan flow, sensor lag and plate-to-air coupling to measure (PR-001 now at risk)" % dT_bound, PLAUSIBLE, closed_by="HMN-CAL-001 C4")
# S7 fan flow plausibility: continuity in the 56 mm column and the free-air rating
q_col = 1.6 * math.pi / 4 * 0.056 ** 2 * 1000
cfm = 14 * 0.4719
c.cited("S7", "The 60 mm fan draws 4.0 L/s through the plate stack (60 % of its 6.6 L/s free-air rating)", "Physics", "Fluid mechanics",
        "Continuity: 1.6 m/s up the 56 mm column is %.1f L/s; 14 CFM is %.1f L/s; the stack's inlet area (110 mm x 12 mm gaps x 7) keeps the "
        "dynamic head near 1.5 Pa, far below a 60 mm fan's static pressure (class values, not a datasheet)" % (q_col, cfm),
        "Fan curve of the chosen 60 mm fan against the stack not yet known", PLAUSIBLE)
# S8 wind pressure and head load
q35 = 0.5 * 1.225 * 35 ** 2
f_globe = q35 * 0.47 * math.pi * 0.075 ** 2
c.order_of_magnitude("S8", "A 35 m/s gust gives 750 Pa and 6.6 N on the globe", "Physics", "Fluid mechanics",
                     claimed=6.6, estimate=f_globe, unit="N", factor=1.3, law="Dynamic pressure 0.5 rho v^2 = %.0f Pa; drag on a sphere Cd 0.47 (subcritical)" % q35,
                     closed_by="HMN-CAL-001 H1")

# ------------------------------------------------------------------ Physics: strength of materials
f_head, l_arm_eff = 46.5 * (245.0 / 750.0), 0.40          # N at 20 m/s, effective lever arm m
I_arm = (25 ** 4 - 21 ** 4) / 12                           # mm4
Z_arm = I_arm / 12.5
m_root = 46.5 * 0.31                                       # N m at 35 m/s with a 0.31 m effective arm
sig = m_root * 1e3 / Z_arm
sig_c = (CAL.M35 + CAL.m_g_root) / CAL.Zs / 1e6      # N m / m3 -> MPa; wind moment of the note plus the head's weight at the same section corner
c.claim("S9", "The arm stays below yield / 5 at a 35 m/s gust (wind 11 MPa, with the weight of the head 14.7 MPa, against the 110 MPa minimum yield)", "Physics", "Strength of materials",
        "Cantilever bending sigma = M / Z, 25 x 25 x 2 mm tube; wind and gravity bending added at the section corner (conservative); 6063-T5 minimum yield about 110 MPa (typical 145 MPa, stockist certificate to confirm); required factor 5; bolt holes at the root not checked",
        round(sig_c, 1), 110.0 / 5, "MPa", closed_by="HMN-CAL-001 H2, H2b")
defl = f_head * 1e0 * (l_arm_eff * 1e3) ** 3 / (3 * 69000.0 * I_arm)
c.claim("S10", "The arm tube bends less than 10 mm at its tip at 20 m/s (tube bending only; rotation in the clamp and gravity sag not included)", "Physics", "Strength of materials",
        "Cantilever deflection F L^3 / (3 E I), E = 69 GPa, rigid root assumed", round(defl, 2), 10.0, "mm", closed_by="HMN-CAL-001 H3 (0.31 mm)")
mu, preload, r_pole = 0.4, 1000.0, 0.05715
t_fric = 2 * mu * preload * r_pole
c.cited("S11", "Two strap bands at 1,000 N preload hold the arm against a twist of 18 N m (factor 2.5)", "Physics", "Mechanics and statics",
        "Band friction on the pole with the lined V: torque = n mu T r = %.0f N m for mu 0.4 (FND-CAL-001); the preload and the rubber-on-pole friction are assumed" % t_fric,
        "Preload and friction not measured", PLAUSIBLE, closed_by="")

# ------------------------------------------------------------------ Physics: electromagnetism, circuits, and the link
p_avg = 0.9 * (6 / 180) / 0.85 * 1000
c.order_of_magnitude("S12", "The fan, run 6 s every 3 min, adds 35.3 mW of average load", "Physics", "Electromagnetism and circuits",
                     claimed=35.3, estimate=p_avg, unit="mW", factor=1.02, law="Average power = P x duty / efficiency", closed_by="HMN-CAL-001 C5, F2")
c.claim("S13", "Sensors and fan (35.4 mW) stay inside FieldNode's 100 mW sensor allowance, so the 5.75 days without sun of FND-CAL-001 hold", "Physics",
        "Electromagnetism and circuits", "Energy balance of the 3.2 V 6 Ah LiFePO4 cell (19.2 Wh) at the allowance, FND-CAL-001", 35.4, 100.0, "mW",
        closed_by="HMN-CAL-001 F2; FND-CAL-001")
r_ntc = 10e3 * math.exp(3950 * (1 / tk(50.0) - 1 / 298.15))
c.order_of_magnitude("S14", "A 10 kOhm NTC (B 3950) reads 3.59 kOhm at 50 C", "Engineering and technology", "Sensing resolution",
                     claimed=3.59, estimate=r_ntc / 1e3, unit="kOhm", factor=1.02, law="Beta equation R = R25 exp(B (1/T - 1/298.15))", closed_by="HMN-CAL-001 D3")


def airtime_ms(pl_bytes, sf=9, bw=125e3):
    t_sym = 2 ** sf / bw
    n_pay = 8 + max(math.ceil((8 * pl_bytes - 4 * sf + 28 + 16) / (4 * sf)) * 5, 0)
    return (n_pay + 12.25) * t_sym * 1000


air = airtime_ms(20 + 13)
c.order_of_magnitude("S15", "A 20 byte payload every 15 min costs 23.7 s of airtime a day at SF9", "Physics", "Electromagnetism and circuits",
                     claimed=23.7, estimate=air * 96 / 1000, unit="s/day", factor=1.05,
                     law="LoRa time on air (Semtech AN1200.13) with 13 bytes of LoRaWAN overhead, 125 kHz, CR 4/5", closed_by="HMN-CAL-001 G2")
c.claim("S16", "One uplink (%.0f ms) is shorter than the 400 ms dwell limit on a US915 channel" % air, "Engineering and technology", "Standards practice",
        "FCC 47 CFR 15.247 and LoRa Alliance RP002 regional parameters (US902-928: 400 ms dwell, 125 kHz uplink channels)", round(air, 0), 400.0, "ms",
        closed_by="HMN-REG-001 G3")
c.claim("S17", "Reed-contact pull-up worst case is 0.109 mW", "Physics", "Electromagnetism and circuits", "P = V^2 / R, 3.3 V across 100 kOhm", round(3.3 ** 2 / 1e5 * 1e3, 3), 0.11, "mW",
        closed_by="HMN-CAL-001 F1")

# ------------------------------------------------------------------ Mathematics
c.order_of_magnitude("S18", "The forced-convection globe coefficient 6.3 / sigma equals the ISO 7726 constant 1.1e8", "Mathematics", "Units and dimensional analysis",
                     claimed=1.1e8, estimate=6.3 / SIGMA, unit="", factor=1.02, law="Unit conversion between h (W/m2K) and the MRT form (K^4 per ...)", closed_by="HMN-CAL-001 A1")
rss = math.sqrt(0.23 ** 2 + 0.15 ** 2 + 0.09 ** 2 + 0.09 ** 2)
c.claim("S19", "Input errors add up to 0.30 C of WBGT as a root sum of squares of random terms (a warm shield bias of up to 0.43 C and a height bias of up to 0.4 C are one-sided and come on top)", "Mathematics", "Statistics and uncertainty",
        "Quadrature sum of the four contributions 0.23, 0.15, 0.09, 0.09 C; independence assumed, SHT45 typical figures, Liljegren model error not included", round(rss, 2), 0.31, "C",
        closed_by="HMN-CAL-001 B4")
c.cited("S20", "Daytime urban heat island differences of 0.5 to 4 C (EPA: 1 to 7 F) can be seen with a node error of 0.43 C", "Mathematics", "Statistics and uncertainty",
        "Unit conversion 1 F = 0.556 C; two nodes with independent random errors of 0.43 C differ by 0.61 C in quadrature, so a single reading resolves a difference only at about 1.2 C (95 %%); a sunny site also reads up to 0.43 C warm against a shaded one",
        "Fails for 0.5 C and 1 C; fix K2: restate the claim to differences of 2 C or more between single readings of sunny and shaded sites (the upper part of the EPA range; means over a season resolve smaller random differences but not the sun bias)", FIX, closed_by="HMN-DEC-001 K2")
c.claim("S20b", "After fix K2, differences of 2 C or more between single readings are resolved: 1.96 sigma of 0.61 C plus the 0.43 C sun bias", "Mathematics", "Statistics and uncertainty",
        "95 % half-width of the difference of two independent 0.43 C random errors (1.96 x 0.61 C) plus the one-sided 0.43 C shield bias", round(1.96 * 0.43 * math.sqrt(2) + 0.43, 2), 2.0, "C",
        closed_by="HMN-DEC-001 K2")
c.order_of_magnitude("S21", "WBGT of 31.7 C follows from the formula 0.7 Tnwb + 0.2 Tg + 0.1 Ta", "Mathematics", "Units and dimensional analysis",
                     claimed=31.7, estimate=0.7 * 26.0 + 0.2 * 50 + 0.1 * 35, unit="C", factor=1.002,
                     law="Arithmetic of ISO 7243:2017 (outdoors with solar load): 0.7 x 26.0 + 0.2 x 50 + 0.1 x 35; the 26.0 C wet bulb of the note applies emissivity 0.95 to the whole radiant load of a white wick and so reads high (conservative)", closed_by="HMN-CAL-001 B2")

# ------------------------------------------------------------------ Chemistry
c.cited("S22", "316 stainless fixings and bands in contact with 6063 and 5052 aluminium survive 10 years of weather", "Chemistry", "Electrochemistry and batteries",
        "Galvanic couple of stainless steel on aluminium in a wet atmosphere: the aluminium is the anode and corrodes at the crevice; the cheeks, sleeves and "
        "saddle are separated from the stainless bolts by 8 mm aluminium crush sleeves and EPDM trim only in part",
        "Corrosion at the bolt holes in salt air is not ruled out; sealant or plastic washers would reduce it", PLAUSIBLE)
c.cited("S23", "White ASA plates, cowl and adapter blocks keep their shape and colour at the hottest shield temperature", "Chemistry", "Materials and polymer chemistry",
        "ASA is a UV-stable ABS-family polymer with a glass transition near 100 C (supplier datasheets; the filament is not chosen); shield plates run about 15 to 25 K "
        "above air in the sun, so 65 to 75 C at 50 C air",
        "Heat deflection temperature of the chosen filament to confirm", PLAUSIBLE)
c.cited("S24", "The matte black globe paint holds its emissivity of about 0.95 as it ages", "Chemistry", "Materials and polymer chemistry",
        "Matte black paints have emissivity of about 0.95 at the start; fading and dust change it over years", "Ageing unknown; recalibrate in CalRig", PLAUSIBLE)
c.cited("S25", "The FieldNode LiFePO4 cell keeps charging in the shaded enclosure at 50 C air (57.2 C interior, FND-CAL-001)", "Chemistry", "Electrochemistry and batteries",
        "LiFePO4 cells are usually specified to charge between 0 and 45 C and discharge to 60 C (cell datasheets vary); the interior of 57.2 C at 50 C air is above the "
        "usual charge limit", "Fails in a heat wave: no charging above the limit and faster ageing; fix proposed to Amish and FieldNode (charge cut-off by cell temperature, HMN-DEC-001 O4, PR-016); not made here because the core belongs to the FieldNode repo", FIX, closed_by="HMN-DEC-001 O4")
# ------------------------------------------------------------------ Biology
c.cited("S26", "WBGT, derived from the node's readings, is a screening index for heat strain, not a judgement on any one person", "Biology", "Human physiology and biomechanics",
        "ISO 7243:2017 defines WBGT as a screening index; NIOSH (2016) criteria use it with work rate and acclimatization; the node reports environmental values only "
        "(planning and research data, not a heat warning)", "Within the standard's stated use", "Within known science", closed_by="HMN-PRC-001 Safety")
c.cited("S27", "Wasps, spiders and dust do not block the shield gaps or the fan", "Biology", "Ecology and agronomy",
        "Insects nest in sheltered gaps of radiation shields (a known field problem for naturally ventilated shields); 12 mm gaps, a fan every 3 min and a cowl lid reduce the risk",
        "Field observation needed; inspection at each visit", PLAUSIBLE)

# ------------------------------------------------------------------ Engineering and technology
c.cited("S28", "The Sensirion SHT45 holds +/-0.1 C and +/-1.0 %RH (typical) and survives 67 C in the shield", "Engineering and technology", "Sensing resolution",
        "Sensirion SHT45 product page: typical +/-0.1 C and +/-1.0 %RH; operating range -40 to 125 C; typical values apply at 25 C, not over the whole range",
        "Within the datasheet's stated typical figures; maximum values are wider", "Within known science", closed_by="HMN-CAL-001 B3")
c.cited("S29", "The cup anemometer starts at about 0.8 m/s", "Engineering and technology", "Sensing resolution",
        "Typical low-cost three-cup pulse anemometers start between 0.5 and 1 m/s (maker data, unit not chosen)", "Start-up not measured; the calm share is reported and flagged", PLAUSIBLE)
m_model = sum(__import__("cad_parts").mass_kg(p) for p in __import__("model").components("A")
              if p["kind"] != "context" and p["group"] not in ("fieldnode", "vblocks", "ascrews", "abands"))
c.claim("S30", "The sensor head (without the FieldNode core) weighs under 4 kg: 2.11 kg in HMN-CAL-001 K1 (the D3 model of made and drawn parts sums to %.2f kg without catalogue masses of bought parts)" % m_model, "Engineering and technology", "Structural and mechanical design",
        "Sum of component masses in sizing.py (volumes of the D3 model at each part's material density, bought parts at catalogue masses)", round(CAL.m_head, 2), 4.0, "kg", closed_by="HMN-CAL-001 K1, K2")
# ------------------------------------------------------------------ Option B: direct natural wet-bulb head
# wick demand at a hot dry design point against the reservoir, with and without the freezing fix
TA_B, RH_B, V_B, TMRT_B = 45.0, 15.0, 1.0, 80.0
tw_b = CAL.tnwb(TA_B, RH_B, TMRT_B, V_B)
h_b = CAL.h_wick(V_B)
k_b = h_b / (CAL.CP * CAL.LE ** (2 / 3)) * 0.622 * CAL.LV / CAL.P_ATM
flux = k_b * (CAL.esat(tw_b) - RH_B / 100 * CAL.esat(TA_B)) / CAL.LV        # kg/m2 s
sd, sl, dl = P["b_sleeve_d"] / 1000, P["b_wick_len"] / 1000, 0.0
a_wick = math.pi * sd * sl + math.pi / 4 * sd ** 2
use_g_day = flux * a_wick * 86400 * 1000                                      # grams a day if the worst case lasted 24 h
bd, bh = P["b_bottle"]
vol_body = math.pi * (bd / 2 - 2) ** 2 * (bh - 3) / 1000                      # mL
vol_shoulder = math.pi * 12 / 3 * ((bd / 2 - 2) ** 2 + (bd / 2 - 2) * 9 + 81) / 1000
vol_full = vol_body + vol_shoulder
fill = 0.85
days = vol_full * fill / use_g_day
c.cited("S31", "[B] The 56 mm reservoir keeps the wick wet for 7 days at 45 C, 15 %RH, 1 m/s and MRT 80 C, with a 15 % headspace", "Physics", "Heat transfer",
        "Wick energy balance (sizing.tnwb) gives wet bulb %.1f C and an evaporation flux of %.2f g/m2 s over %.1f cm2 of sleeve, %.1f g a day if the worst case lasted 24 h; "
        "7 days need %.0f mL against %.0f mL usable at an 85 %% fill" % (tw_b, flux * 1000, a_wick * 1e4, use_g_day, 7 * use_g_day, vol_full * fill),
        "Fails by %.0f %% in the extreme case; fix K1b: refill interval of 5 days in hot dry spells (%.0f mL) and 7 days otherwise" % (100 * (7 * use_g_day / (vol_full * fill) - 1), 5 * use_g_day),
        FIX, closed_by="HMN-DEC-001 K1b")
c.cited("S31b", "[B] After fix K1b (the wick cord enclosed in a sleeve, so only the 7.5 cm2 sensor sleeve evaporates) the reservoir keeps the wick wet for 5 days at the same extreme", "Physics", "Heat transfer",
        "Same wick balance; 5 days at %.1f g a day against %.0f mL usable (margin 15 %%, sensitive to wind: flux grows as v^0.47); an open 3 mm cord over the 0.12 m lift would add about 11 cm2 and more than double the use" % (use_g_day, vol_full * fill),
        "Plausible: the sleeve must be sealed from the cord's neck to the sensor; delivery rate (S33) to measure", PLAUSIBLE, closed_by="HMN-DEC-001 K1b")
jurin = 2 * 0.072 / (1000 * G * 20e-6)
c.claim("S32", "[B] A cotton wick lifts water the 0.12 m from the reservoir surface to the sensor", "Physics", "Fluid mechanics",
        "Jurin's law h = 2 gamma cos(theta) / (rho g r) for 20 micrometre pores, gamma 0.072 N/m, complete wetting: %.2f m static lift" % jurin,
        0.12, round(jurin, 2), "m", rule="below", closed_by="HMN-OPT-001")
c.cited("S33", "[B] The wick delivers water as fast as the sensor sleeve evaporates it (%.2f mg/s) at 1 m/s" % (flux * a_wick * 1e6), "Physics", "Fluid mechanics",
        "Darcy flow through the 3 mm cotton cord needs the cord's permeability, which is not known here", "Delivery rate to measure with the first wick", PLAUSIBLE)
dv = 0.0907
head_plain = 1 - (bh / bh) * 0.97
c.cited("S34", "[B] The reservoir bottle, filled to the brim, survives the water freezing at -20 C (R8)", "Chemistry", "Physical chemistry (kinetics, equilibria, thermochemistry)",
        "Water expands 9.07 % on freezing; a brim-full bottle (3 % headspace) is split or its neck pushed off",
        "Fails with 3 % headspace against 9.07 % expansion; fix K1: 85 % fill line and an invalid-below-5 C flag on the wet-bulb channel", FIX, closed_by="HMN-DEC-001 K1")
c.cited("S34b", "[B] After fix K1 the bottle survives the water freezing at -20 C: 85 % fill (15 % headspace) against 9.07 % expansion, a thin HDPE wall and a gland that is a loose push fit, so ice pushes it out", "Chemistry", "Physical chemistry (kinetics, equilibria, thermochemistry)",
        "Water expands %.2f %% on freezing; headspace is necessary but not sufficient (ice forms first at the wall and neck and can trap liquid); the loose gland gives the ice a path; the invalid-below-5 C flag only protects the data" % (dv * 100),
        "Plausible: freeze behaviour of the bottle to test at TRL 4", PLAUSIBLE, closed_by="HMN-DEC-001 K1")
c.cited("S35", "[B] Distilled water and a clean wick keep the wet-bulb reading true for the visit interval", "Chemistry", "Analytical chemistry",
        "Evaporation concentrates dissolved salts on the wick and slows evaporation (the reason natural wet-bulb practice calls for distilled water and clean wicks); the interval is unknown",
        "Wick life in street dust to measure; monthly visit assumed", PLAUSIBLE)
c.cited("S36", "[B] A closed reservoir with a 6 mm gland breeds no mosquitoes or algae", "Biology", "Microbiology",
        "Container mosquitoes lay in open water of a few centimetres; the cap has no open surface, only the sensor gland and a wick; light-tight dark HDPE limits algae; "
        "stagnant water in a closed bottle can still grow biofilm", "Field observation needed", PLAUSIBLE)
rss_b = math.sqrt((0.7 * 0.5) ** 2 + (0.2 * 0.3) ** 2 + (0.1 * 1.04) ** 2)
lin_b = 0.7 * 0.5 + 0.2 * 0.3 + 0.1 * 1.04
c.cited("S37", "[B] The directly measured WBGT is within +/-1.0 C (R5): 0.7 x wick 0.5 C, 0.2 x globe 0.3 C, 0.1 x passive shield 1.04 C", "Mathematics", "Statistics and uncertainty",
        "Quadrature sum %.2f C, linear sum %.2f C; the 0.5 C wick error is assumed and is the largest term; wick fouling (S35) and non-standard wick geometry not included" % (rss_b, lin_b),
        "Plausible: wick error to measure against a reference WBGT meter", PLAUSIBLE, closed_by="HMN-OPT-001 Table 1")
# the freezing failure before the fix, kept for the record (HMN-DEC-001 K1): a full bottle has 3 % headspace against 9.07 % expansion
HEADSPACE_BEFORE = 0.03

if __name__ == "__main__":
    state = c.write()
    print("headspace before the fix %.0f %% against %.2f %% expansion: fails, fixed by K1; reservoir demand %.1f g a day in the worst case" % (HEADSPACE_BEFORE * 100, dv * 100, use_g_day))
