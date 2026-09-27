"""HeatMap Node product appearance model (build123d), TRL 3.

Finished-product look for photoreal renders: a filleted aluminium sensor arm with an end cap and
an identity label; the formed V-saddle with stainless strap bands, buckles and bolt heads; the
eight-plate white radiation shield on stainless rods with nuts, the aspiration fan (frame, hub and
blades) in its cowl, and the temperature and humidity capsule with its PTFE membrane cap inside
the stack; the matte black globe with its seam flange, boss and gland, and the probe inside it;
the cup anemometer with a teal rotor cap; the M12 harness with plugs and cable ties, and the
stainless retention lanyards. Below the arm sits the FieldNode core envelope: back plate,
enclosure with a lid parting line and lid screws, the board and LiFePO4 cell inside it, the white
sun shield with a name plate, the tilted solar panel with cells, busbars and junction box, the
whip antenna, M12 sockets and a vent plug, all on the HeatMap pole adapter. Context is a short
section of the existing street pole.
APPEARANCE MODEL ONLY: no tolerances, no fabrication detail. CONCEPT, NOT FOR FABRICATION.

Every main dimension, height and interface comes from PARAMS, derived() and build_parts() in
model.py, with the same axes: the pole is the Z axis, Z up with the pavement at z = 0, the arm
along +X (toward the equator), front is -Y. The FieldNode board and cell are appearance stand-ins
for parts defined in the FieldNode repo. See docs/REVIEW.md, session 2026-09-26.

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import Axis, Box, Cylinder, Pos, RegularPolygon, Rot, Sphere, extrude, fillet
from model import PARAMS, derived, path, rod

TITLE = "HeatMap Node: street-pole heat stress sensor with a black globe thermometer"

RENDER_VIEWS = [
    {"name": "hero", "groups": ["shell", "internal", "accessory", "context"], "explode": False, "el": 30, "az": -40,
     "note": "Product render from the front right and above (about 30 deg elevation); sensor arm on a short "
             "section of street pole with the radiation shield, the black globe and the anemometer, and the "
             "FieldNode solar core below"},
    {"name": "exploded", "groups": ["shell", "internal"], "explode": True, "el": 28, "az": -55,
     "note": "Exploded view from the front right and above (about 28 deg elevation): shield plates, fan and "
             "cowl, humidity sensor, black globe and probe, anemometer, arm and clamp; FieldNode core with "
             "sun shield, lid, battery, board and pole adapter"},
    {"name": "detail", "groups": ["shell", "internal", "accessory"], "explode": False, "el": 16, "az": -35,
     "note": "Detail from the front right, slightly above (about 16 deg elevation), without the pole: "
             "radiation shield, black globe and humidity sensor under the arm, FieldNode core below"},
]

# Colours (restrained product palette; kit accent)
C_WHITE = "#F1F1EE"
C_SHELL = "#D6D9DC"
C_SHELL2 = "#BFC4C9"
C_ALU = "#C3C8CE"
C_STEEL = "#B3B9C0"
C_DARK = "#2B2F36"
C_BLACK = "#1C1F24"
C_GLOBE = "#141619"
C_RUBBER = "#202327"
C_ACCENT = "#0F766E"
C_LABEL = "#F4F4F2"
C_PCB = "#166534"
C_CHIP = "#111827"
C_CELL = "#2F5F8A"
C_PV = "#1B2A44"
C_EPOXY = "#5B3A1E"
C_MEMBRANE = "#FAFAF7"
C_ASA = "#3A3F45"
C_POLE = "#A3A9AF"

POLE_Z = (1900.0, 3080.0)      # shown pole section (context), bottom and top


def _fillet_try(shape, edges, radii):
    """Fillet `edges` with the first radius that gives a valid solid; else return the input."""
    edges = list(edges)
    if not edges:
        return shape
    for r in radii:
        try:
            out = fillet(edges, r)
            if out.is_valid and out.volume > 0:
                return out
        except Exception:
            pass
    return shape


def _box(cx, cy, cz, sx, sy, sz):
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def _zcyl(x, y, z, r, h):
    return Pos(x, y, z) * Cylinder(r, h)


def _ycyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(90, 0, 0) * Cylinder(r, h)


def _xcyl(x, y, z, r, h):
    return Pos(x, y, z) * Rot(0, 90, 0) * Cylinder(r, h)


def _hex_z(x, y, z, af, h):
    return Pos(x, y, z - h / 2) * extrude(RegularPolygon(af / 1.732, 6), amount=h)


def _hex_x(x, y, z, af, length):
    return Pos(x, y, z) * Rot(0, 90, 0) * Pos(0, 0, -length / 2) * extrude(RegularPolygon(af / 1.732, 6), amount=length)


def _pipe(points, r):
    """Round tube through `points` with spherical joints (clean bends), as model.path."""
    out = path(points, r)
    for q in points[1:-1]:
        out += Pos(*q) * Sphere(r)
    return out


def _union(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def _par(s, axis):
    return s.edges().filter_by(axis)


def _top(s):
    return s.faces().sort_by(Axis.Z)[-1].edges()


def _bottom(s):
    return s.faces().sort_by(Axis.Z)[0].edges()


def _ring(z, r, w, t=1.5):
    return _zcyl(0, 0, z, r + t, w) - _zcyl(0, 0, z, r, w + 2)


def product_parts(P=PARAMS):
    D = derived(P)
    r = D["r"]
    az = P["arm_z"]
    out = []

    def add(name, shape, color, material, bom, group, explode):
        out.append({"name": name, "shape": shape, "color": color, "material": material,
                    "bom": bom, "group": group, "explode": tuple(float(v) for v in explode)})

    # ------------------------------------------------------------ arm clamp and bands (BOM 8)
    EC = (-120, 0, 0)
    sw, sh, sd = P["saddle"]
    wt = P["saddle_wall"]
    sad = _box(r + sd / 2, 0, az, sd, sw, sh)
    sad = _fillet_try(sad, _par(sad, Axis.X), [5.0, 3.0, 2.0])
    sad = _fillet_try(sad, sad.faces().sort_by(Axis.X)[-1].edges(), [1.5, 1.0])
    sad -= _box(r + (sd - wt) / 2 - 1, 0, az, sd - wt + 2, sw - 2 * wt, sh - 2 * wt)
    sad -= _zcyl(0, 0, az, r + 0.5, sh + 2)
    add("Arm clamp V-saddle (formed aluminium)", sad, C_ALU, "metal", 8, "shell", EC)
    liner = (_zcyl(0, 0, az, r + 0.5, sh - 8) - _zcyl(0, 0, az, r - 0.01, sh)) & _box(r, 0, az, 40, sw - 2 * wt, sh)
    add("Clamp rubber liner", liner, C_RUBBER, "rubber", 8, "shell", (-80, 0, 0))
    bands = None
    for dz in (-P["band_dz"], P["band_dz"]):
        z = az + dz
        bnd = _ring(z, r, P["band_w"])
        buckle = _box(-r - 5, 0, z, 8, 18, P["band_w"] + 3)
        buckle = _fillet_try(buckle, _par(buckle, Axis.Z), [2.0, 1.0])
        screw = _ycyl(-r - 7, -12, z, 3.2, 10)
        bnd = bnd + buckle + screw
        bands = bnd if bands is None else bands + bnd
    add("Clamp strap bands and buckles (316 stainless)", bands, C_STEEL, "metal", 8, "shell", (-200, 0, 0))
    bolts = _union(_hex_x(r + sd + 2.5, 0, az + s * 55, 10.0, 5.0) for s in (-1, 1))
    add("Clamp bolt heads", bolts, C_STEEL, "metal", 10, "shell", (-60, 0, 0))

    # ------------------------------------------------------------ sensor arm (BOM 7)
    x0, x1, w = D["arm_x0"], D["arm_x1"], P["arm_w"]
    tube = _box((x0 + x1) / 2, 0, az, x1 - x0, w, w)
    tube = _fillet_try(tube, _par(tube, Axis.X), [2.5, 1.5, 1.0])
    tube -= _box((x0 + x1) / 2 + 1, 0, az, x1 - x0 + 4, w - 2 * P["arm_t"], w - 2 * P["arm_t"])
    add("Sensor arm (25 mm aluminium tube)", tube, C_ALU, "metal", 7, "shell", (0, 0, 0))
    cap = _box(x1 + 1.25, 0, az, 2.5, w + 1, w + 1)
    cap = _fillet_try(cap, _par(cap, Axis.X), [3.0, 2.0])
    cap = _fillet_try(cap, cap.faces().sort_by(Axis.X)[-1].edges(), [1.0, 0.6])
    add("Arm end cap", cap, C_BLACK, "plastic", 7, "shell", (40, 0, 0))
    hang = rod((P["shield_x"], 0, D["arm_bot"]), (P["shield_x"], 0, D["cowl_top"]), 6)
    hang += rod((P["globe_x"], 0, D["arm_bot"]), (P["globe_x"], 0, D["globe_zc"] + P["globe_d"] / 2 + 12), 6)
    hang += _hex_z(P["shield_x"], 0, D["arm_bot"] - 2.5, 13.0, 5.0) + _hex_z(P["globe_x"], 0, D["arm_bot"] - 2.5, 13.0, 5.0)
    add("Shield and globe hangers", hang, C_STEEL, "metal", 7, "shell", (0, 0, 0))
    lab = _box(200, -w / 2 - 0.2, az, 70, 0.4, 16)
    add("Arm identity label", lab, C_LABEL, "paper", 7, "shell", (0, -40, 0))
    band = _box(173, -w / 2 - 0.4, az, 12, 0.4, 16)
    add("Arm label accent", band, C_ACCENT, "painted", 7, "shell", (0, -40, 0))
    ink = _box(208, -w / 2 - 0.45, az + 3, 40, 0.3, 3.5) + _box(203, -w / 2 - 0.45, az - 3, 30, 0.3, 2)
    add("Arm label print", ink, C_DARK, "paper", 7, "shell", (0, -40, 0))

    # ------------------------------------------------------------ radiation shield (BOM 2)
    sx, sr = P["shield_x"], P["shield_d"] / 2
    for i in range(P["n_plates"]):
        z = D["shield_top"] - P["plate_t"] / 2 - i * P["plate_pitch"]
        pl = _zcyl(sx, 0, z, sr, P["plate_t"])
        pl = _fillet_try(pl, pl.edges(), [1.2, 0.8, 0.5])
        pl -= _zcyl(sx, 0, z, (P["plate_hole"] if i else P["top_hole"]) / 2, P["plate_t"] + 2)
        add(f"Shield plate {i + 1}", pl, C_WHITE, "plastic", 2, "shell", (0, 0, -150 - 28 * i))
    rods = None
    for a in (90, 210, 330):
        rx = sx + P["rod_pcd"] / 2 * math.cos(math.radians(a))
        ry = P["rod_pcd"] / 2 * math.sin(math.radians(a))
        rr = rod((rx, ry, D["shield_top"] + 3), (rx, ry, D["shield_bot"] - 2), P["rod_d"] / 2)
        rr += _hex_z(rx, ry, D["shield_top"] + 2, 8.0, 4.0)
        rr += _zcyl(rx, ry, D["shield_bot"] - 2.5, 4.6, 4.0) + Pos(rx, ry, D["shield_bot"] - 4.5) * Sphere(4.0)
        rods = rr if rods is None else rods + rr
    add("Shield rods and nuts (M5 stainless)", rods, C_STEEL, "metal", 2, "shell", (0, -170, -290))

    # ------------------------------------------------------------ aspiration fan and cowl (BOM 13)
    cw, ch = P["cowl"]
    fw, _, fh = P["fan"]
    zt = D["shield_top"]
    lid = _box(sx, 0, zt + ch - 1.5, cw, cw, 3.0)
    lid = _fillet_try(lid, _par(lid, Axis.Z), [6.0, 4.0])
    lid = _fillet_try(lid, _top(lid), [1.0, 0.6])
    posts = _union(_box(sx + ex * (cw / 2 - 4), ey * (cw / 2 - 4), zt + (ch - 3) / 2, 8, 8, ch - 3)
                   for ex in (-1, 1) for ey in (-1, 1))
    add("Fan cowl (white ASA)", lid + posts, C_WHITE, "plastic", 13, "shell", (0, 0, -70))
    fz = zt + fh / 2 + 1
    frame = _box(sx, 0, fz, fw, fw, fh)
    frame = _fillet_try(frame, _par(frame, Axis.Z), [3.0, 2.0])
    frame -= _zcyl(sx, 0, fz, fw / 2 - 3, fh + 2)
    for ex in (-1, 1):
        for ey in (-1, 1):
            frame -= _zcyl(sx + ex * 25, ey * 25, fz, 2.2, fh + 2)
    add("Aspiration fan frame", frame, C_BLACK, "plastic", 13, "shell", (0, 0, -110))
    rotor = _zcyl(sx, 0, fz, 12, fh - 1)
    rotor = _fillet_try(rotor, _top(rotor), [2.0, 1.0])
    for k in range(7):
        blade = Pos(sx, 0, fz) * Rot(0, 0, k * 360 / 7) * Pos(19.5, 0, 0) * Rot(28, 0, 0) * Box(16, 11, 1.2)
        rotor += blade
    add("Aspiration fan rotor", rotor, C_DARK, "plastic", 13, "shell", (0, 0, -110))
    fl = _zcyl(sx, 0, fz + fh / 2 - 0.3, 7.0, 0.6)
    add("Fan hub label", fl, C_ACCENT, "painted", 13, "shell", (0, 0, -110))

    # ------------------------------------------------------------ temperature and humidity sensor (BOM 3)
    cd, cl = P["th_sensor"]
    zc = D["shield_zc"]
    body = _zcyl(sx, 0, zc + 4, cd / 2, cl - 8)
    body = _fillet_try(body, _bottom(body), [1.0, 0.5])
    add("Temperature and humidity capsule", body, C_SHELL, "plastic", 3, "internal", (0, 0, -520))
    mem = _zcyl(sx, 0, zc - cl / 2 + 4, cd / 2 - 1.5, 8)
    mem = _fillet_try(mem, _bottom(mem), [2.5, 1.5])
    add("PTFE membrane cap", mem, C_MEMBRANE, "fabric", 3, "internal", (0, 0, -540))
    m12 = _zcyl(sx, 0, zc + cl / 2 + 3, 7.0, 6) + _zcyl(sx, 0, zc + cl / 2 + 8, 5.5, 4)
    add("Sensor M12 connector", m12, C_STEEL, "metal", 3, "internal", (0, 0, -520))

    # ------------------------------------------------------------ black globe (BOM 4) and probe (BOM 5)
    gx, gz, gr = P["globe_x"], D["globe_zc"], P["globe_d"] / 2
    EG = (0, 0, -220)
    globe = Pos(gx, 0, gz) * (Sphere(gr) - Sphere(gr - P["globe_wall_drawn"]))
    seam = _zcyl(gx, 0, gz, gr + 1.2, 3.0) - _zcyl(gx, 0, gz, gr - 3, 4.0)
    seam = _fillet_try(seam, _par(seam, Axis.Z) or seam.edges(), [0.8, 0.5])
    add("Black globe (matte black copper sphere)", globe + seam, C_GLOBE, "painted", 4, "shell", EG)
    boss = _zcyl(gx, 0, gz + gr + 4, 10, 16)
    boss = _fillet_try(boss, _top(boss), [1.5, 1.0])
    add("Globe boss (brass)", boss, "#B89B5E", "metal", 4, "shell", EG)
    gland = _hex_z(gx, 0, gz + gr + 14, 14.0, 4.0) + (Pos(gx, 0, gz + gr + 16) * Sphere(6.0) & _box(gx, 0, gz + gr + 19, 14, 14, 6))
    add("Globe probe gland", gland, C_BLACK, "plastic", 4, "shell", (0, 0, -40))
    probe = rod((gx, 0, gz + gr + 12), (gx, 0, gz), P["probe_d"] / 2)
    add("Globe probe stem (stainless)", probe, C_STEEL, "metal", 5, "internal", (0, 0, -40))
    bead = Pos(gx, 0, gz) * Sphere(P["bead_d"] / 2)
    add("Globe probe bead (NTC)", bead, C_EPOXY, "plastic", 5, "internal", (0, 0, -40))

    # ------------------------------------------------------------ cup anemometer (BOM 6)
    ax, hz = D["anemo_x"], D["hub_z"]
    EA = (0, 0, 110)
    mast = rod((ax, 0, D["arm_top"]), (ax, 0, hz - 20), P["mast_d"] / 2)
    mast += _zcyl(ax, 0, D["arm_top"] + 2, 14, 4)
    add("Anemometer mast", mast, C_ALU, "metal", 6, "shell", (0, 0, 60))
    hous = _zcyl(ax, 0, hz - 8, 22, 24)
    hous = _fillet_try(hous, _bottom(hous), [4.0, 2.5])
    hous = _fillet_try(hous, _top(hous), [1.0, 0.5])
    add("Anemometer body", hous, C_WHITE, "plastic", 6, "shell", EA)
    hub = _zcyl(ax, 0, hz + 12, 16, 16)
    hub = _fillet_try(hub, _top(hub), [5.0, 3.0])
    add("Anemometer rotor cap", hub, C_ACCENT, "plastic", 6, "shell", (0, 0, 160))
    cr = P["cup_d"] / 2
    cups = None
    for a in (30, 150, 270):
        cx, cy = ax + P["cup_arm"] * math.cos(math.radians(a)), P["cup_arm"] * math.sin(math.radians(a))
        c = rod((ax, 0, hz + 10), (cx, cy, hz + 10), 2.5)
        cup = Pos(cx, cy, hz + 10) * (Sphere(cr) - Sphere(cr - 2))
        cut = Pos(cx + cr * math.cos(math.radians(a + 90)), cy + cr * math.sin(math.radians(a + 90)), hz + 10) * Box(2 * cr, 2 * cr, 2.5 * cr)
        c += cup - cut
        cups = c if cups is None else cups + c
    add("Anemometer cups and spokes", cups, C_WHITE, "plastic", 6, "shell", (0, 0, 160))

    # ------------------------------------------------------------ harness, ties and lanyards (BOM 9, 10, 11)
    z0 = P["fn_z0"]
    px1 = P["fn_ports_x"][0]
    yb = D["enc_yc"]
    hy = -r - 6
    pts = [(-yb, px1, z0 - 30), (-yb, px1, z0 - 50), (20, hy, z0 - 50),
           (20, hy, az - 60), (r * 0.7, -r * 0.75, az - 60),
           (x0 + 10, -18, az - 20), (D["anemo_x"] - 30, -18, az - 20)]
    harness = _pipe(pts, 3.5)
    harness += _pipe([(sx + 30, -18, az - 20), (sx + 5, -20, D["cowl_top"] + 2), (sx + 5, -20, D["shield_top"] - 10)], 2.5)
    harness += _pipe([(gx - 25, -18, az - 20), (gx - 6, -6, gz + gr + 14)], 2.5)
    harness += _pipe([(D["anemo_x"] - 30, -18, az - 20), (D["anemo_x"] - 8, -8, D["arm_bot"])], 2.5)
    add("Sensor harness (M12 leads)", harness, C_RUBBER, "rubber", 9, "accessory", (0, 0, 0))
    plug = _zcyl(-yb, px1, z0 - 23, 8.0, 14)
    plug = _fillet_try(plug, _bottom(plug), [2.0, 1.0])
    plug += _zcyl(-yb, px1, z0 - 12, 9.0, 8)
    add("Harness M12 plug", plug, C_STEEL, "metal", 9, "accessory", (0, 0, 0))
    ties = None
    for tx in (130, 230, 400, 540):
        t = _box(tx, -4.5, az - 2, 4, 36, 34) - _box(tx, -4.5, az - 2, 6, 33, 31)
        ties = t if ties is None else ties + t
    add("Cable ties", ties, C_BLACK, "plastic", 10, "accessory", (0, 0, 0))
    ld = P["lanyard_d"] / 2
    lany = _pipe([(gx + 8, 8, gz + gr + 10), (gx + 30, 14, D["arm_bot"] - 4), (gx + 40, 14, D["arm_bot"])], ld)
    lany += _pipe([(sx + 20, 44, D["shield_top"]), (sx + 44, 44, D["arm_bot"] - 4), (sx + 50, 14, D["arm_bot"])], ld)
    add("Retention lanyards (316 stainless)", lany, C_STEEL, "metal", 11, "accessory", (0, 0, 0))

    # ------------------------------------------------------------ FieldNode core envelope (BOM 1)
    # Built in the FieldNode convention (panel facing -Y) and turned by fn_azimuth, as model.py.
    turn = Rot(0, 0, P["fn_azimuth"])
    FN = (-360.0, 0.0, -260.0)                           # whole core, exploded clear of the head

    def fn(dx_out=0.0, dz=0.0, dy=0.0):
        """Explode offset for a FieldNode part: dx_out along the panel direction (world +X)."""
        return (FN[0] + dx_out, FN[1] + dy, FN[2] + dz)

    ew, ed, eh = P["fn_enc"]
    pw, ph, pt = P["fn_plate"]
    y0 = D["plate_y0"]
    eb, ef, eyc = D["enc_back"], D["enc_front"], D["enc_yc"]

    plate = _box(0, y0 - pt / 2, z0 - P["fn_plate_drop"] + ph / 2, pw, pt, ph)
    plate = _fillet_try(plate, _par(plate, Axis.Y), [8.0, 5.0])
    for ex in (-1, 1):
        for ez in (z0 - 20, z0 + 250):
            plate -= _ycyl(ex * 75, y0 - pt / 2, ez, 3.0, pt + 2)
    add("FieldNode back plate", turn * plate, C_STEEL, "metal", 1, "shell", fn(-60))

    lid_t = 14.0
    base = _box(0, (eb + ef + lid_t) / 2, z0 + eh / 2, ew, ed - lid_t, eh)
    base = _fillet_try(base, _par(base, Axis.Y), [7.0, 5.0, 3.0])
    base -= _box(0, (eb + ef + lid_t) / 2 - 2, z0 + eh / 2, ew - 5, ed - lid_t, eh - 5)
    add("FieldNode enclosure base", turn * base, C_SHELL, "plastic", 1, "shell", fn(0))
    lid = _box(0, ef + lid_t / 2, z0 + eh / 2, ew, lid_t, eh)
    lid = _fillet_try(lid, _par(lid, Axis.Y), [7.0, 5.0, 3.0])
    lid = _fillet_try(lid, lid.faces().sort_by(Axis.Y)[0].edges(), [2.5, 1.5])
    lid -= _box(0, ef + lid_t / 2 + 2, z0 + eh / 2, ew - 5, lid_t, eh - 5)
    lid -= _box(0, ef + lid_t - 1.0, z0 + eh / 2, ew + 2, 1.2, eh + 2) - _box(0, ef + lid_t - 1.0, z0 + eh / 2, ew - 1.4, 2, eh - 1.4)
    add("FieldNode enclosure lid", turn * lid, C_SHELL2, "plastic", 1, "shell", fn(260))
    lscr = None
    for ex in (-1, 1):
        for ez in (-1, 1):
            s = _ycyl(ex * (ew / 2 - 10), ef - 0.5, z0 + eh / 2 + ez * (eh / 2 - 10), 3.2, 1.2)
            s -= _box(ex * (ew / 2 - 10), ef - 1.1, z0 + eh / 2 + ez * (eh / 2 - 10), 4.0, 1.0, 0.8)
            lscr = s if lscr is None else lscr + s
    add("FieldNode lid screws", turn * lscr, C_STEEL, "metal", 1, "shell", fn(290))

    # board and cell inside (appearance stand-ins; defined in the FieldNode repo)
    by = eb - 12
    pcb = _box(0, by, z0 + eh / 2, ew - 20, 1.6, eh - 24)
    pcb = _fillet_try(pcb, _par(pcb, Axis.Y), [3.0, 2.0])
    add("FieldNode power and radio board", turn * pcb, C_PCB, "plastic", 1, "internal", fn(90))
    comps = (_box(-30, by - 3.8, z0 + 150, 30, 6, 22) + _box(30, by - 2.3, z0 + 150, 26, 3, 20)
             + _box(35, by - 4.3, z0 + 105, 18, 7, 18) + _box(-40, by - 2.8, z0 + 40, 20, 4, 14))
    add("FieldNode board components", turn * comps, C_CHIP, "plastic", 1, "internal", fn(90))
    can = _box(30, by - 4.2, z0 + 150, 24, 0.8, 18)
    add("LoRaWAN module shield can", turn * can, C_STEEL, "metal", 1, "internal", fn(90))
    cz = z0 + 75
    cell = _xcyl(0, by - 22, cz, 16.0, 62)
    add("LiFePO4 cell (3.2 V 6 Ah)", turn * cell, C_CELL, "plastic", 1, "internal", fn(170))
    ends = _xcyl(-32.5, by - 22, cz, 11.0, 3.0) + _xcyl(32.5, by - 22, cz, 11.0, 3.0)
    add("Cell terminals", turn * ends, C_STEEL, "metal", 1, "internal", fn(170))
    clab = (_xcyl(0, by - 22, cz, 16.3, 26) - _xcyl(0, by - 22, cz, 15.0, 30)) & _box(0, by - 22 - 12, cz, 30, 12, 40)
    add("Cell wrap label", turn * clab, C_LABEL, "paper", 1, "internal", fn(170))

    # hot-climate sun shield (front, sides, top, stood off the enclosure)
    st, sg = P["fns_t"], P["fns_gap"]
    yb_s, yf_s = y0 - pt, ef - sg
    xo = ew / 2 + sg
    zlo, zhi = z0 + P["fns_low"], z0 + eh + sg
    hs = zhi - zlo
    shield = _box(0, yf_s - st / 2, zlo + hs / 2, 2 * (xo + st), st, hs)
    for sxn in (-1, 1):
        shield += _box(sxn * (xo + st / 2), (yb_s + yf_s - st) / 2, zlo + hs / 2, st, yb_s - (yf_s - st), hs)
    shield += _box(0, (yf_s - st + yb_s - P["fns_slot"]) / 2, zhi + st / 2, 2 * (xo + st),
                   yb_s - P["fns_slot"] - (yf_s - st), st)
    for k in range(4):                                   # vent slots in the sides
        for sxn in (-1, 1):
            shield -= _box(sxn * (xo + st / 2), (yb_s + yf_s) / 2, zlo + 40 + 40 * k, 4, 60, 8)
    add("FieldNode sun shield (white)", turn * shield, C_WHITE, "painted", 1, "shell", fn(400))
    fy = yf_s - st
    npl = _box(0, fy - 0.2, zlo + hs * 0.62, 110, 0.4, 36)
    add("Name plate", turn * npl, C_LABEL, "paper", 1, "shell", fn(400))
    nacc = _box(0, fy - 0.4, zlo + hs * 0.62 + 14, 110, 0.4, 8)
    add("Name plate accent", turn * nacc, C_ACCENT, "painted", 1, "shell", fn(400))
    nink = (_box(-18, fy - 0.45, zlo + hs * 0.62 + 1, 64, 0.3, 7)
            + _box(-28, fy - 0.45, zlo + hs * 0.62 - 9, 44, 0.3, 3))
    add("Name plate print", turn * nink, C_DARK, "paper", 1, "shell", fn(400))

    # solar panel (sun hood) on its two bars
    T = Pos(0, D["panel_cy"], D["panel_cz"]) * Rot(P["fn_tilt"], 0, 0)
    px_, py_, pz_ = P["fn_panel"]
    frame = Box(px_, py_, pz_)
    frame = _fillet_try(frame, _par(frame, Axis.Z), [4.0, 2.0])
    frame -= Pos(0, 0, pz_ / 2) * Box(px_ - 16, py_ - 16, 8)
    add("Solar panel frame", turn * T * frame, C_ALU, "metal", 1, "shell", fn(0, 150))
    cells = Pos(0, 0, pz_ / 2 - 3.6) * Box(px_ - 16, py_ - 16, 0.8)
    add("Solar cells", turn * T * cells, C_PV, "screen", 1, "shell", fn(0, 150))
    nx, ny = 6, 4
    cwid, chei = (px_ - 16) / nx, (py_ - 16) / ny
    grid = None
    for i in range(1, nx):
        g = Pos(-(px_ - 16) / 2 + i * cwid, 0, pz_ / 2 - 3.1) * Box(1.2, py_ - 16, 0.3)
        grid = g if grid is None else grid + g
    for j in range(1, ny):
        grid += Pos(0, -(py_ - 16) / 2 + j * chei, pz_ / 2 - 3.1) * Box(px_ - 16, 1.2, 0.3)
    add("Solar cell gaps and busbars", turn * T * grid, "#C9CED6", "metal", 1, "shell", fn(0, 150))
    jb = Pos(0, 20, -pz_ / 2 - 6) * Box(60, 40, 12)
    jb = _fillet_try(jb, jb.edges(), [2.0, 1.0])
    add("Panel junction box", turn * T * jb, C_BLACK, "plastic", 1, "shell", fn(0, 150))
    t = math.radians(P["fn_tilt"])
    bars = _union(_pipe([(bx, y0 - pt, z0 + 260), (bx, D["panel_cy"] + 80 * math.cos(t), D["panel_cz"] + 80 * math.sin(t) - 10)], 5)
                  + _pipe([(bx, y0 - pt, z0 + 210), (bx, D["panel_cy"] - 60 * math.cos(t), D["panel_cz"] - 60 * math.sin(t) - 10)], 5)
                  for bx in (-80, 80))
    add("Panel support bars", turn * bars, C_STEEL, "metal", 1, "shell", fn(0, 75))

    # whip antenna, M12 sockets, vent plug
    wd, wl = P["fn_whip"]
    whip = _zcyl(58, eyc, z0 - wl / 2 - 6, wd / 2, wl - 12)
    whip = _fillet_try(whip, _bottom(whip), [4.0, 2.5])
    add("Whip antenna", turn * whip, C_BLACK, "rubber", 1, "shell", fn(0, -40))
    wn = _hex_z(58, eyc, z0 - 4, 16.0, 8.0)
    add("Antenna base nut", turn * wn, C_STEEL, "metal", 1, "shell", fn(0, -40))
    socks = _union(_zcyl(x, eyc, z0 - 4, 10.5, 8) + _hex_z(x, eyc, z0 - 1.5, 22.0, 3.0) for x in P["fn_ports_x"])
    add("M12 sensor sockets", turn * socks, C_STEEL, "metal", 1, "shell", fn(0))
    vent = _zcyl(20, eyc, z0 - 4, 7.0, 8)
    vent = _fillet_try(vent, _bottom(vent), [2.0, 1.0])
    add("Enclosure vent plug", turn * vent, C_DARK, "plastic", 1, "shell", fn(0))

    # ------------------------------------------------------------ FieldNode pole adapter (BOM 12)
    vw, vh, vd = P["adapter_vblock"]
    blocks, straps = [], []
    for dz in P["adapter_dz"]:
        z = z0 + dz
        blk = _box(0, -r - vd / 2, z, vw, vd, vh)
        blk = _fillet_try(blk, _par(blk, Axis.Y), [3.0, 2.0])
        blk -= _zcyl(0, 0, z, r + 0.5, vh + 2)
        blocks.append(blk)
        s = _ring(z, r, P["band_w"]) + _box(0, r + 5, z, 18, 8, P["band_w"] + 3)
        straps.append(s + _xcyl(12, r + 7, z, 3.2, 10))
    add("Pole adapter V-blocks (ASA)", turn * _union(blocks), C_ASA, "plastic", 12, "shell", fn(-140))
    add("Pole adapter strap bands", turn * _union(straps), C_STEEL, "metal", 12, "shell", fn(-220))

    # ------------------------------------------------------------ context: existing street pole
    zb, ztp = POLE_Z
    pole = _zcyl(0, 0, (zb + ztp) / 2, r, ztp - zb)
    pole = _fillet_try(pole, _top(pole), [3.0, 1.5])
    add("Existing street pole (section, not supplied)", pole, C_POLE, "metal", None, "context", (0, 0, 0))
    return out


if __name__ == "__main__":
    for p in product_parts():
        s = p["shape"]
        print(f"{p['name']:46s} {p['group']:9s} {p['material']:8s} valid={s.is_valid} vol={s.volume / 1000:9.2f} cm3")
