"""HeatMap Node parametric model (build123d), TRL 3, constructable design (HMN-DDR-003).

Revised under HMN-DDR-002 (2026-09-25): aspiration fan and cowl on the shield, formed sheet
saddle, arm pointing toward the equator with the FieldNode core above it (2026-10-02), and FieldNode's
hot-climate sun shield on the core. Made constructable under HMN-DDR-003 (2026-10-01,
"Design for construction"): every part can now be cut, bent, drilled, printed or bought, and
every part touches and is fixed to the parts next to it. `python cad/src/model.py --check`
runs the constructability checks (overlaps, contacts and clearances).

Run from the repo root:  python cad/src/model.py [--check]
Exports STEP and STL into cad/step and cad/stl:
    heatmap-node-assembly.step / .stl   sensor head and FieldNode core as fitted to the pole
    sensor-head.step / .stl             arm, clamp, shield, sensors, globe, anemometer, harness
    fieldnode-core-envelope.step / .stl FieldNode envelope, sun shield and the HeatMap pole adapter

Axes: the existing street pole is the Z axis (x = y = 0), Z is up with the pavement at
z = 0. The sensor arm reaches out along +X, which points toward the equator (HMN-DDR-002).
The FieldNode core is built in its own convention (panel facing -Y) and turned by fn_azimuth
about the pole, so it sits on the pole's +X face above the arm (its whip 100 mm or more clear of the arm)
with its panel facing +X. Decided 2026-10-02 (HMN-DEC-001, item 3, option a); the sensor leads run
down the pole from the core ports to the arm.
The FieldNode core is an envelope taken from FND-DWG-001 Rev P3 (back plate with its band slots
and V-block screw holes, enclosure, ports, whip, panel, a simplified bracket and the hot-climate
sun shield); it is built to the FieldNode build plan FND-BLD-001 in its own repo. Main
dimensions and interfaces only; not for fabrication. The same PARAMS feed docs/04-calcs/sizing.py
(HMN-CAL-001), the drawing HMN-DWG-001 (cad/src/sheets.py), the concept media
(cad/src/concept_media.py) and the build plan pictures (cad/src/build_plan_media.py).
"""
import math
import sys
from dataclasses import dataclass
from pathlib import Path

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
    # 12 HeatMap pole adapter for the FieldNode core: two printed 120 deg V-blocks (W x H x depth)
    #   at the FieldNode clamp heights (from the enclosure bottom), and strap bands
    "adapter_vblock": (110.0, 30.0, 38.0), "adapter_dz": (-20.0, 230.0), "adapter_slot": (3.5, 16.0),
    # FieldNode core turned about the pole so that its panel faces +X, the arm's direction (deg)
    "fn_azimuth": 90.0,
    # FieldNode hot-climate sun shield (FND BOM line 14): sheet (drawn), gap, low edge, top slot
    "fns_t": 1.0, "fns_gap": 15.0, "fns_low": 10.0, "fns_slot": 30.0,
}


HARNESS_RUN = {}   # filled by build_components: mm of lead from each core port to the arm sensors (the main run, before the sensor tails)


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
    }


def _b3d():
    import build123d as b
    return b


def box(cx, cy, cz, sx, sy, sz):
    b = _b3d()
    return b.Pos(cx, cy, cz) * b.Box(sx, sy, sz)


def rod(a, c, r):
    """Solid rod of radius r between two 3D points."""
    b = _b3d()
    a, c = b.Vector(*a), b.Vector(*c)
    d = c - a
    return b.Solid.make_cylinder(r, d.length, b.Plane(origin=a, z_dir=d.normalized()))


def path(points, r):
    """A cable or wire along a polyline, with round joints so the bends do not gap."""
    b = _b3d()
    out = fuse(rod(a, c, r) for a, c in zip(points, points[1:]))
    for q in points[1:-1]:
        out = out + b.Pos(*q) * b.Sphere(r)
    return out


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def zcyl(x, y, z, r, h):
    b = _b3d()
    return b.Pos(x, y, z) * b.Cylinder(r, h)


def hexnut(x, y, z0, af, h, bore, axis="z", blind=False):
    """Hex nut across flats af, height h, with a bore; base at z0 along +axis (axis 'z', '-z', 'y', '-y')."""
    b = _b3d()
    n = b.extrude(b.RegularPolygon(af / math.sqrt(3), 6), amount=h)
    if blind:       # acorn nut: bore open at the base only, domed top
        n = n - b.Pos(0, 0, -0.01) * b.Cylinder(bore / 2, h * 0.7, align=(b.Align.CENTER, b.Align.CENTER, b.Align.MIN))
        n = n + b.Pos(0, 0, h) * (b.Sphere(af / 2 * 0.95) & b.Pos(0, 0, af) * b.Box(2 * af, 2 * af, 2 * af))
    else:
        n = n - b.Cylinder(bore / 2, 4 * h)
    rot = {"z": b.Rot(0, 0, 0), "-z": b.Rot(180, 0, 0), "y": b.Rot(-90, 0, 0), "-y": b.Rot(90, 0, 0)}[axis]
    return b.Pos(x, y, z0) * rot * n


def ring_band(points, w, t, z):
    """A thin strap band (width w, thickness t) whose centerline is the closed polygon points, at height z."""
    b = _b3d()
    wire = b.Wire.make_polygon([b.Vector(x, y, 0) for x, y in points], close=True)
    outer = wire.offset_2d(t / 2, kind=b.Kind.INTERSECTION)
    inner = wire.offset_2d(-t / 2, kind=b.Kind.INTERSECTION)
    face = b.Face(outer, [inner])
    return b.Pos(0, 0, z - w / 2) * b.extrude(face, amount=w)


def band_path(r, sx, sy_in, sy_out, front, n=40):
    """Centerline of a band round the back of a pole of radius r (centred at the origin, the
    clamped part on +X): from the pole it runs to (sx, +/-sy) at x = sy_in, through slots to
    x = sy_out and across the front at x = front. Returns 2D points, counter-clockwise."""
    # tangent point from (sy_in, sx) to the circle, on the back (-X) side
    def tangent(px, py):
        d = math.hypot(px, py)
        a = math.atan2(py, px)
        da = math.acos(r / d)
        return a + da if py > 0 else a - da
    a1 = tangent(sy_in, sx)          # upper side
    a2 = tangent(sy_in, -sx) + 2 * math.pi
    pts = [(front, -sx), (front, sx), (sy_out, sx), (sy_in, sx)]
    for i in range(n + 1):
        a = a1 + (a2 - a1) * i / n
        pts.append((r * math.cos(a), r * math.sin(a)))
    pts += [(sy_in, -sx), (sy_out, -sx)]
    return pts


@dataclass
class Component:
    """One component: a single made or bought piece, or a matched set of fixings."""
    key: str
    name: str
    shape: object
    line: int            # BOM line
    kind: str            # "made", "bought", "fixing" or "fieldnode"
    density: float       # kg/m3 for the mass estimate (0: mass taken from the calc note instead)


def build_components(p=PARAMS):
    """Return {key: Component} for every component, in build order."""
    b = _b3d()
    D = derived(p)
    r = D["r"]
    az = p["arm_z"]
    half = math.radians(p["v_angle"] / 2)
    C = {}

    def add(key, name, shape, line, kind, density):
        C[key] = Component(key, name, shape, line, kind, density)

    # ------------------------------------------------------------ 8 arm clamp: saddle, trim, cheeks, bands
    sw, sh, sd = p["saddle"]
    wt = p["saddle_wall"]
    wo, wi, fe = D["web_out"], D["web_in"], D["flange_edge"]
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
    add("saddle", "Arm saddle", saddle, 8, "made", 2700)

    # rubber edge trim on the notch edges: the bearing strip, trim_t thick, 6 mm tall, on each flange
    tt = p["trim_t"]
    va = D["v_apex"]
    trim = None
    for s in (-1, 1):
        zf = az + s * (sh / 2 - wt / 2)
        poly = b.Polygon((ma, 0), (fe, (ma - fe) * math.tan(half)), (fe, (ma - fe) * math.tan(half) - tt / math.cos(half)),
                         (va, 0), (fe, -(ma - fe) * math.tan(half) + tt / math.cos(half)), (fe, -(ma - fe) * math.tan(half)), align=None)
        strip = b.Pos(0, 0, zf) * b.extrude(poly, amount=3.0, both=True)
        trim = strip if trim is None else trim + strip
    add("trim", "Rubber edge trim", trim, 8, "bought", 1200)

    # cheeks: angle with the flat leg on the web front and the upright leg against the arm side
    cl, ct, ch = p["cheek"]
    aw = p["arm_w"]
    cheeks = None
    for s in (-1, 1):
        flat = box(wo + ct / 2, s * (aw / 2 + cl / 2), az, ct, cl, ch)
        up = box(wo + cl / 2, s * (aw / 2 + ct / 2), az, cl, ct, ch)
        c = flat + up
        for dz in (-p["cheek_web_dz"], p["cheek_web_dz"]):
            c = c - b.Pos(wo + ct / 2, s * p["cheek_web_y"], az + dz) * b.Rot(0, 90, 0) * b.Cylinder(3.3, ct + 2)
        for bx in p["cheek_bolt_x"]:
            c = c - b.Pos(wo + bx, s * (aw / 2 + ct / 2), az) * b.Rot(90, 0, 0) * b.Cylinder(3.3, ct + 2)
        cheeks = c if cheeks is None else cheeks + c
    add("cheeks", "Arm cheeks (2)", cheeks, 8, "made", 2700)

    # saddle bands: round the back of the pole, through the web slots, across the web front
    bt = p["band_t"]
    bands = None
    for dz in (-p["band_dz"], p["band_dz"]):
        pts = band_path(r + bt / 2 + 0.1, p["band_slot_y"], wi - 2, wo + bt / 2, wo + bt / 2)
        bd = ring_band(pts, p["band_w"], bt, az + dz)
        bands = bd if bands is None else bands + bd
    add("bands", "Saddle strap bands (2)", bands, 8, "bought", 7900)

    # ------------------------------------------------------------ 7 sensor arm, its end plug and crush sleeves
    x0, x1 = D["arm_x0"], D["arm_x1"]
    at = p["arm_t"]
    arm = box((x0 + x1) / 2, 0, az, x1 - x0, aw, aw) - box((x0 + x1) / 2, 0, az, x1 - x0 + 4, aw - 2 * at, aw - 2 * at)
    sx = p["shield_x"]
    rr = p["rod_pcd"] / 2
    for xx, d in ((sx - rr, 5.5), (sx + rr, 5.5), (p["globe_x"], p["hanger"][0] + 0.5), (D["anemo_x"], p["mast_d"] + 0.5)):
        arm = arm - zcyl(xx, 0, az, d / 2, aw + 4)
    for bx in p["cheek_bolt_x"]:
        arm = arm - b.Pos(x0 + bx, 0, az) * b.Rot(90, 0, 0) * b.Cylinder(3.3, aw + 4)
    arm = arm - b.Pos(D["anemo_x"], 0, az) * b.Rot(90, 0, 0) * b.Cylinder(2.75, aw + 4)
    add("arm", "Sensor arm", arm, 7, "made", 2700)
    plug = box(x1 - 6, 0, az, 12, aw - 2 * at, aw - 2 * at) + box(x1 + 1.25, 0, az, 2.5, aw, aw)
    add("plug", "Arm end plug", plug, 10, "bought", 1100)
    sleeves = fuse(b.Pos(x0 + bx, 0, az) * b.Rot(90, 0, 0) * (b.Cylinder(4.0, aw - 2 * at) - b.Cylinder(3.2, aw)) for bx in p["cheek_bolt_x"])
    add("sleeves", "Crush sleeves (2)", sleeves, 10, "fixing", 2700)

    # cheek bolts: two M6 through cheeks, arm and sleeves (heads +Y, nuts -Y); four M6 through web and cheeks
    yy = aw / 2 + ct
    cb = None
    for bx in p["cheek_bolt_x"]:
        cb_ = b.Pos(x0 + bx, 0, az) * b.Rot(90, 0, 0) * b.Cylinder(3.0, 2 * yy + 6)
        cb_ = cb_ + hexnut(x0 + bx, yy, az, 10, 4, 6, axis="y") + hexnut(x0 + bx, -yy, az, 10, 5, 6, axis="-y")
        cb = cb_ if cb is None else cb + cb_
    for s in (-1, 1):
        for dz in (-p["cheek_web_dz"], p["cheek_web_dz"]):
            y_, z_ = s * p["cheek_web_y"], az + dz
            cb = cb + b.Pos((wi - 3.3 + wo + ct + 6) / 2, y_, z_) * b.Rot(0, 90, 0) * b.Cylinder(3.0, wo + ct + 6 - wi + 3.3)
            cb = cb + b.Pos(wi - 1.65, y_, z_) * b.Rot(0, 90, 0) * b.Cylinder(5.25, 3.3)     # button head inside the web
            cb = cb + b.Pos(wo + ct, y_, z_) * b.Rot(0, 90, 0) * (b.extrude(b.RegularPolygon(10 / math.sqrt(3), 6), amount=5) - b.Cylinder(3, 20))
    add("clamp_bolts", "Clamp bolts", cb, 10, "fixing", 7900)

    # ------------------------------------------------------------ 2 radiation shield: plates, rods, spacers, nuts
    pt, pitch = p["plate_t"], p["plate_pitch"]
    st = D["shield_top"]
    sr = p["shield_d"] / 2
    rods_xy = [(sx + rr * math.cos(math.radians(a)), rr * math.sin(math.radians(a))) for a in (0, 90, 180, 270)]
    fh = p["fan_holes"] / 2
    plates = {}
    for i in range(p["n_plates"]):
        z = st - pt / 2 - i * pitch
        pl = zcyl(sx, 0, z, sr, pt) - zcyl(sx, 0, z, (p["top_hole"] if i == 0 else p["plate_hole"]) / 2, pt + 2)
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
        if i == 0:
            for ex in (-1, 1):
                for ey in (-1, 1):
                    pl = pl - zcyl(sx + ex * fh, ey * fh, z, 2.2, pt + 2)
        plates[i] = pl
    add("plates", "Shield plates (8)", fuse(plates.values()), 2, "made", 1070)
    sb = D["shield_bot"]
    long_top = D["arm_top"] + 4 + 4
    rods, nuts, spacers = None, None, None
    for k, (rx, ry) in enumerate(rods_xy):
        is_long = abs(ry) < 1
        top = long_top if is_long else st + 4 + 3
        rd = zcyl(rx, ry, (sb - 6 + top) / 2, p["rod_d"] / 2, top - (sb - 6))
        rods = rd if rods is None else rods + rd
        n = hexnut(rx, ry, sb, 8, 8, 5, axis="-z", blind=True) + hexnut(rx, ry, st, 8, 4, 5)
        if is_long:
            n = n + hexnut(rx, ry, D["arm_top"], 8, 4, 5)
            sp = zcyl(rx, ry, (st + 4 + D["arm_bot"]) / 2, 4.0, D["arm_bot"] - st - 4) - zcyl(rx, ry, 0, 2.65, 1e5)
            spacers = sp if spacers is None else spacers + sp
        nuts = n if nuts is None else nuts + n
    add("rods", "Shield rods (4) and nuts", rods + nuts, 2, "fixing", 7900)
    add("spacers", "Shield spacers (2)", spacers, 2, "fixing", 2700)

    # ------------------------------------------------------------ 13 fan, cowl and fan screws
    fw, _, fht = p["fan"]
    cw, chh = p["cowl"]
    fan = box(sx, 0, st + fht / 2, fw, fw, fht) - zcyl(sx, 0, st + fht / 2, fw / 2 - 2, fht + 2)
    fan = fan + zcyl(sx, 0, st + fht / 2, 12, fht - 2)
    for a in (0, 120, 240):
        fan = fan + b.Pos(sx, 0, st + fht / 2) * b.Rot(0, 0, a) * b.Pos(20, 0, 0) * b.Box(17, 3, 2)
    for ex in (-1, 1):
        for ey in (-1, 1):
            fan = fan - zcyl(sx + ex * fh, ey * fh, st + fht / 2, 2.2, fht + 2)
    add("fan", "Aspiration fan", fan, 13, "bought", 0)
    lid_t, leg = 3.0, 8.0
    cowl = box(sx, 0, st + chh - lid_t / 2, cw, cw, lid_t)
    for ex in (-1, 1):
        for ey in (-1, 1):
            cowl = cowl + box(sx + ex * fh, ey * fh, st + fht + (chh - lid_t - fht) / 2, leg, leg, chh - lid_t - fht)
            cowl = cowl - zcyl(sx + ex * fh, ey * fh, st + chh / 2, 2.2, chh + 2)
    add("cowl", "Fan cowl", cowl, 13, "made", 1070)
    fs = None
    for ex in (-1, 1):
        for ey in (-1, 1):
            x_, y_ = sx + ex * fh, ey * fh
            s_ = zcyl(x_, y_, (st - pt - 4 + st + chh) / 2, 2.0, chh + pt + 4) + zcyl(x_, y_, st + chh + 1.4, 4.0, 2.8)
            s_ = s_ + hexnut(x_, y_, st - pt, 7, 3.2, 4, axis="-z")
            fs = s_ if fs is None else fs + s_
    add("fan_screws", "Fan screws (4)", fs, 13, "fixing", 7900)

    # ------------------------------------------------------------ 3 temperature and humidity sensor
    cd, cln = p["th_sensor"]
    add("th_sensor", "Temperature and humidity sensor", zcyl(sx, 0, D["shield_zc"], cd / 2, cln), 3, "bought", 0)

    # ------------------------------------------------------------ 4 globe with its hanger tube and nuts; 5 probe
    gx, gz, gr = p["globe_x"], D["globe_zc"], p["globe_d"] / 2
    ho, hb = p["hanger"]
    gt = D["globe_top"]
    globe = b.Pos(gx, 0, gz) * (b.Sphere(gr) - b.Sphere(gr - p["globe_wall_drawn"]))
    globe = globe + zcyl(gx, 0, gt + 4, 10, 16)
    globe = globe - zcyl(gx, 0, gt, ho / 2, 40)
    add("globe", "Black globe", globe, 4, "bought", 0)
    h_bot, h_top = gt - 2, D["arm_top"] + 8 + 6
    hanger = zcyl(gx, 0, (h_bot + h_top) / 2, ho / 2, h_top - h_bot) - zcyl(gx, 0, (h_bot + h_top) / 2, hb / 2, h_top - h_bot + 2)
    hanger = hanger + hexnut(gx, 0, gt + 12, 17, 8, ho) + hexnut(gx, 0, D["arm_bot"], 17, 8, ho, axis="-z") + hexnut(gx, 0, D["arm_top"], 17, 8, ho)
    add("hanger", "Globe hanger tube and nuts", hanger, 4, "fixing", 8500)
    probe = rod((gx, 0, h_top + 4), (gx, 0, gz), p["probe_d"] / 2) + b.Pos(gx, 0, gz) * b.Sphere(p["bead_d"] / 2)
    add("probe", "Globe probe", probe, 5, "bought", 0)

    # ------------------------------------------------------------ 6 anemometer on its mast through the arm
    ax, hz = D["anemo_x"], D["hub_z"]
    mb = D["arm_bot"] - p["mast_below"]
    mast = zcyl(ax, 0, (mb + hz - 20) / 2, p["mast_d"] / 2, hz - 20 - mb) - zcyl(ax, 0, (mb + hz - 20) / 2, p["mast_d"] / 2 - 1.5, hz - mb)
    mast = mast - b.Pos(ax, 0, az) * b.Rot(90, 0, 0) * b.Cylinder(2.75, 40)
    an = mast + zcyl(ax, 0, hz, 22, 40)
    cr = p["cup_d"] / 2
    for a in (30, 150, 270):
        cx_, cy_ = ax + p["cup_arm"] * math.cos(math.radians(a)), p["cup_arm"] * math.sin(math.radians(a))
        an = an + rod((ax, 0, hz + 10), (cx_, cy_, hz + 10), 2.5)
        cup = b.Pos(cx_, cy_, hz + 10) * (b.Sphere(cr) - b.Sphere(cr - 2))
        cut = b.Pos(cx_ + cr * math.cos(math.radians(a + 90)), cy_ + cr * math.sin(math.radians(a + 90)), hz + 10) * b.Box(2 * cr, 2 * cr, 2.5 * cr)
        an = an + (cup - cut)
    add("anemometer", "Cup anemometer", an, 6, "bought", 0)
    xb = b.Pos(ax, 0, az) * b.Rot(90, 0, 0) * b.Cylinder(2.5, aw + 8)
    xb = xb + hexnut(ax, aw / 2, az, 8, 3, 5, axis="y") + hexnut(ax, -aw / 2, az, 8, 4, 5, axis="-y")
    add("mast_bolt", "Mast cross bolt", xb, 6, "fixing", 7900)

    # ------------------------------------------------------------ 11 lanyards, looped round the arm
    ld = p["lanyard_d"] / 2

    def loop(xl):
        return [(xl, 14, az - 14), (xl, 14, az + 14), (xl, -25, az + 14), (xl, -25, az - 14), (xl, 14, az - 14)]
    lan = path([(sx - 30, 42, st), (sx - 30, 42, st + 30), (sx - 30, 14, az - 14)] + loop(sx - 30)[1:], ld)
    lan = lan + path([(gx + 11, 0, gt + 6), (gx + 30, 14, D["arm_bot"] - 14), (gx + 30, 14, az - 14)] + loop(gx + 30)[1:], ld)
    add("lanyard", "Retention lanyards (2)", lan, 11, "bought", 7900)

    # ------------------------------------------------------------ 1 FieldNode core envelope (FND-DWG-001 Rev P3)
    ew, ed, eh = p["fn_enc"]
    z0 = p["fn_z0"]
    pw, ph, ptk = p["fn_plate"]
    y0 = D["plate_y0"]
    turn = b.Rot(0, 0, p["fn_azimuth"])
    plate = box(0, y0 - ptk / 2, z0 - p["fn_plate_drop"] + ph / 2, pw, ptk, ph)
    for dz in p["adapter_dz"]:
        for s in (-1, 1):
            plate = plate - box(s * p["fn_band_slot_x"], y0 - ptk / 2, z0 + dz, 3.0, ptk + 2, 15.0)
            plate = plate - b.Pos(s * p["fn_vscrew_x"], y0 - ptk / 2, z0 + dz) * b.Rot(90, 0, 0) * b.Cylinder(2.25, ptk + 2)
    enc = box(0, D["enc_yc"], z0 + eh / 2, ew, ed, eh)
    tilt = p["fn_tilt"]
    panel = b.Pos(0, D["panel_cy"], D["panel_cz"]) * b.Rot(tilt, 0, 0) * b.Box(*p["fn_panel"])
    t = math.radians(tilt)
    bars = fuse(path([(bx, y0 - ptk, z0 + 260), (bx, D["panel_cy"] + 80 * math.cos(t), D["panel_cz"] + 80 * math.sin(t) - 10)], 5)
                + path([(bx, y0 - ptk, z0 + 210), (bx, D["panel_cy"] - 60 * math.cos(t), D["panel_cz"] - 60 * math.sin(t) - 10)], 5)
                for bx in (-80, 80))
    wd, wl = p["fn_whip"]
    yrow = D["enc_back"] - p["fn_front_row"]
    whip = zcyl(p["fn_ant_x"], yrow, z0 - wl / 2, wd / 2, wl)
    ports = fuse(zcyl(x, yrow, z0 - 8, 11, 16) for x in p["fn_ports_x"])
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
    add("fieldnode", "FieldNode core (built to FND-BLD-001)", turn * (plate + enc + panel + bars + whip + ports + fshield), 1, "fieldnode", 0)

    # ------------------------------------------------------------ 12 pole adapter: printed V-blocks, screws, bands
    vw, vh, vd = p["adapter_vblock"]
    blocks, ascrews, abands = None, None, None
    va_d = D["a_vdepth"]
    for dz in p["adapter_dz"]:
        z = z0 + dz
        blk = box(0, y0 + vd / 2, z, vw, vd, vh)
        mouth = y0 + vd
        vcut = b.extrude(b.Polygon((0, mouth - va_d), (vw / 2 + 2, mouth + 2 / math.tan(half)), (-vw / 2 - 2, mouth + 2 / math.tan(half)), align=None),
                         amount=vh + 4, both=True)
        blk = blk - b.Pos(0, 0, z) * vcut
        sxa, sza = p["adapter_slot"]
        for s in (-1, 1):
            blk = blk - box(s * p["fn_band_slot_x"], y0 + vd / 2, z, sxa, vd + 2, sza)
            blk = blk - b.Pos(s * p["fn_vscrew_x"], y0 + 6, z) * b.Rot(90, 0, 0) * b.Cylinder(2.0, 12)
            sc = b.Pos(s * p["fn_vscrew_x"], y0 + (10 - ptk) / 2, z) * b.Rot(90, 0, 0) * b.Cylinder(2.0, 10 + ptk)
            ascrews = sc if ascrews is None else ascrews + sc
        blocks = blk if blocks is None else blocks + blk
        # band: round the back of the pole (local +Y), through block and plate slots, across the plate front
        pts = band_path(r + bt / 2 + 0.1, p["fn_band_slot_x"], -(mouth + 4), -(y0 - ptk - bt / 2), -(y0 - ptk - bt / 2))
        bd = b.Rot(0, 0, -90) * ring_band(pts, p["band_w"], bt, z)
        abands = bd if abands is None else abands + bd
    add("vblocks", "Adapter V-blocks (2)", turn * blocks, 12, "made", 1070)
    add("ascrews", "Adapter screws (4)", turn * ascrews, 12, "fixing", 7900)
    add("abands", "Adapter strap bands (2)", turn * abands, 12, "bought", 7900)

    # ------------------------------------------------------------ 9 harness: two leads from the FieldNode ports
    ld_, td = p["lead_d"] / 2, p["tail_d"] / 2
    rr_, ang = p["pole_run"]
    leads = None
    for k, (px, dzl, dang) in enumerate(((p["fn_ports_x"][0], 5.0, -6.0), (p["fn_ports_x"][1], -5.0, 6.0))):
        wx, wy = -yrow, px          # port after the 90 deg turn: (x, y) -> (-y, x)
        a = math.radians(ang + dang)
        prx, pry = rr_ * math.cos(a), rr_ * math.sin(a)
        zlow = z0 - 70 - 10 * k          # the leads leave the core ports downward and run down the pole
        pts = [(wx, wy, z0 - 16), (wx, wy, zlow), (60, -80 - 8 * k, zlow), (prx, pry, zlow), (prx, pry, az + 105 - 8 * k),
               (45, -82 - 8 * k, az + 105 - 8 * k), (90, -64 - 8 * k, az + 105 - 8 * k), (90, -64 - 8 * k, az + dzl), (125, -27, az + dzl), (140, -19.5, az + dzl)]
        if k == 0:      # lead A: temperature and humidity sensor and fan
            pts += [(sx + 60, -19.5, az + dzl)]
            lead = path(pts, ld_)
            tail = [(sx + 60, -19.5, az + dzl), (sx + 44, -44, az - 25), (sx + 44, -44, st - 21), (sx, 0, st - 21),
                    (sx, 0, D["shield_zc"] + cln / 2)]
            lead = lead + path(tail, td)
        else:           # lead B: globe probe and anemometer
            pts += [(ax - 14, -19.5, az + dzl)]
            lead = path(pts, ld_)
            lead = lead + path([(gx - 25, -19.5, az + dzl), (gx - 25, -19.5, h_top + 6), (gx, 0, h_top + 6)], td)
            lead = lead + path([(ax - 14, -19.5, az + dzl), (ax - 14, -10, mb - 4), (ax, 0, mb - 4)], td)
        HARNESS_RUN[k] = sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
        leads = lead if leads is None else leads + lead
    add("harness", "Sensor harness (2 leads)", leads, 9, "bought", 0)
    return C


# BOM groups for the concept media and the exports: model key -> (BOM line, name, component keys)
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


def build_parts(p=PARAMS, C=None):
    """Return {key: solid} for the BOM items (key names in BOM above)."""
    C = C or build_components(p)
    return {k: fuse(C[c].shape for c in v[2]) for k, v in BOM_GROUPS.items()}


def pole_context(p=PARAMS, z_lo=0.0, z_hi=None):
    """Existing street pole (not supplied, not in the BOM)."""
    z_hi = p["pole_h"] if z_hi is None else z_hi
    return zcyl(0, 0, (z_lo + z_hi) / 2, p["pole_od"] / 2, z_hi - z_lo)


def assembly(p=PARAMS, with_pole=False):
    b = _b3d()
    parts = build_parts(p)
    kids = list(parts.values()) + ([pole_context(p)] if with_pole else [])
    return b.Compound(children=kids)


# ------------------------------------------------------------------ constructability checks
def check(p=PARAMS, verbose=True):
    """Overlaps, contacts and clearances. Returns (passed, failed) lists of strings."""
    import itertools
    C = build_components(p)
    D = derived(p)
    pole = pole_context(p, p["arm_z"] - 300, p["fn_z0"] + 700)
    shapes = {k: c.shape for k, c in C.items()}
    shapes["pole"] = pole
    # pairs that are meant to share material: a threaded or pressed joint modelled as one volume
    allowed = {("globe", "hanger")}
    ok, bad = [], []

    def dist(a, c):
        return shapes[a].distance_to(shapes[c])
    for a, c in itertools.combinations(shapes, 2):
        if (a, c) in allowed or (c, a) in allowed:
            continue
        try:
            v = (shapes[a] & shapes[c]).volume
        except Exception:
            v = 0.0
        (bad if v > 0.5 else ok).append(f"no overlap {a} / {c}" + (f": {v:.1f} mm3" if v > 0.5 else ""))
    touch = [("trim", "pole"), ("trim", "saddle"), ("saddle", "cheeks"), ("arm", "saddle"), ("arm", "cheeks"),
             ("bands", "pole"), ("clamp_bolts", "cheeks"), ("clamp_bolts", "saddle"), ("sleeves", "arm"),
             ("rods", "plates"), ("rods", "arm"), ("spacers", "arm"), ("spacers", "rods"), ("fan", "plates"),
             ("cowl", "fan"), ("fan_screws", "cowl"), ("fan_screws", "plates"), ("hanger", "arm"),
             ("anemometer", "mast_bolt"), ("mast_bolt", "arm"), ("plug", "arm"),
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
    # the pole range: contact on the V for the smallest and largest poles, inside the notch and the block
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
    from build123d import Compound, export_step, export_stl
    out = Path(__file__).resolve().parents[1]
    (out / "step").mkdir(exist_ok=True)
    (out / "stl").mkdir(exist_ok=True)
    P = build_parts()
    groups = {
        "heatmap-node-assembly": list(P.values()),
        "sensor-head": [P[k] for k in HEAD],
        "fieldnode-core-envelope": [P["fieldnode"], P["adapter"]],
    }
    for name, shapes in groups.items():
        c = Compound(children=shapes)
        export_step(c, str(out / "step" / f"{name}.step"))
        export_stl(c, str(out / "stl" / f"{name}.stl"), tolerance=0.2, angular_tolerance=0.3)
        bb = c.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    D = derived()
    print(f"arm axis {PARAMS['arm_z']:.0f} mm; shield center {D['shield_zc']:.0f} mm; globe center {D['globe_zc']:.0f} mm; "
          f"cups {D['cup_z']:.0f} mm; reach {D['reach']:.0f} mm from the pole axis; top {D['overall_top']:.0f} mm")
