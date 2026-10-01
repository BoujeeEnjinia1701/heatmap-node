"""HeatMap Node prototype build plan pictures (HMN-BLD-001, STANDARDS section 18).

Run from the repo root:  python cad/src/build_plan_media.py [overview|sheets|joints|steps|layouts ...]
With no argument it draws everything. Each picture can also be drawn alone, which keeps memory
low: python cad/src/build_plan_media.py steps 3   (step 3 only), joints 2, sheets 101.
Every picture is drawn from cad/src/model.py (build_components), so the pictures and the model
never disagree:
    docs/05-build-plan/overview.png        every component pulled apart, numbered in build order
    cad/drawings/HMN-DWG-101 to 107        making sketches for the made components
    docs/05-build-plan/joint-NN.png        close-ups of the joints that need explaining
    docs/05-build-plan/step-NN.png         one picture per assembly step
    docs/05-build-plan/arm-holes.png       hole positions along the arm (matplotlib)
Uses .kit/build_views.py. BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT.
"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
import build_views as bv  # noqa: E402
from build_views import Part  # noqa: E402
from model import PARAMS as P, build_components, derived, pole_context, fuse  # noqa: E402

OUT = ROOT / "docs" / "05-build-plan"
DWG = ROOT / "cad" / "drawings"
DATE = "2026-10-01"
D = derived(P)
C = build_components(P)
S = lambda *ks: fuse(C[k].shape for k in ks)  # noqa: E731
AZ = P["arm_z"]
SX, GX, AX = P["shield_x"], P["globe_x"], D["anemo_x"]
ST = D["shield_top"]
Z0 = P["fn_z0"]

COL = {"saddle": "#B45309", "trim": "#111827", "cheeks": "#1D4ED8", "arm": "#94A3B8", "plug": "#111827",
       "plates": "#E7E5E4", "rods": "#374151", "spacers": "#0E7490", "fan": "#1F2937", "cowl": "#0F766E",
       "th": "#0EA5E9", "globe": "#1F2937", "hanger": "#D4A017", "probe": "#C2410C", "anemo": "#0F766E",
       "lanyard": "#B45309", "harness": "#111827", "vblocks": "#7C3AED", "fieldnode": "#CBD5E1",
       "bands": "#6B7280", "bolt": "#111827", "pole": "#9CA3AF"}


def part(name, shape, color, explode=(0, 0, 0), alpha=1.0):
    return Part(name, shape, color, None, tuple(explode), alpha)


def pole(z_lo, z_hi):
    return part("Existing pole (not supplied)", pole_context(P, z_lo, z_hi), COL["pole"])


def win(sh, x0, x1, y0, y1, z0_, z1_):
    import build123d as b
    return sh & (b.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0_ + z1_) / 2) * b.Box(x1 - x0, y1 - y0, z1_ - z0_))


def one_plate(i):
    """Plate i of the stack (0 is the top plate), with the bosses that stand on it."""
    z_top = ST - i * P["plate_pitch"]
    return win(C["plates"].shape, SX - 60, SX + 60, -60, 60, z_top - P["plate_t"] + 0.002, z_top + P["plate_pitch"] - P["plate_t"] - 0.01)


def web_screws():
    """The four M6 button-head screws that hold the cheeks to the saddle web."""
    cb = C["clamp_bolts"].shape
    return win(cb, 40, 100, -60, 60, AZ + 15, AZ + 35) + win(cb, 40, 100, -60, 60, AZ - 35, AZ - 15)


def arm_bolts():
    """The two M6 bolts through the cheeks and the arm."""
    return win(C["clamp_bolts"].shape, 80, 130, -40, 40, AZ - 10, AZ + 10)


# ----------------------------------------------------------------- named parts, in build order
def made():
    return {
        "saddle": part("Arm saddle", C["saddle"].shape, COL["saddle"]),
        "trim": part("Rubber edge trim", C["trim"].shape, COL["trim"]),
        "cheeks": part("Arm cheeks (2) and their screws", C["cheeks"].shape + web_screws(), COL["cheeks"]),
        "arm": part("Sensor arm, plug, sleeves, bolts", S("arm", "plug", "sleeves") + arm_bolts(), COL["arm"]),
        "plates": part("Shield plates (8)", C["plates"].shape, COL["plates"]),
        "rods": part("Shield rods (4), nuts, spacers", S("rods", "spacers"), COL["rods"]),
        "th": part("Temperature and humidity sensor", C["th_sensor"].shape, COL["th"]),
        "fan": part("Aspiration fan", C["fan"].shape, COL["fan"]),
        "cowl": part("Fan cowl and screws", S("cowl", "fan_screws"), COL["cowl"]),
        "globe": part("Black globe", C["globe"].shape, COL["globe"]),
        "hanger": part("Hanger tube and nuts", C["hanger"].shape, COL["hanger"]),
        "probe": part("Globe probe", C["probe"].shape, COL["probe"]),
        "anemo": part("Cup anemometer and mast bolt", S("anemometer", "mast_bolt"), COL["anemo"]),
        "lanyard": part("Retention lanyards (2)", C["lanyard"].shape, COL["lanyard"]),
        "harness": part("Sensor harness (2 leads)", C["harness"].shape, COL["harness"]),
        "vblocks": part("Adapter V-blocks (2) and screws", S("vblocks", "ascrews"), COL["vblocks"]),
        "fieldnode": part("FieldNode core (its own build plan)", C["fieldnode"].shape, COL["fieldnode"]),
        "abands": part("Adapter strap bands (2)", C["abands"].shape, COL["bands"]),
        "bands": part("Saddle strap bands (2)", C["bands"].shape, COL["bands"]),
    }


ORDER = ["saddle", "trim", "cheeks", "arm", "plates", "rods", "th", "fan", "cowl", "globe", "hanger", "probe",
         "anemo", "lanyard", "harness", "vblocks", "fieldnode", "abands", "bands"]


# ----------------------------------------------------------------- overview
def overview():
    M = made()
    off = {"saddle": (-170, 0, 0), "trim": (-330, 0, 40), "cheeks": (-50, 0, 30), "arm": (0, 0, 230),
           "plates": (0, 0, 0), "rods": (-140, 0, 0), "th": (0, 0, -190), "fan": (0, 0, 110), "cowl": (0, 0, 190),
           "globe": (0, 0, -40), "hanger": (0, 0, 90), "probe": (110, 0, 40), "anemo": (0, 0, 330),
           "lanyard": (0, 230, 70), "harness": (520, 0, -560), "vblocks": (-280, 0, -520), "fieldnode": (-90, 0, -520),
           "abands": (-450, 0, -520), "bands": (-460, 0, 0)}
    parts = []
    for k in ORDER:
        p = M[k]
        p.explode = off[k]
        parts.append(p)
    return bv.overview(parts, OUT / "overview.png", "HeatMap Node prototype: every component, pulled apart",
                       subtitle="Numbered in build order. Seen from the front left and above; the pole is not shown",
                       elev=16, azim=-62, size=(11, 8.5), dpi=150, key=True)


# ----------------------------------------------------------------- making sketches
def sheets(only=None):
    import build123d as b
    M = made()
    base = dict(project="HeatMap Node", date=DATE)
    out = []
    w = P["saddle"][0]

    def want(n):
        return only is None or str(n) in only

    if want(101):
        out.append(bv.component_sheet(
            Part("Arm saddle", C["saddle"].shape, COL["saddle"]), [M["arm"], M["cheeks"], pole(AZ - 300, AZ + 300)],
            dwg_no="HMN-DWG-101", title="HeatMap Node arm saddle: making sketch", material="Aluminium sheet 3 mm, 5052-H32",
            view_shape=b.Pos(0, 0, -AZ) * C["saddle"].shape, inset_view=(25, -130),
            notes=[f"A channel {w:.0f} wide, 180 tall and 40 deep, bent from one 3 mm sheet blank.",
                   "The web is the flat back the arm bears on; the two flanges point at the pole.",
                   "Blank about 120 x 250 mm; the bending shop sets the length for its bend",
                   "  allowance so the web is 180 outside and each flange stands 40 out.",
                   "Before bending, cut a 120 degree V in each end of the blank (the flange):",
                   "  110.9 wide at the free edge, point 32 in from the edge (8 from the web).",
                   "Web holes: four 6.6 mm, 35 each side of centre, 25 above and below the",
                   "  middle (65 and 115 up from the bottom edge).",
                   "Band slots: four 3 x 16 mm, 55 each side of centre, centred 20 from the",
                   "  top and bottom edges. Chain drill 3 mm and file square.",
                   "Bend both flanges 90 degrees the same way, inside radius about 3 mm.",
                   "Deburr; push rubber edge trim over both V edges (it takes 1.5 mm).",
                   "Check: on a 114 mm tube both V edges touch the tube through the trim."],
            **base))
    if want(102):
        ch = win(C["cheeks"].shape, 60, 130, 0, 60, AZ - 50, AZ + 50)
        out.append(bv.component_sheet(
            Part("Arm cheek", ch, COL["cheeks"]), [M["saddle"], M["arm"]],
            dwg_no="HMN-DWG-102", title="HeatMap Node arm cheek (make 2): making sketch", material="Aluminium equal angle 40 x 40 x 3 mm, 6063",
            view_shape=b.Pos(-D["web_out"], 0, -AZ) * ch, inset_view=(20, -60),
            notes=["Cut two 80 mm lengths of 40 x 40 x 3 angle; square and deburr the ends.",
                   "Flat leg (goes on the saddle web): two 6.6 mm holes, 22.5 from the",
                   "  outside corner of the angle, 15 and 65 up from the bottom end.",
                   "Upright leg (grips the arm): two 6.6 mm holes at mid-height (40 up),",
                   "  12 and 32 out from the outside face of the flat leg.",
                   "Left and right cheeks are mirror images: clamp the upright legs back",
                   "  to back and drill them together so the holes line up.",
                   "Fit: flat leg flat on the web front, the arm between the two upright",
                   "  legs. M6 button-head screws from inside the saddle hold the flat leg;",
                   "  two M6 bolts pass through both cheeks and the arm.",
                   "Check: with the arm between them both upright legs touch the arm."],
            **base))
    if want(103):
        x0 = D["arm_x0"]
        holes = [(P["cheek_bolt_x"][0], "cheek bolt"), (SX - P["rod_pcd"] / 2 - x0, "shield rod"),
                 (SX + P["rod_pcd"] / 2 - x0, "shield rod"), (GX - x0, "globe tube"), (AX - x0, "mast")]
        out.append(bv.component_sheet(
            Part("Sensor arm", S("arm", "plug"), COL["arm"]), [M["saddle"], M["cheeks"], M["plates"], M["globe"], M["anemo"]],
            dwg_no="HMN-DWG-103", title="HeatMap Node sensor arm: making sketch", material="Aluminium square tube 25 x 25 x 2 mm, 6063",
            view_shape=b.Pos(-x0, 0, -AZ) * C["arm"].shape, inset_view=(20, -60),
            notes=[f"Cut 530 mm of 25 x 25 x 2 tube; square and deburr both ends.",
                   "Measure every hole from the root end (the end that bears on the saddle).",
                   "Through both side walls, on the centre line: 6.6 mm at 12 and 32",
                   "  (cheek bolts) and 5.5 mm at 500 (anemometer mast cross bolt).",
                   "Through the top and bottom walls, on the centre line:",
                   f"  5.5 mm at {holes[1][0]:.1f} and {holes[2][0]:.1f} (shield rods),",
                   f"  10.5 mm at {holes[3][0]:.1f} (globe hanger tube),",
                   f"  16.5 mm at {holes[4][0]:.1f} (anemometer mast; step drill).",
                   "Drill each top and bottom pair in one pass on a drill press so they",
                   "  line up; the arm-holes picture in the plan repeats these figures.",
                   "Push the end plug into the tip and slide the two crush sleeves in",
                   "  from the root end to line up with the cheek bolt holes.",
                   "Check: a drill of each hole size passes straight through each pair."],
            **base))
    if want(104):
        tp = one_plate(0)
        out.append(bv.component_sheet(
            Part("Top shield plate", tp, COL["plates"]), [M["fan"], M["cowl"], M["rods"], M["arm"]],
            dwg_no="HMN-DWG-104", title="HeatMap Node top shield plate: making sketch", material="UV-stable white ASA, 3D printed",
            view_shape=b.Pos(-SX, 0, -ST) * tp, inset_view=(30, -60),
            notes=["Print one, flat, 110 mm across and 3 mm thick, in white ASA, 4 walls,",
                   "  40 % infill or more, in an enclosed printer.",
                   "Centre hole 56 mm: the fan draws air up through it.",
                   "Four 5.5 mm rod holes on a 92 mm circle, 90 degrees apart",
                   "  (46 from the centre); two of them line up with the arm.",
                   "Four 4.4 mm fan screw holes on a 50 mm square, centred.",
                   "  The rod holes sit on the square's centre lines, the fan holes",
                   "  on its diagonals.",
                   "Fit: the fan sits flat on top over the centre hole; the cowl stands on",
                   "  the fan; four M4 x 40 screws go through cowl, fan and plate, nuts below.",
                   "Nuts on the four rods clamp this plate down onto the stack.",
                   "Check: the fan's corner holes line up with the four 4.4 mm holes."],
            **base))
    if want(105):
        hp = one_plate(P["hub_plate"])
        out.append(bv.component_sheet(
            Part("Ring plate with sensor hub", hp, COL["plates"]), [M["th"], M["rods"]],
            dwg_no="HMN-DWG-105", title="HeatMap Node ring plates (make 7; one with the sensor hub): making sketch",
            material="UV-stable white ASA, 3D printed", view_shape=b.Pos(-SX, 0, -(ST - P["hub_plate"] * P["plate_pitch"])) * hp,
            inset_view=(30, -60),
            notes=["Print seven ring plates flat, bosses up: 110 mm across, 3 mm thick,",
                   "  with a 56 mm centre hole. Print six without the hub.",
                   "Four bosses 10 mm across and 12 mm tall stand on each ring around",
                   "  5.5 mm rod holes on a 92 mm circle. Each boss carries the plate above,",
                   "  so the plates sit 15 mm apart with 12 mm air gaps.",
                   "The seventh ring (the third plate from the top) also has a hub 22 mm",
                   "  across and 8 mm tall on three 4 mm spokes; its 18.5 mm bore holds",
                   "  the sensor capsule. Add a 2.5 mm side hole in the hub and tap or",
                   "  thread-form it M3 for a nylon set screw.",
                   "Fit: the rods pass through the bosses; nothing is glued.",
                   "Check: eight plates stack 108 mm tall on the rods, gaps even."],
            **base))
    if want(106):
        out.append(bv.component_sheet(
            Part("Fan cowl", C["cowl"].shape, COL["cowl"]), [M["plates"], M["fan"], M["rods"]],
            dwg_no="HMN-DWG-106", title="HeatMap Node fan cowl: making sketch", material="UV-stable white ASA, 3D printed",
            view_shape=b.Pos(-SX, 0, -ST) * C["cowl"].shape, inset_view=(30, -60),
            notes=["Print one, lid down: a lid 76 x 76 x 3 mm on four legs 8 x 8 mm.",
                   "The legs stand on the fan's four corners, on a 50 mm square, and",
                   "  lift the lid 12 mm above the fan so the air leaves sideways.",
                   "Overall height from the top plate is 30 mm (fan 15, legs 12, lid 3).",
                   "A 4.4 mm hole runs down through each leg and the lid.",
                   "Fit: four M4 x 40 pan-head screws from the top of the lid, through",
                   "  the legs, the fan's corner holes and the top plate, with nuts under",
                   "  the plate. Tighten lightly: the fan frame is plastic.",
                   "The lid edge stays 4 mm or more clear of the rods and spacers.",
                   "Check: the lid sits level and the fan spins freely by hand."],
            **base))
    if want(107):
        import build123d as bb
        blk = win(C["vblocks"].shape, -100, 100, -100, 100, Z0 + P["adapter_dz"][0] - 20, Z0 + P["adapter_dz"][0] + 20)
        loc = bb.Pos(0, 0, -(Z0 + P["adapter_dz"][0])) * bb.Rot(0, 0, -P["fn_azimuth"]) * blk
        out.append(bv.component_sheet(
            Part("Adapter V-block", blk, COL["vblocks"]), [M["fieldnode"], M["abands"], pole(Z0 - 150, Z0 + 350)],
            dwg_no="HMN-DWG-107", title="HeatMap Node pole adapter V-block (make 2): making sketch",
            material="ASA, 3D printed at 100 % infill", view_shape=loc, inset_view=(20, -140),
            notes=["Print two, standing on the 110 x 38 mm face, 100 % infill, 5 walls.",
                   "Block 110 wide, 30 tall and 38 deep with a 120 degree V across its",
                   "  whole width: point 31.8 in from the pole face, 6.2 from the back.",
                   "Two band slots 3.5 x 16 mm right through, front to back, 51 each side",
                   "  of centre, centred on the height; they line up with the slots in",
                   "  the FieldNode back plate.",
                   "Two holes for M4 brass heat-set inserts in the flat back face, 18 each",
                   "  side of centre, centred on the height, 8 deep; press the inserts in",
                   "  with a soldering iron, flush.",
                   "Fit: the flat back sits on the back of the FieldNode back plate in place",
                   "  of FieldNode's own V-blocks, held by its M4 countersunk screws.",
                   "Check: poles of 60, 114 and 200 mm each touch both V faces."],
            **base))
    return out


# ----------------------------------------------------------------- joints
def joints(only=None):
    out = []

    def want(n):
        return only is None or str(n) in only
    if want(1):
        box_ = (-75, 95, -80, 80, AZ + 84, AZ + 92)
        bandbox = (-75, 95, -80, 80, AZ + 64, AZ + 76)
        out.append(bv.joint([
            part("Pole (site supplied)", win(pole_context(P), *box_), "#D1D5DB"),
            part("Saddle flange with its V notch", win(C["saddle"].shape, *box_), COL["saddle"]),
            part("Rubber edge trim: the pole bears here", win(C["trim"].shape, *box_), "#111827"),
            part("Strap band (below the flange)", win(C["bands"].shape, *bandbox), "#2563EB")],
            OUT / "joint-01.png", "Joint 1: arm saddle on the pole, seen from above",
            subtitle="The pole sits in the V and bears on the trim on both edges; the band runs round the pole, through the web and across its front",
            elev=82, azim=-90, size=(8, 6)))
    if want(2):
        x0 = D["arm_x0"]
        box_ = (40, 135, -62, 62, AZ - 48, AZ + 48)
        out.append(bv.joint([
            part("Saddle web", win(C["saddle"].shape, *box_), COL["saddle"]),
            part("Arm cheek", win(C["cheeks"].shape, *box_), COL["cheeks"]),
            part("Sensor arm (cut open)", win(C["arm"].shape, *box_), COL["arm"]),
            part("Crush sleeve inside the arm", win(C["sleeves"].shape, *box_), "#C2410C"),
            part("M6 bolts and nuts", win(C["clamp_bolts"].shape, *box_), COL["bolt"])],
            OUT / "joint-02.png", "Joint 2: arm root between the cheeks (cut open along the arm)",
            subtitle="The arm bears on the web; two M6 bolts pass through both cheeks, the arm and a crush sleeve",
            cut="-Y", elev=22, azim=55, size=(8, 6)))
    if want(3):
        rx = SX + P["rod_pcd"] / 2
        box_ = (rx - 30, rx + 22, -22, 22, D["shield_bot"] - 12, D["arm_top"] + 14)
        out.append(bv.joint([
            part("Shield plates and bosses", win(C["plates"].shape, *box_), "#D6D3D1"),
            part("M5 rod, nuts, acorn nut", win(C["rods"].shape, *box_), COL["rods"]),
            part("Spacer between top plate and arm", win(C["spacers"].shape, *box_), COL["spacers"]),
            part("Sensor arm", win(C["arm"].shape, *box_), COL["arm"])],
            OUT / "joint-03.png", "Joint 3: a long shield rod through the stack and the arm (cut open)",
            subtitle="Bosses carry each plate; the rod clamps the stack; the spacer and the nut on the arm hold it to the arm",
            cut="+Y", elev=8, azim=-90, size=(8, 6.5)))
    if want(4):
        box_ = (SX - 58, SX + 58, -58, 58, ST - 8, ST + 32)
        out.append(bv.joint([
            part("Top shield plate", win(C["plates"].shape, *box_), "#D6D3D1"),
            part("Fan", win(C["fan"].shape, *box_), COL["fan"]),
            part("Cowl on four legs", win(C["cowl"].shape, *box_), COL["cowl"]),
            part("M4 screws and nuts", win(C["fan_screws"].shape, *box_), COL["bolt"]),
            part("Rod nuts and spacers", win(S("rods", "spacers"), *box_), COL["rods"])],
            OUT / "joint-04.png", "Joint 4: fan and cowl on the top plate",
            subtitle="Air is drawn up the stack, through the fan and out sideways under the lid", elev=25, azim=-55, size=(8, 6)))
    if want(5):
        box_ = (SX - 70, SX + 70, -70, 70, ST - 64, ST - 19)
        out.append(bv.joint([
            part("Third plate with the hub, and the plates below", win(C["plates"].shape, *box_), "#D6D3D1"),
            part("Sensor capsule in the hub", win(C["th_sensor"].shape, *box_), COL["th"]),
            part("Sensor lead, out between the second and third plates", win(C["harness"].shape, *box_), COL["harness"])],
            OUT / "joint-05.png", "Joint 5: temperature and humidity sensor in its hub",
            subtitle="The second plate and the top plate are left off. The capsule sits in the hub; its lead runs out over the third plate",
            elev=45, azim=-45, size=(8, 6)))
    if want(6):
        box_ = (GX - 26, GX + 26, -26, 26, D["globe_top"] - 18, D["arm_top"] + 26)
        out.append(bv.joint([
            part("Globe top and its boss", win(C["globe"].shape, *box_), COL["globe"]),
            part("Hanger tube and three M10 nuts", win(C["hanger"].shape, *box_), COL["hanger"]),
            part("Probe stem inside the tube", win(C["probe"].shape, *box_), COL["probe"]),
            part("Sensor arm", win(C["arm"].shape, *box_), COL["arm"])],
            OUT / "joint-06.png", "Joint 6: globe hanger tube through the arm (cut open)",
            subtitle="The hollow tube screws into the globe's boss and is nutted above and below the arm; the probe runs down inside it",
            cut="+Y", elev=8, azim=-90, size=(8, 6.5)))
    if want(7):
        box_ = (AX - 32, AX + 34, -34, 34, D["arm_bot"] - 24, D["arm_top"] + 28)
        out.append(bv.joint([
            part("Sensor arm and end plug", win(S("arm", "plug"), *box_), COL["arm"]),
            part("Anemometer mast", win(C["anemometer"].shape, *box_), COL["anemo"]),
            part("M5 cross bolt (nut side)", win(C["mast_bolt"].shape, AX - 32, AX + 34, -34, -12.5, D["arm_bot"] - 24, D["arm_top"] + 28), COL["bolt"])],
            OUT / "joint-07.png", "Joint 7: anemometer mast through the arm tip",
            subtitle="The mast passes through the arm and is pinned by one M5 bolt through arm and mast", elev=22, azim=-50, size=(8, 6)))
    if want(8):
        zc = Z0 + P["adapter_dz"][0]
        box_ = (-70, 95, -85, 85, zc + 8, zc + 15)
        bandbox = (-70, 95, -95, 95, zc - 7, zc + 7)
        out.append(bv.joint([
            part("Pole (site supplied)", win(pole_context(P), *box_), "#D1D5DB"),
            part("Adapter V-block", win(C["vblocks"].shape, *box_), COL["vblocks"]),
            part("FieldNode back plate", win(C["fieldnode"].shape, -1, 95, -95, 95, zc + 8, zc + 15), "#6B7280"),
            part("Strap band (below), through block and plate", win(C["abands"].shape, *bandbox), "#2563EB")],
            OUT / "joint-08.png", "Joint 8: adapter V-block between the pole and the FieldNode back plate",
            subtitle="Seen from above at the lower block. The band runs round the pole, through the block and the plate and across the plate front",
            elev=82, azim=-90, size=(8, 6)))
    return out


# ----------------------------------------------------------------- assembly steps
def steps(only=None):
    M = made()
    out = []

    def want(n):
        return only is None or str(n) in only

    def st(n, done, new, title, sub, **kw):
        if want(n):
            out.append(bv.step(done, new, OUT / f"step-{n:02d}.png", f"Step {n}: {title}", subtitle=sub, **kw))

    def mv(p, e):
        return Part(p.name, p.shape, p.color, None, tuple(e), p.alpha)
    sad = M["saddle"]
    st(1, [sad], [mv(M["trim"], (-90, 0, 0))], "rubber trim onto the saddle's V edges",
       "Push the trim over both notched flange edges, starting at the point of each V", elev=30, azim=-140)
    st(2, [sad, M["trim"]], [mv(M["cheeks"], (90, 0, 0))], "cheeks onto the saddle",
       "Four M6 button-head screws from inside the saddle, nyloc nuts on the cheeks; snug for now",
       elev=22, azim=-50, label_done=False)
    clamp = [sad, M["trim"], M["cheeks"]]
    st(3, clamp, [mv(M["arm"], (220, 0, 0))], "arm between the cheeks",
       "Arm end on the web; two M6 x 40 bolts through cheeks, arm and sleeves; then tighten all six",
       elev=22, azim=-50, label_done=False)
    # the shield is built on the bench, upside up
    plates = M["plates"]
    lower = part("Ring plates 3 to 8, bottom first", win(C["plates"].shape, SX - 60, SX + 60, -60, 60, D["shield_bot"] - 1, ST - 18),
                 "#14B8A6")
    rr_ = C["rods"].shape
    rods_ = part("Four rods with acorn nuts", win(rr_, SX - 60, SX + 60, -60, 60, D["shield_bot"] - 20, ST - 0.01)
                 + win(rr_, SX - 60, SX + 60, -60, 60, ST + 4.01, D["arm_top"] - 0.01), COL["rods"])
    st(4, [rods_], [mv(lower, (0, 0, 140))], "start the shield stack on its rods",
       "Rods upright with acorn nuts below; slide on the bottom plate, then each ring, bosses up; hub plate last",
       elev=20, azim=-60)
    st(5, [rods_, lower], [mv(M["th"], (0, 0, -150))], "sensor into the hub",
       "Push the capsule up through the rings into the hub; nylon set screw; lay its lead out over the hub",
       elev=15, azim=-60, label_done=False)
    upper = part("Second plate and top plate", win(C["plates"].shape, SX - 60, SX + 60, -60, 60, ST - 18, ST + 1), "#14B8A6")
    st(6, [rods_, lower, M["th"]], [mv(upper, (0, 0, 120))], "close the stack",
       "Second plate, then the top plate; a nut on each rod on the top plate, finger tight plus a quarter turn",
       elev=20, azim=-60, label_done=False)
    stack = [part("Shield stack", S("plates", "th_sensor"), COL["plates"]), rods_]
    st(7, stack, [mv(M["fan"], (0, 0, 90)), mv(part("Cowl and screws", S("cowl", "fan_screws"), COL["cowl"]), (0, 0, 170))],
       "fan and cowl onto the top plate", "Fan flat over the centre hole, label up; cowl on the fan; four M4 screws, nuts under the plate",
       elev=25, azim=-60)
    head0 = clamp + [M["arm"]]
    shield_all = part("Shield with fan and cowl", S("plates", "th_sensor", "fan", "cowl", "fan_screws", "rods"), "#14B8A6")
    st(8, head0, [mv(shield_all, (0, 0, -160)), mv(part("Spacers (2)", C["spacers"].shape, COL["spacers"]), (0, 0, -80))],
       "hang the shield on the arm", "Spacers on the two long rods, rods up through the arm, a nut on each on top of the arm",
       elev=15, azim=-55, label_done=False)
    head1 = head0 + [part("Shield", S("plates", "th_sensor", "fan", "cowl", "fan_screws", "rods", "spacers"), COL["plates"])]
    st(9, head1, [mv(part("Globe with hanger tube and probe", S("globe", "hanger", "probe"), COL["globe"]), (0, 0, -200))],
       "hang the globe", "Tube into the boss with a lock nut, probe down the tube; lower nut on, tube up through the arm, top nut on",
       elev=15, azim=-55, label_done=False)
    head2 = head1 + [part("Globe", S("globe", "hanger", "probe"), COL["globe"])]
    st(10, head2, [mv(M["anemo"], (0, 0, 220))], "anemometer onto the arm tip",
       "Mast down through the arm until its pin holes line up; one M5 bolt through arm and mast, nyloc nut",
       elev=15, azim=-55, label_done=False)
    head3 = head2 + [M["anemo"]]
    st(11, head3, [mv(M["lanyard"], (0, 110, 60))], "retention lanyards",
       "Seen from the right. One from the top plate and one from the globe boss, each looped round the arm and closed",
       elev=22, azim=50, label_done=False)
    leads_head = part("Sensor leads along the arm", win(C["harness"].shape, 70, 700, -80, 80, AZ - 150, AZ + 100), COL["harness"])
    st(12, head3 + [M["lanyard"]], [mv(leads_head, (0, -120, 0))], "sensor leads along the arm",
       "Plug each sensor tail into its lead; run both leads along the arm's side; a cable tie every 80 mm",
       elev=25, azim=-60, label_done=False)
    fn = M["fieldnode"]
    st(13, [fn], [mv(M["vblocks"], (-150, 0, 0))], "adapter V-blocks onto the FieldNode core",
       "In place of FieldNode's own V-blocks: two M4 countersunk screws each from the front of its back plate",
       elev=18, azim=-140)
    core = [fn, M["vblocks"]]
    st(14, core, [mv(M["abands"], (-160, 0, 0))], "FieldNode core onto the pole",
       "At height. Each band round the pole, through its block and plate slots, across the plate front; tension and lock",
       context=[pole(Z0 - 250, Z0 + 650)], elev=15, azim=-105)
    head_all = part("Sensor head, assembled on the ground", S("saddle", "trim", "cheeks", "clamp_bolts", "arm", "plug", "plates", "th_sensor",
                                                             "rods", "spacers", "fan", "cowl", "fan_screws", "globe", "hanger",
                                                             "probe", "anemometer", "mast_bolt", "lanyard"), "#14B8A6")
    st(15, core + [M["abands"]], [mv(head_all, (250, 0, 0)), mv(M["bands"], (-200, 0, 0))], "sensor head onto the pole",
       "At height, 650 mm above the core. Saddle on the pole, arm toward the equator; bands through the web slots",
       context=[pole(Z0 - 250, AZ + 300)], elev=15, azim=-105, size=(8, 7))
    st(16, core + [M["abands"], head_all, M["bands"]], [mv(part("Sensor harness", C["harness"].shape, COL["harness"]), (0, -150, 0))],
       "sensor leads down the pole to the FieldNode ports",
       "Leads round the side of the saddle and down the pole, a tie every 300 mm; plugs into ports A and B",
       context=[pole(Z0 - 250, AZ + 300)], elev=15, azim=-105, size=(8, 7), label_done=False)
    return out


# ----------------------------------------------------------------- arm hole layout
def layouts():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    INK, MUT, AC = "#111827", "#4B5563", "#0F766E"
    x0 = D["arm_x0"]
    L = P["arm_len"]
    fig = plt.figure(figsize=(12, 5.2), dpi=150)
    ax = fig.add_axes([0.04, 0.12, 0.92, 0.7]); ax.set_aspect("equal"); ax.set_axis_off()
    # top view (top wall) above, side view below
    for y0, lab in ((40, "Top wall (seen from above): vertical holes go through top and bottom walls"),
                    (-15, "Side wall (seen from the front): horizontal holes go through both side walls")):
        ax.add_patch(Rectangle((0, y0), L, 25, fc="#F3F4F6", ec=INK, lw=1.1))
        ax.text(0, y0 + 29, lab, fontsize=8, color=MUT, ha="left")
    vert = [(SX - P["rod_pcd"] / 2 - x0, 5.5, "shield rod"), (SX + P["rod_pcd"] / 2 - x0, 5.5, "shield rod"),
            (GX - x0, 10.5, "globe tube"), (AX - x0, 16.5, "mast")]
    hor = [(P["cheek_bolt_x"][0], 6.6, "cheek bolt"), (P["cheek_bolt_x"][1], 6.6, "cheek bolt"), (AX - x0, 5.5, "mast bolt")]
    for x, d, n in vert:
        ax.add_patch(plt.Circle((x, 52.5), d / 2, fc="white", ec=INK, lw=1))
        ax.text(x, 82, f"{x:.1f}\n{d:g} {n}", ha="center", va="bottom", fontsize=7.5, color=AC, linespacing=1.15)
        ax.plot([x, x], [52.5 + d / 2 + 1, 66], color=AC, lw=0.4, ls=":"); ax.plot([x, x], [77, 81], color=AC, lw=0.4, ls=":")
    for i, (x, d, n) in enumerate(hor):
        ax.add_patch(plt.Circle((x, -2.5), d / 2, fc="white", ec=INK, lw=1))
        yy = -26 - 13 * (i % 2)
        ax.text(x + (14 if i == 1 else 0), yy, f"{x:.1f}  {d:g} {n}", ha="center", va="top", fontsize=7.5, color=AC)
        ax.plot([x, x], [-2.5 - d / 2 - 1, yy + 1], color=AC, lw=0.4, ls=":")
    ax.text(-4, 52.5, "root\nend", ha="right", va="center", fontsize=7.5, color=MUT)
    ax.text(L + 4, 52.5, "tip", ha="left", va="center", fontsize=7.5, color=MUT)
    ax.set_xlim(-30, L + 30); ax.set_ylim(-48, 106)
    fig.text(0.03, 0.95, "Sensor arm: hole positions", fontsize=13, fontweight="bold", color=INK, va="top")
    fig.text(0.03, 0.89, "25 x 25 x 2 mm tube, 530 mm long. Hole centres in mm from the root end (the end that bears on the saddle), "
             "all on the centre line of the face. Hole sizes in mm. From the model.", fontsize=8.5, color=MUT, va="top")
    fig.text(0.03, 0.02, "BUILD PLAN ILLUSTRATION, PLAN NOT YET BUILT", fontsize=7, color="#B45309")
    fig.text(0.97, 0.02, "github.com/BoujeeEnjinia1701/heatmap-node", fontsize=7, color=AC, ha="right", family="monospace")
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "arm-holes.png", facecolor="white"); plt.close(fig)
    return OUT / "arm-holes.png"


if __name__ == "__main__":
    args = sys.argv[1:] or ["overview", "sheets", "layouts", "joints", "steps"]
    fns = {"overview": overview, "sheets": sheets, "layouts": layouts, "joints": joints, "steps": steps}
    i = 0
    while i < len(args):
        w = args[i]
        only = None
        while i + 1 < len(args) and args[i + 1] not in fns:
            only = (only or []) + [args[i + 1]]; i += 1
        r = fns[w](only) if w in ("sheets", "joints", "steps") else fns[w]()
        print(w, only or "", "->", r)
        i += 1
