"""HeatMap Node parametric model, kit 1.9 interface (STANDARDS section 24), detail level D3 for every option.

Run from the repo root:
    python .kit/cad_check.py --export     fidelity check, STEP per part and per assembly (cad/step/)
    python cad/src/model.py               part list with masses; STL of the chosen design (cad/stl/)
    python cad/src/model.py --check       constructability checks (touches and clearances) on the chosen design

Axes: the existing street pole is the Z axis (x = y = 0), Z is up with the pavement at z = 0. The sensor arm
reaches out along +X, which points toward the equator (HMN-DDR-002). The FieldNode core is built in its own
convention (panel facing -Y) and turned by fn_azimuth about the pole, so it sits on the pole's +X face above the
arm with its panel facing +X (HMN-DEC-001, item 3).

Options (HMN-OPT-001):
    A  fan-aspirated shield, 150 mm globe and cup anemometer: air temperature and humidity are read from air
       the fan draws past the sensor, the globe and wind speed feed a model that derives MRT and WBGT. This is
       the current design (HMN-PRC-001, HMN-DDR-001 to 003); the drawing, BOM and build plan describe it.
    B  direct natural wet-bulb head: a wetted-wick sensor on a water reservoir, the same 150 mm globe and a
       passive naturally ventilated shield; WBGT is computed from the three instruments as ISO 7243 defines
       it, with no anemometer, fan or wind model.

Both options share the clamp, the arm, the FieldNode core and its pole adapter, so what differs is the head.
Every part is a cad_parts.part() dict: made (cut, bent, drilled or printed), bought, fastener or context (the
existing pole). BOM line numbers are given on the made and bought parts of option A. The FieldNode core is
an envelope taken from FND-DWG-001 Rev P3 (its board, cell, panel and bracket are appearance stand-ins for
parts defined in the FieldNode repo); it is built to the FieldNode build plan FND-BLD-001 in that repo. The
same PARAMS feed docs/04-calcs/sizing.py (HMN-CAL-001), the drawing HMN-DWG-001 (cad/src/sheets.py), the
concept media (cad/src/concept_media.py) and the build plan pictures (cad/src/build_plan_media.py).
"""
from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

import build123d as b  # noqa: E402
import cad_parts as cp  # noqa: E402
from cad_parts import part, at  # noqa: E402
from hmn_geom import (box, zcyl, rod, fuse, path, hexnut, ring_band, band_path, nut_local, pan_screw,  # noqa: E402,F401
                      button_screw, brk)

TITLE = "HeatMap Node"

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # site interface: existing round pole (design case 114.3 mm OD, 4 in nominal); fit range
    "pole_od": 114.3, "pole_range": (60.0, 200.0), "pole_h": 4000.0,   # shown height only
    # 8 arm clamp (HMN-DDR-003): 3 mm aluminium sheet formed into a channel; web (Y) x height (Z)
    #   x depth (X); the top and bottom flanges carry 120 deg V notches lined with rubber edge trim
    "saddle": (120.0, 180.0, 40.0), "saddle_wall": 3.0, "v_angle": 120.0, "trim_t": 1.5,
    "notch_land": 8.0,             # metal from the notch apex to the outer face of the web
    "band_w": 13.0, "band_t": 0.8, "band_dz": 70.0, "band_slot": (3.0, 16.0), "band_slot_y": 55.0,
    # arm cheeks: two 40 x 40 x 3 mm aluminium angles, 80 mm long, that grip the arm root
    "cheek": (40.0, 3.0, 80.0), "cheek_web_y": 35.0, "cheek_web_dz": 25.0, "cheek_bolt_x": (12.0, 32.0),
    # 7 sensor arm: 25 x 25 x 2 mm aluminium square tube; length from the web; height
    "arm_z": 2800.0, "arm_w": 25.0, "arm_t": 2.0, "arm_len": 530.0,
    # 2 radiation shield: plate diameter, count, pitch, thickness, center hole, x position, gap below arm
    #   four M5 rods on a 92 mm circle (HMN-DDR-003): two continue through the arm on spacers
    "shield_d": 110.0, "n_plates": 8, "plate_pitch": 15.0, "plate_t": 3.0, "plate_hole": 56.0,
    "shield_x": 300.0, "shield_gap": 45.0, "rod_d": 5.0, "rod_pcd": 92.0, "boss_d": 10.0,
    "hub": (22.0, 5.0), "hub_plate": 2,          # sensor hub on the third plate: outside diameter, height above it
    # 13 aspiration fan and cowl (HMN-DDR-002): 60 x 60 x 15 mm 5 V fan over a hole in the top
    #   plate, in a printed cowl (lid side x overall height) on four legs over the fan's screw holes
    "fan": (60.0, 60.0, 15.0), "fan_holes": 50.0, "cowl": (76.0, 30.0), "top_hole": 56.0,
    # 3 air temperature and humidity sensor (capsule diameter x length)
    "th_sensor": (18.0, 45.0),
    # 4 black globe: diameter, copper wall used for mass (drawn thicker), x position, gap below arm
    "globe_d": 150.0, "globe_wall": 0.4, "globe_wall_drawn": 1.5, "globe_x": 500.0, "globe_gap": 45.0,
    "hanger": (10.0, 7.0),         # M10 hollow threaded tube (lamp rod): outside and bore diameter
    # 5 globe probe: stem diameter, bead diameter
    "probe_d": 5.0, "bead_d": 10.0,
    # 6 cup anemometer: mast height above the arm top, cup radius arm, cup diameter, inset from arm tip
    "mast_h": 170.0, "mast_d": 16.0, "cup_arm": 70.0, "cup_d": 44.0, "anemo_inset": 30.0, "mast_below": 15.0,
    # 11 secondary retention lanyard (globe and shield to the arm), wire diameter
    "lanyard_d": 2.0,
    # 9 harness: lead diameter, the radius it runs up the pole at and its angle there (deg)
    "lead_d": 7.0, "tail_d": 4.0, "pole_run": (63.0, -95.0),
    # 1 FieldNode core envelope, from FND-DWG-001 Rev P3: enclosure W (X) x D (Y) x H (Z),
    #   bottom height, back plate W x H x t, panel (X x slope x t), tilt, center (y from the plate
    #   rear face, height above the enclosure bottom), whip, port and antenna positions
    "fn_enc": (150.0, 90.0, 200.0), "fn_z0": 3110.0, "fn_plate": (180.0, 320.0, 3.0), "fn_plate_drop": 40.0,
    "fn_panel": (290.0, 200.0, 17.0), "fn_tilt": 40.0, "fn_panel_c": (-73.0, 385.0),
    "fn_whip": (10.0, 190.0), "fn_ports_x": (-54.0, -22.0), "fn_ant_x": 30.0, "fn_front_row": 55.0,
    "fn_band_slot_x": 51.0, "fn_vscrew_x": 18.0,
    # FieldNode envelope detail (appearance stand-ins for FND parts): enclosure wall, lid thickness, board (X x Z x t),
    #   board stand-off height, 32700-class LiFePO4 cell (diameter x length)
    "fn_wall": 3.0, "fn_lid": 6.0, "fn_pcb": (96.0, 150.0, 1.6), "fn_standoff": 10.0, "fn_cell": (32.0, 70.0),
    # 12 HeatMap pole adapter for the FieldNode core: two printed 120 deg V-blocks (W x H x depth)
    #   at the FieldNode clamp heights (from the enclosure bottom), and strap bands
    "adapter_vblock": (110.0, 30.0, 38.0), "adapter_dz": (-20.0, 230.0), "adapter_slot": (3.5, 16.0),
    # FieldNode core turned about the pole so that its panel faces +X, the arm's direction (deg)
    "fn_azimuth": 90.0,
    # FieldNode hot-climate sun shield (FND BOM line 14): sheet (drawn), gap, low edge, top slot
    "fns_t": 1.0, "fns_gap": 15.0, "fns_low": 10.0, "fns_slot": 30.0,
    # ---- option B, direct natural wet-bulb head (HMN-OPT-001): passive shield of 6 plates, wick reservoir
    "b_n_plates": 6, "b_shield_x": 230.0,
    "b_wick_x": 370.0, "b_wick_gap": 60.0, "b_wick_rods": 68.0,       # reservoir plate x, gap below arm, rod spacing
    "b_wick_plate": (90.0, 40.0, 3.0), "b_bottle": (56.0, 100.0), "b_neck": (24.0, 18.0),   # bottle diameter x body height; neck OD x bore
    "b_sensor_d": 6.0, "b_wick_len": 28.0, "b_sleeve_d": 8.0,
}


def derived(p=PARAMS):
    """Dimensions the calc note and the drawing quote, computed from PARAMS."""
    r = p["pole_od"] / 2
    half = math.radians(p["v_angle"] / 2)
    sw, sh, sd = p["saddle"]
    trim_off = p["trim_t"] / math.sin(half)
    v_apex = r / math.sin(half)                        # apex of the contact V (on the trim) from the pole axis
    metal_apex = v_apex + trim_off                     # apex of the notch cut in the metal
    web_out = metal_apex + p["notch_land"]             # outer face of the saddle web
    arm_x0 = web_out                                   # arm root bears on the web
    arm_x1 = arm_x0 + p["arm_len"]
    arm_bot = p["arm_z"] - p["arm_w"] / 2
    arm_top = p["arm_z"] + p["arm_w"] / 2
    shield_top = arm_bot - p["shield_gap"]
    cowl_top = shield_top + p["cowl"][1]
    stack_h = (p["n_plates"] - 1) * p["plate_pitch"] + p["plate_t"]
    shield_bot = shield_top - stack_h
    globe_r = p["globe_d"] / 2
    globe_zc = arm_bot - p["globe_gap"] - globe_r
    anemo_x = arm_x1 - p["anemo_inset"]
    hub_z = arm_top + p["mast_h"]
    # adapter V-block: the V spans the whole block width at its mouth
    vw, vh, vd = p["adapter_vblock"]
    a_vdepth = vw / 2 / math.tan(half)
    plate_y0 = -(v_apex + (vd - a_vdepth))             # FieldNode back plate rear face (local frame)
    ew, ed, eh = p["fn_enc"]
    enc_back = plate_y0 - p["fn_plate"][2]
    t = math.radians(p["fn_tilt"])
    pcy = plate_y0 + p["fn_panel_c"][0]
    pcz = p["fn_z0"] + p["fn_panel_c"][1]
    halfp = p["fn_panel"][1] / 2
    rmax = p["pole_range"][1] / 2
    b_shield_top = shield_top
    return {
        "r": r, "arm_x0": arm_x0, "arm_x1": arm_x1, "arm_bot": arm_bot, "arm_top": arm_top,
        "v_apex": v_apex, "metal_apex": metal_apex, "web_out": web_out, "web_in": web_out - p["saddle_wall"],
        "flange_edge": web_out - sd,
        "notch_half": (metal_apex - (web_out - sd)) * math.tan(half),      # half-width of the notch at the flange edge
        "shield_top": shield_top, "cowl_top": cowl_top, "shield_bot": shield_bot, "shield_zc": (shield_top + shield_bot) / 2,
        "stack_h": stack_h, "globe_zc": globe_zc, "globe_bot": globe_zc - globe_r, "globe_top": globe_zc + globe_r,
        "anemo_x": anemo_x, "hub_z": hub_z, "cup_z": hub_z + 10,
        "reach": anemo_x + p["cup_arm"] + p["cup_d"] / 2,       # farthest point from the pole axis
        "plate_y0": plate_y0, "enc_back": enc_back, "enc_front": enc_back - ed, "enc_yc": enc_back - ed / 2,
        "a_vdepth": a_vdepth, "a_mouth": plate_y0 + vd,
        "fn_top": pcz + halfp * math.sin(t) + p["fn_panel"][2] / 2,
        "panel_cy": pcy, "panel_cz": pcz,
        "panel_front_y": pcy - halfp * math.cos(t),
        # FieldNode panel in world axes after the fn_azimuth turn (90 deg: old -y becomes +x)
        "panel_cx_w": -pcy, "panel_front_x_w": -(pcy - halfp * math.cos(t)),
        "panel_low_z": pcz - halfp * math.sin(t), "panel_high_z": pcz + halfp * math.sin(t),
        "overall_top": hub_z + p["cup_d"] / 2 + 10,
        # a pole of radius R touches a 120 deg V at +/- R cos(half angle)... from its center line
        "v_contact_max": rmax * math.cos(half) * 2,
        # option B
        "b_shield_top": b_shield_top,
        "b_shield_bot": b_shield_top - ((p["b_n_plates"] - 1) * p["plate_pitch"] + p["plate_t"]),
        "sensor_zc": shield_top - 54.0,
        "b_wick_zp": arm_bot - p["b_wick_gap"],
    }


OPTIONS = {"A": "Fan-aspirated shield, globe and anemometer", "B": "Direct natural wet-bulb head"}
PRINCIPLES = {
    "A": "A fan draws air past the humidity sensor inside a white plate shield every 3 min, a 150 mm black globe and a "
         "cup anemometer give radiant heat and wind, and a model derives mean radiant temperature and WBGT.",
    "B": "A wetted-wick sensor on a small water reservoir measures the natural wet bulb directly, beside the same "
         "150 mm globe and a passive shield, so WBGT is computed as ISO 7243 defines it with no wind input.",
}
CHOSEN = "A"
OPTION_VIEWS = {k: {"el": 18, "az": -50, "scale": "person", "keep_context": True, "ground_z": 0} for k in OPTIONS}
ALLOWED_CONTACTS = []

HARNESS_RUN = {}   # filled by the harness builder: mm of lead from each core port to the arm sensors (before the sensor tails)

ST, AL, WH, BLK, BR, SS = "stainless", "aluminium", "pe_tank_white", "matte_black", "brass", "stainless"


# ----------------------------------------------------------------------------------------------- helpers
def _fs(items, origin, rot, group, prefix="", material=SS, kind="fastener", bom=None):
    """Place a list of (name, shape) fastener items (cad_parts.hex_bolt_set and others) as part dicts."""
    return [part(prefix + n, at(s, origin, rot), material, kind=kind, group=group, bom=bom) for n, s in items]


def _shs_x(x0, x1, z, a, t):
    """Square hollow section along +X from x0 to x1 with its axis at height z."""
    return at(cp.shs(a, t, x1 - x0), (x0, 0, z), (0, 90, 0))


def pole_context(p=PARAMS, z_lo=0.0, z_hi=None):
    """Existing street pole (not supplied, not in the BOM)."""
    z_hi = p["pole_h"] if z_hi is None else z_hi
    return zcyl(0, 0, (z_lo + z_hi) / 2, p["pole_od"] / 2, z_hi - z_lo)


# ----------------------------------------------------------------------------------------------- shared: clamp and arm
def clamp_parts(p, D):
    """Line 8: formed saddle, rubber trim, cheeks, strap bands and their buckles, with the clamp fixings (line 10)."""
    r, az, half = D["r"], p["arm_z"], math.radians(p["v_angle"] / 2)
    sw, sh, sd = p["saddle"]
    wt = p["saddle_wall"]
    wo, wi, fe = D["web_out"], D["web_in"], D["flange_edge"]
    out = []
    web = box(wo - wt / 2, 0, az, wt, sw, sh)
    flanges = fuse(box((wi + fe) / 2, 0, az + s * (sh / 2 - wt / 2), wi - fe, sw, wt) for s in (-1, 1))
    ma = D["metal_apex"]
    span = (ma - fe) + 2
    notch = b.extrude(b.Polygon((ma, 0), (fe - 2, span * math.tan(half)), (fe - 2, -span * math.tan(half)), align=None),
                      amount=sh + 20, both=True)
    notch = b.Pos(0, 0, az) * notch
    saddle = web + flanges - notch
    sx_, sz_ = p["band_slot"]
    for s in (-1, 1):
        for dz in (-p["band_dz"], p["band_dz"]):
            saddle = saddle - box(wo - wt / 2, s * p["band_slot_y"], az + dz, wt + 2, sx_, sz_)
        for dz in (-p["cheek_web_dz"], p["cheek_web_dz"]):
            saddle = saddle - b.Pos(wo - wt / 2, s * p["cheek_web_y"], az + dz) * b.Rot(0, 90, 0) * b.Cylinder(3.3, wt + 2)
    out.append(part("Arm saddle (3 mm sheet channel)", saddle, AL, "made", 8, "saddle"))

    tt, va = p["trim_t"], D["v_apex"]
    for s, nm in ((1, "top"), (-1, "bottom")):
        zf = az + s * (sh / 2 - wt / 2)
        poly = b.Polygon((ma, 0), (fe, (ma - fe) * math.tan(half)), (fe, (ma - fe) * math.tan(half) - tt / math.cos(half)),
                         (va, 0), (fe, -(ma - fe) * math.tan(half) + tt / math.cos(half)), (fe, -(ma - fe) * math.tan(half)), align=None)
        out.append(part(f"EPDM edge trim, {nm} flange", b.Pos(0, 0, zf) * b.extrude(poly, amount=3.0, both=True), "epdm", "bought", 8, "trim"))

    cl, ct, ch = p["cheek"]
    aw = p["arm_w"]
    for s, nm in ((1, "+Y"), (-1, "-Y")):
        flat = box(wo + ct / 2, s * (aw / 2 + cl / 2), az, ct, cl, ch)
        up = box(wo + cl / 2, s * (aw / 2 + ct / 2), az, cl, ct, ch)
        c = flat + up
        for dz in (-p["cheek_web_dz"], p["cheek_web_dz"]):
            c = c - b.Pos(wo + ct / 2, s * p["cheek_web_y"], az + dz) * b.Rot(0, 90, 0) * b.Cylinder(3.3, ct + 2)
        for bx in p["cheek_bolt_x"]:
            c = c - b.Pos(wo + bx, s * (aw / 2 + ct / 2), az) * b.Rot(90, 0, 0) * b.Cylinder(3.3, ct + 2)
        out.append(part(f"Arm cheek {nm} (40 x 40 x 3 angle)", c, AL, "made", 8, "cheeks"))

    bt = p["band_t"]
    for k, dz in enumerate((-p["band_dz"], p["band_dz"])):
        pts = band_path(r + bt / 2 + 0.1, p["band_slot_y"], wi - 2, wo + bt / 2, wo + bt / 2)
        out.append(part(f"Saddle strap band {k + 1} (13 mm)", ring_band(pts, p["band_w"], bt, az + dz), SS, "bought", 8, "bands"))
        out.append(part(f"Saddle band buckle {k + 1}", brk(box(wo + bt + 3.0, 0, az + dz, 6.0, 30.0, 16.0), 1.2), SS, "bought", 8, "bands"))

    # fixings (line 10): crush sleeves, two M6 cheek bolts through the arm, four M6 button screws with nyloc nuts
    for bx in p["cheek_bolt_x"]:
        sl = b.Pos(0, 0, 0) * (b.Cylinder(4.0, aw - 2 * p["arm_t"]) - b.Cylinder(3.2, aw))
        out.append(part("Crush sleeve 8 x 0.8 mm", at(sl, (wo + bx, 0, az), (90, 0, 0)), AL, "fastener", None, "sleeves"))
        grip = 2 * ct + aw
        out += _fs(cp.hex_bolt_set(6, grip), (wo + bx, grip / 2, az), (-90, 0, 0), "clamp_bolts", "Cheek bolt: ")
    for s in (-1, 1):
        for dz in (-p["cheek_web_dz"], p["cheek_web_dz"]):
            y_, z_ = s * p["cheek_web_y"], az + dz
            out.append(part("M6 x 20 button-head screw (ISO 7380)", at(button_screw(6, 20), (wi, y_, z_), (0, -90, 0)), SS, "fastener", None, "clamp_bolts"))
            out.append(part("M6 washer (ISO 7089)", at(cp.washer(6), (wo + ct, y_, z_), (0, 90, 0)), SS, "fastener", None, "clamp_bolts"))
            out.append(part("M6 nyloc nut (ISO 10511)", at(nut_local(10, 6.0, 6.0, "nyloc"), (wo + ct + 1.6, y_, z_), (0, 90, 0)), SS, "fastener", None, "clamp_bolts"))
    return out


def arm_parts(p, D, vertical_holes, cross_holes=()):
    """Line 7: the 25 x 25 x 2 mm square tube, drilled; and its end plug (line 10)."""
    az, aw, at_ = p["arm_z"], p["arm_w"], p["arm_t"]
    x0, x1 = D["arm_x0"], D["arm_x1"]
    arm = _shs_x(x0, x1, az, aw, at_)
    for xx, d in vertical_holes:
        arm = arm - zcyl(xx, 0, az, d / 2, aw + 4)
    for bx in p["cheek_bolt_x"]:
        arm = arm - b.Pos(x0 + bx, 0, az) * b.Rot(90, 0, 0) * b.Cylinder(3.3, aw + 4)
    for xx, d in cross_holes:
        arm = arm - b.Pos(xx, 0, az) * b.Rot(90, 0, 0) * b.Cylinder(d / 2, aw + 4)
    out = [part("Sensor arm (25 x 25 x 2 SHS)", arm, AL, "made", 7, "arm")]
    plug = at(b.extrude(b.Sketch() + b.RectangleRounded(aw - 2 * at_ - 0.4, aw - 2 * at_ - 0.4, 1.8), 12), (x1 - 12, 0, az), (0, 90, 0))
    plug = plug + at(brk(b.extrude(b.Sketch() + b.RectangleRounded(aw, aw, 4.0), 2.5), 0.6), (x1, 0, az), (0, 90, 0))
    out.append(part("Arm end plug", plug, "hdpe_black", "bought", 10, "plug"))
    return out


# ----------------------------------------------------------------------------------------------- shared: shield stack
def shield_parts(p, D, n_plates, sx, fan=True, ST_=None):
    """Line 2: the stack of white plates on four M5 rods; two rods continue through the arm on spacers."""
    out = []
    az = p["arm_z"]
    pt, pitch = p["plate_t"], p["plate_pitch"]
    st = D["shield_top"] if ST_ is None else ST_
    sr = p["shield_d"] / 2
    rr = p["rod_pcd"] / 2
    rods_xy = [(sx + rr * math.cos(math.radians(a)), rr * math.sin(math.radians(a))) for a in (0, 90, 180, 270)]
    fh = p["fan_holes"] / 2
    for i in range(n_plates):
        z = st - pt / 2 - i * pitch
        hole = (p["top_hole"] if fan else 0) if i == 0 else p["plate_hole"]
        pl = zcyl(sx, 0, z, sr, pt)
        if hole:
            pl = pl - zcyl(sx, 0, z, hole / 2, pt + 2)
        if i == p["hub_plate"]:      # sensor hub on three spokes
            hd, hh = p["hub"]
            pl = pl + zcyl(sx, 0, z - pt / 2 + (pt + hh) / 2, hd / 2, pt + hh)
            for a in (30, 150, 270):
                ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
                mid = (hd / 2 + p["plate_hole"] / 2) / 2
                pl = pl + b.Pos(sx + mid * ca, mid * sa, z) * b.Rot(0, 0, a) * b.Box(p["plate_hole"] / 2 - hd / 2 + 2, 4, pt)
            pl = pl - zcyl(sx, 0, z, (p["th_sensor"][0] + 0.5) / 2, pt + 2 * hh + 4)
        if i > 0:                    # bosses that carry the plate above
            for (rx, ry) in rods_xy:
                pl = pl + zcyl(rx, ry, z + pt / 2 + (pitch - pt) / 2, p["boss_d"] / 2, pitch - pt)
        for (rx, ry) in rods_xy:
            pl = pl - zcyl(rx, ry, z, 2.75, pitch * 2 + 2)
        if i == 0 and fan:
            for ex in (-1, 1):
                for ey in (-1, 1):
                    pl = pl - zcyl(sx + ex * fh, ey * fh, z, 2.2, pt + 2)
        out.append(part(f"Shield plate {i + 1} (110 mm, white ASA)", pl, WH, "made", 2, "plates"))
    sb = st - ((n_plates - 1) * pitch + pt)
    long_top = D["arm_top"] + 4 + 4
    for k, (rx, ry) in enumerate(rods_xy):
        is_long = abs(ry) < 1
        top = long_top if is_long else st + 4 + 3
        rd = zcyl(rx, ry, (sb - 6 + top) / 2, p["rod_d"] / 2, top - (sb - 6))
        out.append(part(f"M5 threaded rod {k + 1} (316)", brk(rd, 0.4), SS, "fastener", None, "rods"))
        out.append(part("M5 acorn nut (DIN 1587)", at(nut_local(8, 8.0, 5.0, "acorn"), (rx, ry, sb), (180, 0, 0)), SS, "fastener", None, "rods"))
        out.append(part("M5 hex nut (ISO 4032)", at(nut_local(8, 4.0, 5.0), (rx, ry, st), (0, 0, 0)), SS, "fastener", None, "rods"))
        if is_long:
            out.append(part("M5 hex nut above the arm (ISO 4032)", at(nut_local(8, 4.0, 5.0), (rx, ry, D["arm_top"]), (0, 0, 0)), SS, "fastener", None, "rods"))
            sp = zcyl(rx, ry, (st + 4 + D["arm_bot"]) / 2, 4.0, D["arm_bot"] - st - 4) - zcyl(rx, ry, 0, 2.65, 1e5)
            out.append(part("Shield spacer 8 x 0.8 mm tube", sp, AL, "made", 2, "spacers"))
    return out


def fan_parts(p, D, sx):
    """Line 13: 60 mm fan, cowl and four M4 screws with nuts."""
    out = []
    st = D["shield_top"]
    pt = p["plate_t"]
    fw, _, fht = p["fan"]
    cw, chh = p["cowl"]
    fh = p["fan_holes"] / 2
    fan = box(sx, 0, st + fht / 2, fw, fw, fht) - zcyl(sx, 0, st + fht / 2, fw / 2 - 2, fht + 2)
    fan = fan + zcyl(sx, 0, st + fht / 2, 12, fht - 2)
    for a in (0, 120, 240):
        fan = fan + b.Pos(sx, 0, st + fht / 2) * b.Rot(0, 0, a) * b.Pos(20, 0, 0) * b.Box(17, 3, 2)
    for ex in (-1, 1):
        for ey in (-1, 1):
            fan = fan - zcyl(sx + ex * fh, ey * fh, st + fht / 2, 2.2, fht + 2)
    out.append(part("Aspiration fan 60 x 60 x 15 mm, 5 V", fan, "hdpe_black", "bought", 13, "fan"))
    lid_t, leg = 3.0, 8.0
    cowl = box(sx, 0, st + chh - lid_t / 2, cw, cw, lid_t)
    for ex in (-1, 1):
        for ey in (-1, 1):
            cowl = cowl + box(sx + ex * fh, ey * fh, st + fht + (chh - lid_t - fht) / 2, leg, leg, chh - lid_t - fht)
            cowl = cowl - zcyl(sx + ex * fh, ey * fh, st + chh / 2, 2.2, chh + 2)
    out.append(part("Fan cowl (white ASA)", cowl, WH, "made", 13, "cowl"))
    for ex in (-1, 1):
        for ey in (-1, 1):
            x_, y_ = sx + ex * fh, ey * fh
            out.append(part("M4 x 37 pan-head screw", at(pan_screw(4, chh + pt + 4), (x_, y_, st + chh), (0, 0, 0)), SS, "fastener", None, "fan_screws"))
            out.append(part("M4 hex nut (ISO 4032)", at(nut_local(7, 3.2, 4.0), (x_, y_, st - pt), (180, 0, 0)), SS, "fastener", None, "fan_screws"))
    return out


def sensor_parts(p, D, sx):
    """Line 3: SHT45 board in a capsule with a PTFE membrane cap, seated in the hub of the third plate."""
    cd, cln = p["th_sensor"]
    zc = D["sensor_zc"]
    wall = 1.5
    cap = b.Pos(sx, 0, zc) * (b.Cylinder(cd / 2, cln) - b.Pos(0, 0, -wall) * b.Cylinder(cd / 2 - wall, cln))
    cap = brk(cap, 1.0)
    pcb = box(sx, 0, zc + 6.5, 9.0, 1.6, 29.0)
    memb = zcyl(sx, 0, zc - cln / 2 + 0.75, cd / 2 - wall - 0.1, 1.5)
    return [part("Sensor capsule (SHT45 housing)", cap, WH, "bought", 3, "th_sensor"),
            part("SHT45 board", pcb, "polycarbonate", "bought", 3, "th_sensor", color="#166534"),
            part("PTFE membrane cap", memb, "label", "bought", 3, "th_sensor")]


def globe_parts(p, D, gx):
    """Lines 4 and 5: copper globe on its M10 hanger tube with three nuts; probe stem and bead."""
    out = []
    gz, gr = D["globe_zc"], p["globe_d"] / 2
    ho, hb = p["hanger"]
    gt = D["globe_top"]
    az = p["arm_z"]
    globe = b.Pos(gx, 0, gz) * (b.Sphere(gr) - b.Sphere(gr - p["globe_wall_drawn"]))
    globe = globe + zcyl(gx, 0, gt + 4, 10, 16)
    globe = globe - zcyl(gx, 0, gt, ho / 2 + 0.1, 40)
    out.append(part("Black globe 150 mm (copper float ball, painted)", globe, BLK, "bought", 4, "globe"))
    h_bot, h_top = gt - 2, D["arm_top"] + 8 + 6
    hanger = zcyl(gx, 0, (h_bot + h_top) / 2, ho / 2, h_top - h_bot) - zcyl(gx, 0, (h_bot + h_top) / 2, hb / 2, h_top - h_bot + 2)
    out.append(part("Globe hanger tube (M10 lamp rod)", brk(hanger, 0.5), BR, "bought", 4, "hanger"))
    for nm, z0, ax_ in (("on the globe boss", gt + 12, "z"), ("under the arm", D["arm_bot"], "-z"), ("above the arm", D["arm_top"], "z")):
        out.append(part(f"M10 brass nut {nm}", hexnut(gx, 0, z0, 17, 8, ho, axis=ax_), BR, "fastener", None, "hanger"))
    # probe: 5 mm stiff tube and a 10 mm epoxy bead at the globe centre
    stem_bot = gz + p["bead_d"] / 2 - 0.5
    stem = zcyl(gx, 0, (stem_bot + h_top + 4) / 2, p["probe_d"] / 2, h_top + 4 - stem_bot) - zcyl(gx, 0, (stem_bot + h_top + 4) / 2, p["probe_d"] / 2 - 0.6, h_top + 6 - stem_bot)
    out.append(part("Globe probe stem (5 mm tube)", brk(stem, 0.3), SS, "bought", 5, "probe"))
    out.append(part("NTC bead thermistor 10k (epoxy)", b.Pos(gx, 0, gz) * b.Sphere(p["bead_d"] / 2), "hdpe_recycled", "bought", 5, "probe", color="#7A4B2A"))
    return out, h_top


def lanyard_parts(p, D, sx, gx):
    """Line 11: two 2 mm stainless lanyards looped round the arm, to the shield top and the globe boss."""
    az = p["arm_z"]
    ld = p["lanyard_d"] / 2
    st = D["shield_top"]
    gt = D["globe_top"]

    def loop(xl):
        return [(xl, 14, az - 14), (xl, 14, az + 14), (xl, -25, az + 14), (xl, -25, az - 14), (xl, 14, az - 14)]
    l1 = path([(sx - 30, 42, st), (sx - 30, 42, st + 30), (sx - 30, 14, az - 14)] + loop(sx - 30)[1:], ld)
    l2 = path([(gx + 11, 0, gt + 6), (gx + 30, 14, D["arm_bot"] - 14), (gx + 30, 14, az - 14)] + loop(gx + 30)[1:], ld)
    return [part("Retention lanyard, shield top to arm", l1, SS, "bought", 11, "lanyard"),
            part("Retention lanyard, globe boss to arm", l2, SS, "bought", 11, "lanyard")]


# ----------------------------------------------------------------------------------------------- shared: harness
def harness_parts(p, D, sx, gx, h_top, tails_b):
    """Line 9: two M12 leads from the FieldNode ports down the pole and along the arm, with M12 plugs.
    Lead A feeds the T and RH sensor; lead B the globe probe and the extra sensors in `tails_b`
    (list of point lists, each starting on the lead's end point (x, -19.5, arm_z + dz) is added here)."""
    az = p["arm_z"]
    z0 = p["fn_z0"]
    yrow = D["enc_back"] - p["fn_front_row"]
    st = D["shield_top"]
    ld_, td = p["lead_d"] / 2, p["tail_d"] / 2
    rr_, ang = p["pole_run"]
    out = []
    plug_h = 28.0
    for k, (px, dzl, dang) in enumerate(((p["fn_ports_x"][0], 5.0, -6.0), (p["fn_ports_x"][1], -5.0, 6.0))):
        wx, wy = -yrow, px          # port after the 90 deg turn: (x, y) -> (-y, x)
        a = math.radians(ang + dang)
        prx, pry = rr_ * math.cos(a), rr_ * math.sin(a)
        zlow = z0 - 70 - 10 * k
        zbk = az + 97 + 8 * k       # lead B runs above lead A where they leave the pole, so neither crosses the other
        pts = [(wx, wy, z0 - 16 - plug_h), (wx, wy, zlow), (60, -80 - 8 * k, zlow), (prx, pry, zlow), (prx, pry, zbk),
               (45, -82 - 8 * k, zbk), (90, -64 - 8 * k, zbk), (90, -64 - 8 * k, az + dzl), (125, -27, az + dzl), (140, -19.5, az + dzl)]
        if k == 0:
            pts += [(sx + 60, -19.5, az + dzl)]
            lead = path(pts, ld_)
            tail = [(sx + 60, -19.5, az + dzl), (sx + 44, -44, az - 25), (sx + 44, -44, st - 21), (sx, 0, st - 21),
                    (sx, 0, D["sensor_zc"] + p["th_sensor"][1] / 2)]
            lead = lead + path(tail, td)
            nm = "Sensor lead A (T and RH sensor, fan), M12"
        else:
            end_x = max(t[0][0] for t in tails_b)
            pts += [(end_x, -19.5, az + dzl)]
            lead = path(pts, ld_)
            for tl in tails_b:
                lead = lead + path(tl, td)
            nm = "Sensor lead B (globe probe, second sensor), M12"
        HARNESS_RUN[k] = sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
        out.append(part(nm, lead, "hdpe_black", "bought", 9, "harness"))
        plug = brk(zcyl(wx, wy, z0 - 16 - plug_h / 2, 8.0, plug_h), 1.5)
        out.append(part(f"M12 5-pin plug {k + 1}", plug, "zinc_plated", "bought", 9, "harness"))
    return out


# ----------------------------------------------------------------------------------------------- shared: FieldNode core and adapter
def fieldnode_parts(p, D):
    """Line 1: the FieldNode core as an envelope of its main parts (FND-DWG-001 Rev P3), turned onto the pole's +X face."""
    out = []
    turn = b.Rot(0, 0, p["fn_azimuth"])
    ew, ed, eh = p["fn_enc"]
    z0 = p["fn_z0"]
    pw, ph, ptk = p["fn_plate"]
    y0 = D["plate_y0"]
    wall, lid_t = p["fn_wall"], p["fn_lid"]
    add = lambda nm, sh, mat, grp="fieldnode", **kw: out.append(part(nm, turn * sh, mat, kw.pop("kind", "bought"), 1, grp, **kw))

    # back plate with its band slots and countersunk V-block screw holes
    plate = box(0, y0 - ptk / 2, z0 - p["fn_plate_drop"] + ph / 2, pw, ptk, ph)
    for dz in p["adapter_dz"]:
        for s in (-1, 1):
            plate = plate - box(s * p["fn_band_slot_x"], y0 - ptk / 2, z0 + dz, 3.0, ptk + 2, 15.0)
            plate = plate - b.Pos(s * p["fn_vscrew_x"], y0 - ptk / 2, z0 + dz) * b.Rot(90, 0, 0) * b.Cylinder(2.25, ptk + 2)
            plate = plate - b.Pos(s * p["fn_vscrew_x"], y0 - ptk + 1.2, z0 + dz) * b.Rot(90, 0, 0) * b.Cone(2.2, 4.4, 2.4)
    add("FieldNode back plate (3 mm, slotted)", plate, AL, "fieldnode", kind="made")

    # enclosure body (open to the front), lid
    body_d = ed - lid_t
    body_c = D["enc_back"] - body_d / 2
    body = box(0, body_c, z0 + eh / 2, ew, body_d, eh) - box(0, body_c - wall / 2 - 0.5, z0 + eh / 2, ew - 2 * wall, body_d - wall + 1.0, eh - 2 * wall)
    add("FieldNode enclosure IP65 (150 x 90 x 200)", brk(body, 1.0), WH, "fieldnode", kind="made")
    add("FieldNode enclosure lid", brk(box(0, D["enc_front"] + lid_t / 2, z0 + eh / 2, ew, lid_t, eh), 1.5), WH, "fieldnode", kind="made")

    # board on four stand-offs, with four screws; cell
    pw_, ph_, pt_ = p["fn_pcb"]
    zc = z0 + eh / 2
    y_in = D["enc_back"] - wall                    # inside face of the back wall
    so = p["fn_standoff"]
    y_pcb = y_in - so - pt_ / 2
    holes = [(sx_ * (pw_ / 2 - 5), sz_ * (ph_ / 2 - 5)) for sx_ in (-1, 1) for sz_ in (-1, 1)]
    pcb = box(0, y_pcb, zc, pw_, pt_, ph_)
    for hx, hz in holes:
        pcb = pcb - b.Pos(hx, y_pcb, zc + hz) * b.Rot(90, 0, 0) * b.Cylinder(1.7, pt_ + 2)
    pcb = pcb + box(-20, y_pcb - pt_ / 2 - 1.5, zc + 35, 22, 3, 22) + box(24, y_pcb - pt_ / 2 - 3, zc - 25, 30, 6, 20) + box(0, y_pcb - pt_ / 2 - 1, zc - 55, 40, 2, 14)
    add("FieldNode board (MPPT and LoRaWAN module, stand-in)", pcb, "polycarbonate", "fieldnode", kind="bought", color="#166534")
    for hx, hz in holes:
        so_ = b.Pos(hx, y_in - so / 2, zc + hz) * b.Rot(90, 0, 0) * (b.Cylinder(2.75, so) - b.Pos(0, 0, so / 2 - 3.5) * b.Cylinder(1.5, 7.2))
        out.append(part("M3 brass stand-off 10 mm", turn * so_, BR, "fastener", None, "fieldnode"))
        scr = b.Pos(hx, y_pcb - pt_ / 2, zc + hz) * b.Rot(90, 0, 0) * pan_screw(3, 7.6)
        out.append(part("M3 x 8 pan-head board screw", turn * scr, SS, "fastener", None, "fieldnode"))
    cd, cl = p["fn_cell"]
    cell = b.Pos(0, y_pcb - 22, z0 + wall + cd / 2) * b.Rot(0, 90, 0) * b.Cylinder(cd / 2, cl)
    add("LiFePO4 cell 3.2 V 6 Ah (stand-in)", brk(cell, 1.0), "glass", "fieldnode", kind="bought", color="#2F5F8A")

    # ports, antenna
    yrow = D["enc_back"] - p["fn_front_row"]
    for k, x in enumerate(p["fn_ports_x"]):
        sock = zcyl(x, yrow, z0 - 2, 11.0, 4.0) + zcyl(x, yrow, z0 - 10, 8.0, 12.0)
        add(f"M12 5-pin socket {'AB'[k]}", brk(sock, 0.6), "zinc_plated", "fieldnode", kind="bought")
    wd, wl = p["fn_whip"]
    ax = p["fn_ant_x"]
    add("Antenna base (SMA)", brk(zcyl(ax, yrow, z0 - 10, 7.0, 20.0), 1.0), "zinc_plated", "fieldnode", kind="bought")
    add("Antenna whip (LoRa, 868 and 915 MHz)", brk(zcyl(ax, yrow, z0 - 20 - (wl - 20) / 2, wd / 2, wl - 20), 1.0), "hdpe_black", "fieldnode", kind="bought")

    # solar panel on its bracket
    tilt = p["fn_tilt"]
    t = math.radians(tilt)
    pcy, pcz = D["panel_cy"], D["panel_cz"]
    pwid, plen, pth = p["fn_panel"]
    ring = b.Box(pwid, plen, pth) - b.Box(pwid - 6, plen - 6, pth + 2)
    frame = b.Pos(0, pcy, pcz) * b.Rot(tilt, 0, 0) * ring
    lam = b.Pos(0, pcy, pcz) * b.Rot(tilt, 0, 0) * b.Pos(0, 0, pth / 2 - 2.5) * b.Box(pwid - 6.2, plen - 6.2, 5.0)
    back = b.Pos(0, pcy, pcz) * b.Rot(tilt, 0, 0) * b.Pos(0, 0, -pth / 2 + 1.0) * b.Box(pwid - 6.2, plen - 6.2, 2.0)
    add("Solar panel frame (6 W, 290 x 200 x 17)", brk(frame, 0.8), AL, "fieldnode", kind="bought")
    add("Solar panel laminate", lam, "glass", "fieldnode", kind="bought", color="#1B2A44")
    add("Solar panel back sheet", back, "hdpe_black", "fieldnode", kind="bought")
    panel_solid = b.Pos(0, pcy, pcz) * b.Rot(tilt, 0, 0) * b.Box(pwid, plen, pth)
    plate_solid = box(0, y0 - ptk / 2, z0 - p["fn_plate_drop"] + ph / 2, pw, ptk, ph)
    for bi, (zs, off) in enumerate(((260, 80), (210, -60))):
        for bx in (-80, 80):
            a_ = (bx, y0 - ptk + 6, z0 + zs)
            c_ = (bx, pcy + off * math.cos(t), pcz + off * math.sin(t) - 10)
            dv = (c_[0] - a_[0], c_[1] - a_[1], c_[2] - a_[2])
            dl = math.sqrt(sum(v * v for v in dv))
            c_ = tuple(c_[i] + dv[i] / dl * 8.0 for i in range(3))     # run into the panel; the panel is then cut away
            bar = rod(a_, c_, 5.0) - panel_solid - plate_solid
            add(f"Panel bracket arm {bi * 2 + (1 if bx > 0 else 0) + 1} (10 mm bar)", bar, AL, "fieldnode", kind="made")

    # hot-climate sun shield (FND BOM line 14)
    fst, sg = p["fns_t"], p["fns_gap"]
    yb_s = y0 - ptk
    yf_s = D["enc_front"] - sg
    xo = ew / 2 + sg
    zlo, zhi = z0 + p["fns_low"], z0 + eh + sg
    hs = zhi - zlo
    fshield = box(0, yf_s - fst / 2, zlo + hs / 2, 2 * (xo + fst), fst, hs)
    for sxn in (-1, 1):
        fshield = fshield + box(sxn * (xo + fst / 2), (yb_s + yf_s - fst) / 2, zlo + hs / 2, fst, yb_s - (yf_s - fst), hs)
    fshield = fshield + box(0, (yf_s - fst + yb_s - p["fns_slot"]) / 2, zhi + fst / 2, 2 * (xo + fst), yb_s - p["fns_slot"] - (yf_s - fst), fst)
    add("FieldNode sun shield (1 mm sheet)", fshield, AL, "fieldnode", kind="made", color="#F2F2EE")
    return out


def adapter_parts(p, D):
    """Line 12: two printed 120 degree V-blocks, four countersunk M4 screws, two strap bands with buckles."""
    out = []
    r = D["r"]
    half = math.radians(p["v_angle"] / 2)
    z0 = p["fn_z0"]
    y0 = D["plate_y0"]
    ptk = p["fn_plate"][2]
    bt = p["band_t"]
    vw, vh, vd = p["adapter_vblock"]
    turn = b.Rot(0, 0, p["fn_azimuth"])
    va_d = D["a_vdepth"]
    for k, dz in enumerate(p["adapter_dz"]):
        z = z0 + dz
        blk = box(0, y0 + vd / 2, z, vw, vd, vh)
        mouth = y0 + vd
        vcut = b.extrude(b.Polygon((0, mouth - va_d), (vw / 2 + 2, mouth + 2 / math.tan(half)), (-vw / 2 - 2, mouth + 2 / math.tan(half)), align=None),
                         amount=vh + 4, both=True)
        blk = blk - b.Pos(0, 0, z) * vcut
        sxa, sza = p["adapter_slot"]
        for s in (-1, 1):
            blk = blk - box(s * p["fn_band_slot_x"], y0 + vd / 2, z, sxa, vd + 2, sza)
            blk = blk - b.Pos(s * p["fn_vscrew_x"], y0 + 6, z) * b.Rot(90, 0, 0) * b.Cylinder(2.1, 12)
        out.append(part(f"Adapter V-block {k + 1} (120 deg, ASA)", turn * blk, WH, "made", 12, "vblocks", color="#3A3F45"))
        for s in (-1, 1):
            scr = b.Pos(s * p["fn_vscrew_x"], y0 - ptk, z) * b.Rot(90, 0, 0) * _csk_screw(4, 13)
            out.append(part("M4 x 13 countersunk screw (ISO 10642)", turn * scr, SS, "fastener", None, "ascrews"))
        pts = band_path(r + bt / 2 + 0.1, p["fn_band_slot_x"], -(mouth + 4), -(y0 - ptk - bt / 2), -(y0 - ptk - bt / 2))
        bd = b.Rot(0, 0, -90) * ring_band(pts, p["band_w"], bt, z)
        out.append(part(f"Adapter strap band {k + 1} (13 mm)", turn * bd, SS, "bought", 12, "abands"))
        bk = box(0, y0 - ptk - bt - 3.0, z, 30.0, 6.0, 16.0)
        out.append(part(f"Adapter band buckle {k + 1}", turn * brk(bk, 1.2), SS, "bought", 12, "abands"))
    return out


def _csk_screw(d, length):
    """Countersunk screw: flat head top at z = 0 (cone down to the shank), shank to -length."""
    head = b.Pos(0, 0, -1.2) * b.Cone(d / 2, 2.1 * d / 2, 2.4)
    shank = b.Pos(0, 0, -length / 2) * b.Cylinder(d / 2, length)
    return head + shank


# ----------------------------------------------------------------------------------------------- option A
def option_a(p=PARAMS):
    D = derived(p)
    sx, gx, ax = p["shield_x"], p["globe_x"], D["anemo_x"]
    az, aw = p["arm_z"], p["arm_w"]
    x0 = D["arm_x0"]
    rr = p["rod_pcd"] / 2
    parts = clamp_parts(p, D)
    vh = [(sx - rr, 5.5), (sx + rr, 5.5), (gx, p["hanger"][0] + 0.5), (ax, p["mast_d"] + 0.5)]
    parts += arm_parts(p, D, vh, cross_holes=[(ax, 5.5)])
    parts += shield_parts(p, D, p["n_plates"], sx, fan=True)
    parts += fan_parts(p, D, sx)
    parts += sensor_parts(p, D, sx)
    gp, h_top = globe_parts(p, D, gx)
    parts += gp
    # 6 cup anemometer on its mast through the arm
    hz = D["hub_z"]
    mb = D["arm_bot"] - p["mast_below"]
    md = p["mast_d"]
    mast = zcyl(ax, 0, (mb + hz - 20) / 2, md / 2, hz - 20 - mb) - zcyl(ax, 0, (mb + hz - 20) / 2, md / 2 - 1.5, hz - mb)
    mast = mast - b.Pos(ax, 0, az) * b.Rot(90, 0, 0) * b.Cylinder(2.75, 40)
    parts.append(part("Anemometer mast (16 mm tube)", brk(mast, 0.4), AL, "bought", 6, "anemometer"))
    parts.append(part("Anemometer rotor hub", brk(zcyl(ax, 0, hz, 22, 40), 3.0), "hdpe_recycled", "bought", 6, "anemometer"))
    cr = p["cup_d"] / 2
    for a in (30, 150, 270):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        cx_, cy_ = ax + p["cup_arm"] * ca, p["cup_arm"] * sa
        end = p["cup_arm"] - cr
        parts.append(part(f"Anemometer cup arm {a} deg", brk(rod((ax + 22 * ca, sa * 22, hz + 10), (ax + end * ca, end * sa, hz + 10), 2.5), 0.4), AL, "bought", 6, "anemometer"))
        cup = b.Pos(cx_, cy_, hz + 10) * (b.Sphere(cr) - b.Sphere(cr - 2))
        cut = b.Pos(cx_ + cr * math.cos(math.radians(a + 90)), cy_ + cr * math.sin(math.radians(a + 90)), hz + 10) * b.Box(2 * cr, 2 * cr, 2.5 * cr)
        parts.append(part(f"Anemometer cup {a} deg", cup - cut, "hdpe_recycled", "bought", 6, "anemometer"))
    parts += _fs(cp.hex_bolt_set(5, aw), (ax, aw / 2, az), (-90, 0, 0), "mast_bolt", "Mast cross bolt: ")
    parts += lanyard_parts(p, D, sx, gx)
    # lead B runs to x = ax - 14; the globe tail starts at gx - 25 on the same lead
    parts += harness_parts(p, D, sx, gx, h_top, [[(ax - 14, -19.5, az - 5.0), (ax - 14, -10, mb - 8), (ax, 0, mb - 8), (ax, 0, mb + 10)],
                                                [(gx - 25, -19.5, az - 5.0), (gx - 25, -19.5, h_top + 6), (gx, 0, h_top + 6)]])
    parts += fieldnode_parts(p, D)
    parts += adapter_parts(p, D)
    return parts


# ----------------------------------------------------------------------------------------------- option B
def option_b(p=PARAMS):
    D = derived(p)
    sx, gx = p["b_shield_x"], p["globe_x"]
    wx = p["b_wick_x"]
    az, aw = p["arm_z"], p["arm_w"]
    rr = p["rod_pcd"] / 2
    parts = clamp_parts(p, D)
    wr = p["b_wick_rods"] / 2
    vh = [(sx - rr, 5.5), (sx + rr, 5.5), (gx, p["hanger"][0] + 0.5), (wx - wr, 5.5), (wx + wr, 5.5)]
    parts += arm_parts(p, D, vh)
    parts += shield_parts(p, D, p["b_n_plates"], sx, fan=False)
    parts += sensor_parts(p, D, sx)
    gp, h_top = globe_parts(p, D, gx)
    parts += gp
    # wick reservoir: plate hung from the arm on two M5 rods and spacers, bottle through the plate, cap, wick sensor
    zp = D["b_wick_zp"]
    pl_l, pl_w, pl_t = p["b_wick_plate"]
    plate = b.Pos(wx, 0, zp - pl_t / 2) * b.Box(pl_l, pl_w, pl_t)
    plate = plate - zcyl(wx, 0, zp - pl_t / 2, p["b_neck"][0] / 2 + 0.3, pl_t + 2)
    for s in (-1, 1):
        plate = plate - zcyl(wx + s * wr, 0, zp - pl_t / 2, 2.75, pl_t + 2)
    parts.append(part("Reservoir plate (3 mm aluminium)", brk(plate, 0.6), AL, "made", None, "wick"))
    for k, s in enumerate((-1, 1)):
        x_ = wx + s * wr
        top = D["arm_top"] + 8
        bot = zp - pl_t - 6
        parts.append(part(f"M5 threaded rod {k + 1} (316), reservoir", brk(zcyl(x_, 0, (bot + top) / 2, 2.5, top - bot), 0.4), SS, "fastener", None, "wick"))
        sp = zcyl(x_, 0, (zp + 4.0 + D["arm_bot"]) / 2, 4.0, D["arm_bot"] - zp - 4.0) - zcyl(x_, 0, 0, 2.65, 1e5)
        parts.append(part("Reservoir spacer 8 x 0.8 mm tube", sp, AL, "made", None, "wick"))
        parts.append(part("M5 hex nut above the arm (ISO 4032)", at(nut_local(8, 4.0, 5.0), (x_, 0, D["arm_top"]), (0, 0, 0)), SS, "fastener", None, "wick"))
        parts.append(part("M5 acorn nut under the plate", at(nut_local(8, 8.0, 5.0, "acorn"), (x_, 0, zp - pl_t), (180, 0, 0)), SS, "fastener", None, "wick"))
        parts.append(part("M5 hex nut on the plate (ISO 4032)", at(nut_local(8, 4.0, 5.0), (x_, 0, zp), (0, 0, 0)), SS, "fastener", None, "wick"))
    bd, bh = p["b_bottle"]
    nd, nb = p["b_neck"]
    zb = zp - pl_t                                   # shoulder bears on the plate underside
    shoulder = 12.0
    neck_len = pl_t + 4.0 + 9.9
    outer = (b.Pos(wx, 0, zb - shoulder - bh / 2) * b.Cylinder(bd / 2, bh)
             + b.Pos(wx, 0, zb - shoulder / 2) * b.Cone(bd / 2, nd / 2, shoulder)
             + zcyl(wx, 0, zb + neck_len / 2, nd / 2, neck_len))
    inner = (b.Pos(wx, 0, zb - shoulder - bh / 2 + 1.5) * b.Cylinder(bd / 2 - 2, bh - 3)
             + b.Pos(wx, 0, zb - shoulder / 2) * b.Cone(bd / 2 - 2, nb / 2, shoulder)
             + zcyl(wx, 0, zb + neck_len / 2, nb / 2, neck_len + 2))
    parts.append(part("Water reservoir bottle (HDPE, 56 mm)", outer - inner, "hdpe_natural", "bought", None, "wick"))
    parts.append(part("Bottle lock ring", zcyl(wx, 0, zp + 2, 17.0, 4.0) - zcyl(wx, 0, zp + 2, nd / 2 + 0.05, 5), "hdpe_black", "bought", None, "wick"))
    cap_z0, cap_h = zp + 4.0, 14.0
    cap = zcyl(wx, 0, cap_z0 + cap_h / 2, 15.0, cap_h) - zcyl(wx, 0, cap_z0 + 5.0 - 0.01, nd / 2 + 0.1, 10.02) - zcyl(wx, 0, cap_z0 + cap_h / 2, p["b_sensor_d"] / 2 + 0.1, cap_h + 2)
    parts.append(part("Reservoir cap with sensor gland", brk(cap, 0.8), "hdpe_black", "bought", None, "wick"))
    sd = p["b_sensor_d"]
    t_bot = cap_z0 + 7.0
    t_top = cap_z0 + cap_h + p["b_wick_len"] + 2.0
    parts.append(part("Wick sensor tube (6 mm, NTC inside)", brk(zcyl(wx, 0, (t_bot + t_top) / 2, sd / 2, t_top - t_bot), 0.4), SS, "bought", None, "wick"))
    s_bot, s_top = cap_z0 + cap_h, cap_z0 + cap_h + p["b_wick_len"]
    sleeve = zcyl(wx, 0, (s_bot + s_top) / 2, p["b_sleeve_d"] / 2, s_top - s_bot) - zcyl(wx, 0, (s_bot + s_top) / 2, sd / 2 + 0.1, s_top - s_bot + 2)
    parts.append(part("Cotton wick sleeve", brk(sleeve, 0.4), "label", "bought", None, "wick"))
    tail_top, tail_bot = t_bot, zb - shoulder - bh + 8
    parts.append(part("Cotton wick tail (3 mm cord)", brk(zcyl(wx, 0, (tail_top + tail_bot) / 2, 1.5, tail_top - tail_bot), 0.3), "rope", "bought", None, "wick"))
    parts += lanyard_parts(p, D, sx, gx)
    tail_w = [(wx - 45, -19.5, az - 5.0), (wx - 45, -27, az - 30), (wx - 45, -27, t_top + 7), (wx, 0, t_top + 7), (wx, 0, t_top)]
    parts += harness_parts(p, D, sx, gx, h_top, [tail_w, [(gx - 25, -19.5, az - 5.0), (gx - 25, -19.5, h_top + 6), (gx, 0, h_top + 6)]])
    parts += fieldnode_parts(p, D)
    parts += adapter_parts(p, D)
    return parts


_CACHE = {}


def components(option=CHOSEN):
    """Parts of one option as cad_parts.part() dicts, with the existing pole as context."""
    if option not in _CACHE:
        parts = {"A": option_a, "B": option_b}[option]()
        pole = part("Existing street pole (not supplied)", pole_context(PARAMS, 0.0, 3750.0), "galvanised", "context", None, "context")
        _CACHE[option] = parts + [pole]
    return list(_CACHE[option])


# ----------------------------------------------------------------------------------------------- views for the older scripts
@dataclass
class Component:
    """A group of parts under the key the drawing, concept and build-plan scripts use."""
    key: str
    name: str
    shape: object
    line: int
    kind: str
    density: float


# model key -> (BOM line, name, component keys); the keys are the `group` of the parts in option A
BOM_GROUPS = {
    "fieldnode": (1, "FieldNode core with sun shield (FND-DWG-001 envelope)", ["fieldnode"]),
    "shield": (2, "Multi-plate radiation shield", ["plates", "rods", "spacers"]),
    "th_sensor": (3, "Air temperature and humidity sensor", ["th_sensor"]),
    "globe": (4, "Black globe, 150 mm, on its hanger tube", ["globe", "hanger"]),
    "probe": (5, "Globe temperature probe", ["probe"]),
    "anemometer": (6, "Cup anemometer", ["anemometer", "mast_bolt"]),
    "arm": (7, "Sensor arm", ["arm", "plug", "sleeves"]),
    "clamp": (8, "Arm clamp: saddle, cheeks and bands", ["saddle", "trim", "cheeks", "bands", "clamp_bolts"]),
    "harness": (9, "Sensor harness, M12", ["harness"]),
    "lanyard": (11, "Secondary retention lanyards", ["lanyard"]),
    "adapter": (12, "FieldNode pole adapter", ["vblocks", "ascrews", "abands"]),
    "fan": (13, "Aspiration fan and cowl", ["fan", "cowl", "fan_screws"]),
}
BOM = {k: (v[0], v[1]) for k, v in BOM_GROUPS.items()}
HEAD = ["shield", "fan", "th_sensor", "globe", "probe", "anemometer", "arm", "clamp", "harness", "lanyard"]


def build_components(p=PARAMS):
    """{group key: Component} for option A, each the fusion of its parts (the key names of the earlier model)."""
    groups = {}
    for pt in components("A"):
        if pt["kind"] == "context":
            continue
        groups.setdefault(pt["group"], []).append(pt)
    out = {}
    for g, items in groups.items():
        line = next((i["bom"] for i in items if i["bom"]), 0)
        shape = fuse(i["shape"] for i in items)
        mass = sum(cp.mass_kg(i) for i in items)            # kg, from the materials of the parts
        dens = mass / (shape.volume / 1e9) if shape.volume else 0.0   # effective kg/m3, so sizing.py's volume x density gives the mass
        out[g] = Component(g, items[0]["name"], shape, line or 0, items[0]["kind"], dens)
    return out


def build_parts(p=PARAMS, C=None):
    """{BOM key: solid} for the BOM items of option A (the drawing, the concept media and the exports)."""
    C = C or build_components(p)
    return {k: fuse(C[c].shape for c in v[2]) for k, v in BOM_GROUPS.items()}


def assembly(p=PARAMS, with_pole=False):
    parts = build_parts(p)
    kids = list(parts.values()) + ([pole_context(p)] if with_pole else [])
    return b.Compound(children=kids)


# ------------------------------------------------------------------ constructability checks (option A)
def check(p=PARAMS, verbose=True):
    """Touches and clearances between groups of option A. Returns (passed, failed) lists of strings.
    Overlaps between individual parts are checked by .kit/cad_check.py."""
    C = build_components(p)
    D = derived(p)
    pole = pole_context(p, p["arm_z"] - 300, p["fn_z0"] + 700)
    shapes = {k: c.shape for k, c in C.items()}
    shapes["pole"] = pole
    ok, bad = [], []

    def dist(a, c):
        return shapes[a].distance_to(shapes[c])
    touch = [("trim", "pole"), ("trim", "saddle"), ("saddle", "cheeks"), ("arm", "saddle"), ("arm", "cheeks"),
             ("bands", "pole"), ("clamp_bolts", "cheeks"), ("clamp_bolts", "saddle"), ("rods", "plates"), ("rods", "arm"),
             ("spacers", "arm"), ("spacers", "rods"), ("fan", "plates"), ("cowl", "fan"), ("fan_screws", "cowl"),
             ("fan_screws", "plates"), ("hanger", "arm"), ("anemometer", "mast_bolt"), ("mast_bolt", "arm"), ("plug", "arm"),
             ("vblocks", "pole"), ("vblocks", "fieldnode"), ("ascrews", "fieldnode"), ("abands", "pole"),
             ("harness", "fieldnode"), ("lanyard", "arm"), ("lanyard", "plates"), ("lanyard", "globe")]
    for a, c in touch:
        d = dist(a, c)
        (ok if d < 0.6 else bad).append(f"touch {a} / {c}: {d:.2f} mm")
    clear = [("harness", "pole", 0.5), ("harness", "saddle", 2.0), ("harness", "cheeks", 0.5), ("harness", "plates", 0.5),
             ("harness", "clamp_bolts", 0.5), ("harness", "bands", 0.5), ("harness", "abands", 0.5), ("harness", "vblocks", 2.0),
             ("cowl", "rods", 2.0), ("cowl", "spacers", 2.0), ("globe", "arm", 30.0), ("plates", "arm", 30.0),
             ("fieldnode", "arm", 100.0), ("fieldnode", "saddle", 50.0), ("fieldnode", "cheeks", 50.0), ("fieldnode", "bands", 50.0),
             ("fieldnode", "anemometer", 100.0), ("fieldnode", "plates", 50.0), ("fieldnode", "globe", 50.0), ("anemometer", "globe", 10.0),
             ("saddle", "pole", 1.0), ("th_sensor", "plates", 0.1)]
    for a, c, m in clear:
        d = dist(a, c)
        (ok if d >= m else bad).append(f"clearance {a} / {c} >= {m} mm: {d:.1f} mm")
    for dd in p["pole_range"]:
        R = dd / 2
        lat = R * math.cos(math.radians(p["v_angle"] / 2))
        good = lat < D["notch_half"] - 1 and lat < p["adapter_vblock"][0] / 2 - 1
        (ok if good else bad).append(f"pole {dd:.0f} mm touches both V faces {lat:.1f} mm each side of centre "
                                     f"(saddle notch half-width {D['notch_half']:.1f}, adapter {p['adapter_vblock'][0] / 2:.0f})")
    if verbose:
        for s in bad:
            print("FAIL", s)
        print(f"{len(ok)} checks pass, {len(bad)} fail")
    return ok, bad


if __name__ == "__main__":
    if "--check" in sys.argv:
        _, bad = check()
        sys.exit(1 if bad else 0)
    out = HERE.parent
    (out / "stl").mkdir(exist_ok=True)
    for opt in OPTIONS:
        ps = [q for q in components(opt) if q["kind"] != "context"]
        mass = sum(cp.mass_kg(q) for q in ps)
        print(f"option {opt} {OPTIONS[opt]}: {len(ps)} parts, mass {mass:.2f} kg")
    if "--no-stl" not in sys.argv:
        P_ = build_parts()
        groups = {"heatmap-node-assembly": list(P_.values()), "sensor-head": [P_[k] for k in HEAD],
                  "fieldnode-core-envelope": [P_["fieldnode"], P_["adapter"]]}
        for name, shapes in groups.items():
            c = b.Compound(children=shapes)
            b.export_stl(c, str(out / "stl" / f"{name}.stl"), tolerance=0.2, angular_tolerance=0.3)
            bb = c.bounding_box()
            print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    D = derived()
    print(f"arm axis {PARAMS['arm_z']:.0f} mm; shield center {D['shield_zc']:.0f} mm; globe center {D['globe_zc']:.0f} mm; "
          f"cups {D['cup_z']:.0f} mm; reach {D['reach']:.0f} mm from the pole axis; top {D['overall_top']:.0f} mm")
