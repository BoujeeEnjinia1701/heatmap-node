"""HeatMap Node product appearance model for photoreal renders (STANDARDS sections 12 and 24), TRL 3.

Every product part is components(CHOSEN) from cad/src/model.py exactly as modelled (option A): the formed
saddle with its EPDM trim, cheeks, strap bands and buckles, every cheek bolt, button screw, nut and washer;
the drilled arm and its end plug; the eight white shield plates on four M5 rods with acorn nuts and spacers;
the fan, cowl and screws; the sensor capsule with its PTFE membrane cap; the black globe on its hanger
tube and nuts, probe and bead; the cup anemometer (mast, hub, arms, cups) and its cross bolt; the
lanyards; the M12 leads and plugs; and the FieldNode core (back plate, enclosure and lid, board, cell,
sockets, antenna, solar panel and bracket, sun shield) on the printed pole adapter with its bands. Only the
site is added, as context parts: a street pole set in a concrete plinth with a luminaire arm, a kerb, and a
1.75 m person standing on the pavement for scale. The hero is rendered by .kit/photoreal.py as an outdoor
scene on concrete (ground level at model z = 0, sun high in the south-west of the picture).
APPEARANCE MODEL ONLY. CONCEPT, NOT FOR FABRICATION.

Groups: "head" (sensor head parts), "core" (FieldNode core and the pole adapter), "stub" (a short pole
section for studio views), "context" (the site and the person).

    from product_model import product_parts
    for p in product_parts(): print(p["name"], p["group"], p["material"])
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / ".kit")]

from build123d import Box, Cylinder, Pos, Rot  # noqa: E402
import model as M  # noqa: E402
from cad_parts import part, break_edges, round_tube  # noqa: E402

TITLE = "HeatMap Node: street-pole heat stress sensor with a black globe thermometer"

_SITE = ["--scene=outdoor", "--ground=concrete", "--ground-z=0", "--sun=52,-62", "--lens=40"]
RENDER_VIEWS = [
    {"name": "hero", "groups": ["head", "core", "context"], "explode": False, "el": 14, "az": -40, "args": _SITE,
     "note": "Site render in full sun from the front right, a little above the pavement (about 14 deg elevation): a "
             "street pole on a concrete plinth beside a kerb carries the sensor arm at 2.8 m, pointing toward the equator, "
             "with the shield, the black globe and the anemometer, and the FieldNode solar core above it; "
             "1.75 m person on the pavement for scale"},
    {"name": "studio", "groups": ["head", "core", "stub"], "explode": False, "el": 24, "az": -38,
     "note": "Studio render from the front right and above (about 24 deg elevation) on a short section of pole: "
             "formed saddle and strap bands, arm, radiation shield with fan cowl, globe, anemometer and the "
             "FieldNode core with its sun shield and solar panel"},
    {"name": "exploded", "groups": ["head", "core", "stub"], "explode": True, "el": 26, "az": -52,
     "note": "Exploded view from the front right and above (about 26 deg elevation): clamp, arm, shield stack with "
             "fan and cowl, sensor, globe with probe, anemometer, harness and lanyards pulled apart; FieldNode core "
             "and pole adapter lifted clear"},
    {"name": "detail", "groups": ["head", "stub"], "explode": False, "el": 16, "az": -35,
     "note": "Detail from the front right, slightly above (about 16 deg elevation), without the FieldNode core: "
             "radiation shield and fan cowl, black globe, anemometer and the formed saddle on the pole section"},
]

# explode offsets (mm) by the BOM key of the part's group in model.py
_EXPLODE = {
    "fieldnode": (150, -200, 560), "adapter": (-200, -320, 360), "shield": (0, -320, -300), "fan": (0, -320, 80),
    "th_sensor": (0, -320, -480), "globe": (160, 0, -420), "probe": (160, -320, -150), "anemometer": (200, 0, 260),
    "arm": (0, 0, 120), "clamp": (0, 0, 0), "harness": (-60, -320, -80), "lanyard": (160, 0, -760),
}
_KEY = {g: k for k, v in M.BOM_GROUPS.items() for g in v[2]}


def _tube(od, wall, z0, z1, x=0.0, y=0.0):
    return Pos(x, y, z0) * round_tube(od, wall, z1 - z0)


def site():
    """Street pole in a concrete plinth with a luminaire arm, a kerb and a 1.75 m person. Ground level is model z = 0
    (photoreal --ground-z=0); every site part reaches below it."""
    P = M.PARAMS
    out = []
    ctx = lambda n, sh, mat, tag="(site)": out.append(part(f"{n} {tag}", sh, mat, kind="context", group="context"))
    od = P["pole_od"]
    ctx("Street pole", _tube(od, 4.5, -400.0, 4700.0), "galvanised")
    ctx("Pole cap", Pos(0, 0, 4710) * Cylinder(od / 2 + 3, 20), "galvanised")
    ctx("Concrete plinth", break_edges(Pos(0, 0, -300) * Cylinder(190, 600), 15), "concrete")
    ctx("Pole base collar", Pos(0, 0, 160) * Cylinder(od / 2 + 22, 120), "galvanised")
    # luminaire arm toward the road side behind the pole (-X), head at its end
    ctx("Luminaire arm", Pos(-900, 0, 4500) * Rot(0, 90, 0) * round_tube(60, 4, 1800), "galvanised")
    ctx("Luminaire head", break_edges(Pos(-1750, 0, 4440) * Box(700, 300, 90), 25), "galvanised")
    ctx("Kerb", break_edges(Pos(0, -2300, -150) * Box(9000, 160, 600), 12), "concrete")
    try:
        import context_parts
        man = Pos(-950, -750, 0) * Rot(0, 0, 25) * context_parts.mannequin(1750.0, "stand")
        out.append(part("Person 1.75 m (scale)", man, "skin", kind="context", group="context"))
    except Exception as e:   # the mannequin is for scale only; never block the product parts
        print("mannequin not added:", e)
    return out


def product_parts():
    out = []
    for p in M.components(M.CHOSEN):
        if p["kind"] == "context":
            continue
        q = dict(p)
        q["group"] = "core" if p["group"] in ("fieldnode", "vblocks", "ascrews", "abands") else "head"
        q["explode"] = _EXPLODE.get(_KEY.get(p["group"], ""), (0, 0, 0))
        out.append(q)
    out.append(part("Street pole section (not supplied)", _tube(M.PARAMS["pole_od"], 4.5, 2300.0, 3950.0), "galvanised",
                    kind="context", group="stub"))
    return out + site()


if __name__ == "__main__":
    ps = product_parts()
    print(len(ps), "parts;", sum(p["group"] in ("head", "core") for p in ps), "product,", sum(p["group"] == "context" for p in ps), "context")
