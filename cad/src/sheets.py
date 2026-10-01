"""HeatMap Node general arrangement sheet HMN-DWG-001, Rev P2 (TRL 3, HMN-DDR-002 applied).

Run from the repo root:  python cad/src/sheets.py
Writes cad/drawings/HMN-DWG-001.svg, .pdf and .png from the parametric model in
cad/src/model.py with .kit/drawing.py. Dimensions come from PARAMS and derived(), so they
follow any parameter change. The concept blueprint in media/ is HMN-DWG-010.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / ".kit"), str(ROOT / "cad" / "src")]
from drawing import Sheet, _viewbox, _t, M, TB_Y, INK, MUTED  # noqa: E402
from model import PARAMS as P, build_parts, derived, zcyl  # noqa: E402

DATE = "2026-09-25"
POLE_BOT, POLE_TOP = 1960.0, 3080.0     # pole stub shown on the sheet


def safe_project_views(part, workdir, line_weight=0.35):
    """As drawing.project_views, but edge by edge, so a degenerate edge is skipped."""
    from build123d import ExportSVG, LineType, Unit
    workdir = Path(workdir); workdir.mkdir(parents=True, exist_ok=True)
    bb = part.bounding_box()
    c = bb.center(); d = max(bb.size.X, bb.size.Y, bb.size.Z) * 10
    setups = {"front": ((c.X, c.Y - d, c.Z), (0, 0, 1)), "top": ((c.X, c.Y, c.Z + d), (0, 1, 0)),
              "right": ((c.X + d, c.Y, c.Z), (0, 0, 1)), "iso": ((c.X + d, c.Y - d, c.Z + d * 0.8), (0, 0, 1))}
    out, skipped = {}, 0
    for name, (origin, up) in setups.items():
        visible, hidden = part.project_to_viewport(origin, up, (c.X, c.Y, c.Z))
        ex = ExportSVG(unit=Unit.MM, line_weight=line_weight)
        ex.add_layer("Visible", line_color=0x111827)
        ex.add_layer("Hidden", line_color=0x6B7280, line_type=LineType.ISO_DASH, line_weight=line_weight / 2)
        for layer, edges in (("Visible", visible), ("Hidden", [] if name in ("iso", "front", "right") else hidden)):
            for e in edges:
                try:
                    ex.add_shape(e, layer=layer)
                except (AssertionError, ValueError, ZeroDivisionError):
                    skipped += 1
        p = workdir / f"{name}.svg"
        ex.write(str(p))
        out[name] = p
    print(f"projected views; skipped {skipped} degenerate edges")
    return out


def ortho_cells(sheet, views, names=("front", "top", "right")):
    """Repeat Sheet.add_ortho's layout arithmetic to find where each view lands (x, y, w, h)."""
    ax, ay, aw, ah = M + 10, M + 16, 245, TB_Y - M - 20
    gap, lab = 14, 12
    dims = {n: _viewbox(Path(views[n]).read_text())[2:] for n in names}
    fw, fh = dims["front"]; tw, th = dims["top"]; rw, rh = dims["right"]
    k = sheet.scale
    ax += (aw - (k * (max(fw, tw) + rw) + gap)) / 2
    ay += (ah - (k * (th + max(fh, rh)) + gap + 2 * lab)) / 2
    colw = k * max(fw, tw)
    front_y = ay + k * th + lab + gap
    row_h = k * max(fh, rh)
    return {"top": (ax, ay, colw, k * th), "front": (ax, front_y, colw, row_h),
            "right": (ax + colw + gap, front_y, k * rw, row_h)}


def dim_h(x1, x2, y, text):
    a = 1.4
    return [f'<line x1="{x1:.2f}" y1="{y:.2f}" x2="{x2:.2f}" y2="{y:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x1:.2f} {y:.2f} l{a} -0.5 l0 1 Z" fill="{INK}"/>',
            f'<path d="M{x2:.2f} {y:.2f} l{-a} -0.5 l0 1 Z" fill="{INK}"/>',
            _t((x1 + x2) / 2, y - 1.0, text, 2.3, 400, INK, "middle", mono=True)]


def dim_v(x, y1, y2, text, side=-1):
    a = 1.4
    cx, cy = x + side * 1.0, (y1 + y2) / 2
    return [f'<line x1="{x:.2f}" y1="{y1:.2f}" x2="{x:.2f}" y2="{y2:.2f}" stroke="{INK}" stroke-width="0.18"/>',
            f'<path d="M{x:.2f} {y1:.2f} l-0.5 {a} l1 0 Z" fill="{INK}"/>',
            f'<path d="M{x:.2f} {y2:.2f} l-0.5 {-a} l1 0 Z" fill="{INK}"/>',
            f'<g transform="rotate(-90 {cx:.2f} {cy:.2f})">{_t(cx, cy, text, 2.3, 400, INK, "middle", mono=True)}</g>']


def ext(x1, y1, x2, y2):
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.13"/>'


def leader(x1, y1, x2, y2, text, anchor="start"):
    return [f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{MUTED}" stroke-width="0.15"/>',
            f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="0.5" fill="{INK}"/>',
            _t(x2 + (1 if anchor == "start" else -1), y2 + 0.8, text, 2.1, 400, INK, anchor)]


def main():
    from build123d import Compound
    D = derived(P)
    parts = build_parts(P)
    pole = zcyl(0, 0, (POLE_BOT + POLE_TOP) / 2, P["pole_od"] / 2, POLE_TOP - POLE_BOT)
    asm = Compound(children=list(parts.values()) + [pole])
    work = ROOT / "cad" / "drawings" / "_views"
    views = safe_project_views(asm, work)
    bb = asm.bounding_box()
    s = Sheet(project="HeatMap Node", title="General arrangement", dwg_no="HMN-DWG-001", rev="P3",
              author="Amish Chadha", date=DATE, scale=0.1, theme="technical",
              material="Al arm and formed sheet saddle; ASA shield and cowl; copper globe; bought-in parts per bom/bom.csv. "
                       "PRELIMINARY, NOT FOR FABRICATION",
              revisions=[("P1", "Preliminary GA for TRL 3 (from cad/src/model.py)", DATE, "AC"),
                         ("P2", "HMN-DDR-002: fan, formed saddle, arm to equator, FieldNode shield", DATE, "AC"),
                         ("P3", "Layout and labels tidied", DATE, "AC")])
    s.add_ortho(views)
    k = s.scale
    c = ortho_cells(s, views)
    L = []
    az = P["arm_z"]

    # front view (from -Y): X to the right, Z up
    x, y, w, h = c["front"]
    X = lambda mx: x + (mx - bb.min.X) * k
    Z = lambda mz: y + h - (mz - bb.min.Z) * k
    top_dim = D["overall_top"] + 60
    # horizontal positions from the pole axis, stacked above the model
    for i, (xx, lab) in enumerate(((P["shield_x"], f"{P['shield_x']:.0f} shield"), (P["globe_x"], f"{P['globe_x']:.0f} globe"),
                                   (D["anemo_x"], f"{D['anemo_x']:.0f} anemometer"))):
        yd = Z(top_dim) + 8 - 4 * i
        L += [ext(X(0), Z(POLE_TOP) - 1, X(0), yd - 1), ext(X(xx), Z(az) - 1, X(xx), yd - 1)]
        L += dim_h(X(0), X(xx), yd, lab)
    # elevations to the left of the model
    xl = X(bb.min.X) - 4
    for zz, lab in ((D["globe_zc"], f"{D['globe_zc']:.0f} globe center"),
                    (D["shield_zc"], f"{D['shield_zc']:.0f} T and RH sensor"),
                    (az, f"{az:.0f} arm axis"),
                    (D["cup_z"], f"{D['cup_z']:.0f} cup center"),
                    (P["fn_z0"], f"{P['fn_z0']:.0f} FieldNode underside")):
        x_from = X(D["anemo_x"]) if zz == D["cup_z"] else (X(P["globe_x"]) if zz == D["globe_zc"] else
                  (X(P["shield_x"]) if zz == D["shield_zc"] else (X(0) if zz == az else X(-D["enc_yc"] + P["fn_enc"][1] / 2))))
        L.append(ext(x_from, Z(zz), xl + 1, Z(zz)))
        dy = 1.0 if zz == D["globe_zc"] else (-1.0 if zz == D["shield_zc"] else 0)
        L.append(_t(xl, Z(zz) + 0.8 + dy, f"EL {lab.upper()}", 2.1, 400, INK, "end"))
    L += dim_h(X(P["globe_x"] - P["globe_d"] / 2), X(P["globe_x"] + P["globe_d"] / 2), Z(D["globe_bot"]) + 5, f"D{P['globe_d']:.0f}")
    L.append(_t(xl, Z(D["overall_top"]) - 12, "ELEVATIONS ABOVE PAVEMENT", 2.0, 600, MUTED, "end"))
    L += leader(X(0), Z(POLE_BOT + 150), X(0) + 17, Z(POLE_BOT + 60), "EXISTING POLE D114 (NOT SUPPLIED)")

    # top view (from +Z): X to the right, Y up the sheet
    x, y, w, h = c["top"]
    Xt = lambda mx: x + (mx - bb.min.X) * k
    Yt = lambda my: y + h - (my - bb.min.Y) * k
    L += leader(Xt(D["panel_front_x_w"]), Yt(0), Xt(-120), Yt(bb.min.Y) + 4, "ARM AND PANEL FACE +X (EQUATOR)", "end")
    L += dim_h(Xt(D["anemo_x"] - P["cup_arm"] - P["cup_d"] / 2), Xt(D["reach"]), Yt(bb.max.Y) - 3, f"{D['reach']:.0f} reach")

    # right view (from +X): Y to the right... +Y appears to the right
    x, y, w, h = c["front"]
    L += leader(X(D["panel_front_x_w"]), Z(D["panel_low_z"]), X(D["panel_front_x_w"]) + 10, Z(D["panel_low_z"]) + 7,
                f"FIELDNODE PANEL, TILT {P['fn_tilt']:.0f} DEG")

    s._layers += L
    s.add_svg(views["iso"], 276, 32, 140, 100, label="Isometric view", sublabel="Not to scale")
    sw, sh, sd = P["saddle"]
    s.add_notes("Main dimensions and interfaces (mm)", [
        f"Pole D{P['pole_od']} design case; clamps fit {P['pole_range'][0]:.0f} to {P['pole_range'][1]:.0f}; no drilling",
        f"Arm {P['arm_w']:.0f} x {P['arm_w']:.0f} x {P['arm_t']:.0f} Al, {P['arm_len']:.0f} long, axis at {az:.0f}",
        f"Saddle {P['v_angle']:.0f} deg V, {sw:.0f} x {sh:.0f} x {sd:.0f}; two 13 mm strap bands",
        f"Shield {P['n_plates']} plates D{P['shield_d']:.0f} at {P['plate_pitch']:.0f} pitch; sensor at stack center",
        f"Fan {P['fan'][0]:.0f} x {P['fan'][1]:.0f} x {P['fan'][2]:.0f} 5 V in {P['cowl'][0]:.0f} sq cowl on the top plate",
        f"Globe D{P['globe_d']:.0f} copper, matte black; NTC bead at center",
        f"Anemometer mast {P['mast_h']:.0f} above the arm; cup circle D{2 * P['cup_arm'] + P['cup_d']:.0f}",
        "FieldNode core with sun shield per FND-DWG-001, below the arm, on 120 deg V adapter",
        "Lanyards: globe and shield to arm (secondary retention)",
        "Third-angle; front view from -Y; pole on the Z axis; +X to the equator",
    ], x=276, y=150, width=146)
    out = s.save(ROOT / "cad" / "drawings" / "HMN-DWG-001")
    shutil.rmtree(work, ignore_errors=True)
    print(f"wrote {out} and .pdf, .png at scale 1:{1 / k:g}")


if __name__ == "__main__":
    main()
