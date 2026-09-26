"""HeatMap Node parametric model (build123d), TRL 3, massing-plus level of detail.

Run from the repo root:  python cad/src/model.py
Exports STEP and STL into cad/step and cad/stl:
    heatmap-node-assembly.step / .stl   sensor head and FieldNode core as fitted to the pole
    sensor-head.step / .stl             arm, clamp, shield, sensors, globe, anemometer, harness
    fieldnode-core-envelope.step / .stl FieldNode envelope with the HeatMap pole adapter

Axes: the existing street pole is the Z axis (x = y = 0), Z is up with the pavement at
z = 0. The sensor arm reaches out along +X. The FieldNode core hangs on the pole's -Y face,
which is meant to face the equator, so its panel tilts toward -Y (the FieldNode convention).
The FieldNode core is an envelope taken from FND-DWG-001 Rev P1 (enclosure, back plate,
panel, bracket, whip); its internals are in the FieldNode repo. Main dimensions and
interfaces only; not fabrication detail and not for fabrication. The same PARAMS feed
docs/04-calcs/sizing.py (HMN-CAL-001), the drawing HMN-DWG-001 (cad/src/sheets.py) and the
concept media (cad/src/concept_media.py).
"""
import math
from pathlib import Path

# Top-level parameters (mm). Edit these, not the geometry below.
PARAMS = {
    # site interface: existing round pole (design case 114.3 mm OD, 4 in nominal); fit range
    "pole_od": 114.3, "pole_range": (60.0, 200.0), "pole_h": 3400.0,   # shown height only
    # 8 arm clamp: 120 deg V saddle, width (Y) x height (Z) x depth (X); two strap bands
    "saddle": (110.0, 180.0, 30.0), "saddle_wall": 5.0, "v_angle": 120.0, "band_w": 13.0, "band_dz": 70.0,
    # 7 sensor arm: 25 x 25 x 2 mm aluminium square tube; length from the saddle face; height
    "arm_z": 2800.0, "arm_w": 25.0, "arm_t": 2.0, "arm_len": 520.0,
    # 2 radiation shield: plate diameter, count, pitch, thickness, center hole, x position, gap below arm
    "shield_d": 110.0, "n_plates": 8, "plate_pitch": 15.0, "plate_t": 3.0, "plate_hole": 56.0,
    "shield_x": 300.0, "shield_gap": 20.0, "rod_d": 5.0, "rod_pcd": 84.0,
    # 3 air temperature and humidity sensor (capsule diameter x length)
    "th_sensor": (18.0, 45.0),
    # 4 black globe: diameter, copper wall used for mass (drawn thicker), x position, gap below arm
    "globe_d": 150.0, "globe_wall": 0.4, "globe_wall_drawn": 1.5, "globe_x": 500.0, "globe_gap": 45.0,
    # 5 globe probe: stem diameter, bead diameter
    "probe_d": 5.0, "bead_d": 10.0,
    # 6 cup anemometer: mast height above the arm top, cup radius arm, cup diameter, inset from arm tip
    "mast_h": 170.0, "mast_d": 16.0, "cup_arm": 70.0, "cup_d": 44.0, "anemo_inset": 20.0,
    # 11 secondary retention lanyard (globe and shield to the arm), wire diameter
    "lanyard_d": 2.0,
    # 1 FieldNode core envelope, from FND-DWG-001 Rev P1: enclosure W (X) x D (Y) x H (Z),
    #   bottom height, back plate W x H x t, panel (X x slope x t), tilt, center (y from the plate
    #   rear face, height above the enclosure bottom), whip
    "fn_enc": (150.0, 90.0, 200.0), "fn_z0": 2150.0, "fn_plate": (180.0, 320.0, 3.0), "fn_plate_drop": 40.0,
    "fn_panel": (290.0, 200.0, 17.0), "fn_tilt": 40.0, "fn_panel_c": (-73.0, 385.0),
    "fn_whip": (10.0, 190.0), "fn_ports_x": (-52.0, -22.0),
    # 12 HeatMap pole adapter for the FieldNode core: two 120 deg V-blocks (W x H x depth) and strap bands
    "adapter_vblock": (110.0, 30.0, 18.0), "adapter_dz": (-20.0, 230.0),
}


def derived(p=PARAMS):
    """Dimensions the calc note and the drawing quote, computed from PARAMS."""
    r = p["pole_od"] / 2
    sw, sh, sd = p["saddle"]
    arm_x0 = r + sd                                    # arm root at the saddle face
    arm_x1 = arm_x0 + p["arm_len"]
    arm_bot = p["arm_z"] - p["arm_w"] / 2
    arm_top = p["arm_z"] + p["arm_w"] / 2
    shield_top = arm_bot - p["shield_gap"]
    stack_h = (p["n_plates"] - 1) * p["plate_pitch"] + p["plate_t"]
    shield_bot = shield_top - stack_h
    globe_r = p["globe_d"] / 2
    globe_zc = arm_bot - p["globe_gap"] - globe_r
    anemo_x = arm_x1 - p["anemo_inset"]
    hub_z = arm_top + p["mast_h"]
    plate_y0 = -(r + p["adapter_vblock"][2])           # FieldNode back plate rear face
    ew, ed, eh = p["fn_enc"]
    enc_back = plate_y0 - p["fn_plate"][2]
    t = math.radians(p["fn_tilt"])
    pcy = plate_y0 + p["fn_panel_c"][0]
    pcz = p["fn_z0"] + p["fn_panel_c"][1]
    half = p["fn_panel"][1] / 2
    return {
        "r": r, "arm_x0": arm_x0, "arm_x1": arm_x1, "arm_bot": arm_bot, "arm_top": arm_top,
        "shield_top": shield_top, "shield_bot": shield_bot, "shield_zc": (shield_top + shield_bot) / 2,
        "stack_h": stack_h, "globe_zc": globe_zc, "globe_bot": globe_zc - globe_r,
        "anemo_x": anemo_x, "hub_z": hub_z, "cup_z": hub_z + 10,
        "reach": anemo_x + p["cup_arm"] + p["cup_d"] / 2,       # farthest point from the pole axis
        "plate_y0": plate_y0, "enc_back": enc_back, "enc_front": enc_back - ed, "enc_yc": enc_back - ed / 2,
        "fn_top": pcz + half * math.sin(t) + p["fn_panel"][2] / 2,
        "panel_cy": pcy, "panel_cz": pcz,
        "panel_front_y": pcy - half * math.cos(t),
        "overall_top": hub_z + p["cup_d"] / 2 + 10,
        # the V-saddle touches a pole of radius r at +/- r cos(half angle) either side of center
        "v_contact_max": p["pole_range"][1] / 2 * math.cos(math.radians(p["v_angle"] / 2)) * 2,
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
    return fuse(rod(a, c, r) for a, c in zip(points, points[1:]))


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def zcyl(x, y, z, r, h):
    b = _b3d()
    return b.Pos(x, y, z) * b.Cylinder(r, h)


def band(z, r, w, t=1.5):
    return zcyl(0, 0, z, r + t, w) - zcyl(0, 0, z, r, w + 2)


def build_parts(p=PARAMS):
    """Return {key: solid} for the BOM items (key names in BOM below)."""
    b = _b3d()
    D = derived(p)
    r = D["r"]
    az = p["arm_z"]
    parts = {}

    # 8 Arm clamp: V saddle on the +X face and two strap bands
    sw, sh, sd = p["saddle"]
    wt = p["saddle_wall"]
    saddle = box(r + sd / 2, 0, az, sd, sw, sh)
    saddle = saddle - box(r + (sd - wt) / 2 - 1, 0, az, sd - wt + 2, sw - 2 * wt, sh - 2 * wt)   # channel, open to the pole
    saddle = saddle - zcyl(0, 0, az, r + 0.5, sh + 2)     # seats on the pole
    parts["clamp"] = saddle + band(az - p["band_dz"], r, p["band_w"]) + band(az + p["band_dz"], r, p["band_w"])

    # 7 Sensor arm (square tube) with the shield and globe hangers
    x0, x1, w = D["arm_x0"], D["arm_x1"], p["arm_w"]
    arm = box((x0 + x1) / 2, 0, az, x1 - x0, w, w) - box((x0 + x1) / 2 + 1, 0, az, x1 - x0 + 4, w - 2 * p["arm_t"], w - 2 * p["arm_t"])
    arm = arm + rod((p["shield_x"], 0, D["arm_bot"]), (p["shield_x"], 0, D["shield_top"]), 6)
    arm = arm + rod((p["globe_x"], 0, D["arm_bot"]), (p["globe_x"], 0, D["globe_zc"] + p["globe_d"] / 2 + 12), 6)
    parts["arm"] = arm

    # 2 Multi-plate radiation shield: solid top plate, open rings below, three spacer rods
    sx, sr = p["shield_x"], p["shield_d"] / 2
    plates = []
    for i in range(p["n_plates"]):
        z = D["shield_top"] - p["plate_t"] / 2 - i * p["plate_pitch"]
        pl = zcyl(sx, 0, z, sr, p["plate_t"])
        if i:
            pl = pl - zcyl(sx, 0, z, p["plate_hole"] / 2, p["plate_t"] + 2)
        plates.append(pl)
    for a in (90, 210, 330):
        rx = sx + p["rod_pcd"] / 2 * math.cos(math.radians(a))
        ry = p["rod_pcd"] / 2 * math.sin(math.radians(a))
        plates.append(rod((rx, ry, D["shield_top"]), (rx, ry, D["shield_bot"]), p["rod_d"] / 2))
    parts["shield"] = fuse(plates)

    # 3 Air temperature and humidity sensor capsule at the middle of the stack
    cd, cl = p["th_sensor"]
    parts["th_sensor"] = zcyl(sx, 0, D["shield_zc"], cd / 2, cl)

    # 4 Black globe with its top boss (wall drawn thicker than the real 0.4 mm)
    gx, gz, gr = p["globe_x"], D["globe_zc"], p["globe_d"] / 2
    globe = b.Pos(gx, 0, gz) * (b.Sphere(gr) - b.Sphere(gr - p["globe_wall_drawn"]))
    parts["globe"] = globe + zcyl(gx, 0, gz + gr + 4, 10, 16)

    # 5 Globe probe: stiff stem from the boss to a bead at the globe center
    parts["probe"] = rod((gx, 0, gz + gr + 12), (gx, 0, gz), p["probe_d"] / 2) + b.Pos(gx, 0, gz) * b.Sphere(p["bead_d"] / 2)

    # 6 Cup anemometer on a mast at the arm tip
    ax, hz = D["anemo_x"], D["hub_z"]
    an = rod((ax, 0, D["arm_top"]), (ax, 0, hz), p["mast_d"] / 2) + zcyl(ax, 0, hz, 22, 40)
    cr = p["cup_d"] / 2
    for a in (30, 150, 270):
        cx, cy = ax + p["cup_arm"] * math.cos(math.radians(a)), p["cup_arm"] * math.sin(math.radians(a))
        an = an + rod((ax, 0, hz + 10), (cx, cy, hz + 10), 2.5)
        cup = b.Pos(cx, cy, hz + 10) * (b.Sphere(cr) - b.Sphere(cr - 2))
        cut = b.Pos(cx + cr * math.cos(math.radians(a + 90)), cy + cr * math.sin(math.radians(a + 90)), hz + 10) * b.Box(2 * cr, 2 * cr, 2.5 * cr)
        an = an + (cup - cut)
    parts["anemometer"] = an

    # 11 Secondary retention: stainless lanyards from the globe boss and the shield top to the arm
    ld = p["lanyard_d"] / 2
    parts["lanyard"] = (path([(gx + 8, 8, gz + gr + 10), (gx + 30, 14, D["arm_bot"] - 4), (gx + 40, 14, D["arm_bot"])], ld)
                        + path([(sx + 20, 14, D["shield_top"]), (sx + 40, 14, D["arm_bot"])], ld))

    # 9 Sensor harness: two M12 leads from the FieldNode ports, up the pole, along the arm
    ew, ed, eh = p["fn_enc"]
    z0 = p["fn_z0"]
    px1 = p["fn_ports_x"][0]
    yb = D["enc_yc"]
    hy = -r - 6
    harness = path([(px1, yb, z0), (px1, yb, z0 - 50), (px1 + 20, hy, z0 - 50),
                    (px1 + 20, hy, az - 60), (r * 0.7, -r * 0.75, az - 60),
                    (x0 + 10, -18, az - 20), (D["anemo_x"] - 30, -18, az - 20)], 3.5)
    harness = harness + path([(sx + 30, -18, az - 20), (sx + 5, -8, D["shield_top"] - 10)], 2.5)
    harness = harness + path([(gx - 25, -18, az - 20), (gx - 6, -6, gz + p["globe_d"] / 2 + 14)], 2.5)
    harness = harness + path([(D["anemo_x"] - 30, -18, az - 20), (D["anemo_x"] - 8, -8, D["arm_bot"])], 2.5)
    parts["harness"] = harness

    # 1 FieldNode core envelope (FND-DWG-001): back plate, enclosure, panel on two bars, whip
    pw, ph, pt = p["fn_plate"]
    y0 = D["plate_y0"]
    plate = box(0, y0 - pt / 2, z0 - p["fn_plate_drop"] + ph / 2, pw, pt, ph)
    enc = box(0, D["enc_yc"], z0 + eh / 2, ew, ed, eh)
    tilt = p["fn_tilt"]
    panel = b.Pos(0, D["panel_cy"], D["panel_cz"]) * b.Rot(tilt, 0, 0) * b.Box(*p["fn_panel"])
    t = math.radians(tilt)
    bars = fuse(path([(bx, y0 - pt, z0 + 260), (bx, D["panel_cy"] + 80 * math.cos(t), D["panel_cz"] + 80 * math.sin(t) - 10)], 5)
                + path([(bx, y0 - pt, z0 + 210), (bx, D["panel_cy"] - 60 * math.cos(t), D["panel_cz"] - 60 * math.sin(t) - 10)], 5)
                for bx in (-80, 80))
    wd, wl = p["fn_whip"]
    whip = zcyl(58, D["enc_yc"], z0 - wl / 2, wd / 2, wl)
    ports = fuse(zcyl(x, D["enc_yc"], z0 - 8, 11, 16) for x in p["fn_ports_x"])
    parts["fieldnode"] = plate + enc + panel + bars + whip + ports

    # 12 HeatMap pole adapter for the FieldNode core: two wide V-blocks and strap bands
    vw, vh, vd = p["adapter_vblock"]
    blocks = []
    for dz in p["adapter_dz"]:
        z = z0 + dz
        blk = box(0, -r - vd / 2, z, vw, vd, vh) - zcyl(0, 0, z, r + 0.5, vh + 2)
        blocks.append(blk + band(z, r, p["band_w"]))
    parts["adapter"] = fuse(blocks)
    return parts


BOM = {  # model key: (BOM line, name)
    "fieldnode": (1, "FieldNode core (FND-DWG-001 envelope)"),
    "shield": (2, "Multi-plate radiation shield"),
    "th_sensor": (3, "Air temperature and humidity sensor"),
    "globe": (4, "Black globe, 150 mm"),
    "probe": (5, "Globe temperature probe"),
    "anemometer": (6, "Cup anemometer"),
    "arm": (7, "Sensor arm"),
    "clamp": (8, "Arm clamp and bands"),
    "harness": (9, "Sensor harness, M12"),
    "lanyard": (11, "Secondary retention lanyards"),
    "adapter": (12, "FieldNode pole adapter"),
}
HEAD = ["shield", "th_sensor", "globe", "probe", "anemometer", "arm", "clamp", "harness", "lanyard"]


def pole_context(p=PARAMS):
    """Existing street pole (not supplied, not in the BOM)."""
    return zcyl(0, 0, p["pole_h"] / 2, p["pole_od"] / 2, p["pole_h"])


def assembly(p=PARAMS, with_pole=False):
    b = _b3d()
    parts = build_parts(p)
    kids = list(parts.values()) + ([pole_context(p)] if with_pole else [])
    return b.Compound(children=kids)


if __name__ == "__main__":
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
        export_stl(c, str(out / "stl" / f"{name}.stl"))
        bb = c.bounding_box()
        print(f"{name}: {bb.size.X:.0f} x {bb.size.Y:.0f} x {bb.size.Z:.0f} mm")
    D = derived()
    print(f"arm axis {PARAMS['arm_z']:.0f} mm; shield center {D['shield_zc']:.0f} mm; globe center {D['globe_zc']:.0f} mm; "
          f"cups {D['cup_z']:.0f} mm; reach {D['reach']:.0f} mm from the pole axis; top {D['overall_top']:.0f} mm")
