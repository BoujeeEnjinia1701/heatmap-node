"""Repo-specific geometry helpers for the HeatMap Node model (kit 1.9). Millimetres, build123d.

Small helpers the kit parts library (.kit/cad_parts.py) does not carry: boxes and cylinders placed by centre,
a cable swept along a polyline, strap bands round a pole, and the fasteners that cad_parts has no size for
(M3 and M4 screws and nuts, button-head and pan-head screws, nylon-insert and acorn nuts, ISO 7380 / 7045 style).
Suggested kit addition: ISO sizes M3 and M4 in cad_parts.ISO, and nyloc and acorn nuts.
"""
import math

import build123d as b


def box(cx, cy, cz, sx, sy, sz):
    return b.Pos(cx, cy, cz) * b.Box(sx, sy, sz)


def zcyl(x, y, z, r, h):
    return b.Pos(x, y, z) * b.Cylinder(r, h)


def rod(a, c, r):
    """Solid rod of radius r between two 3D points."""
    a, c = b.Vector(*a), b.Vector(*c)
    d = c - a
    return b.Solid.make_cylinder(r, d.length, b.Plane(origin=a, z_dir=d.normalized()))


def fuse(shapes):
    out = None
    for s in shapes:
        out = s if out is None else out + s
    return out


def path(points, r):
    """A cable or wire along a polyline, with round joints so the bends do not gap."""
    out = fuse(rod(a, c, r) for a, c in zip(points, points[1:]))
    for q in points[1:-1]:
        out = out + b.Pos(*q) * b.Sphere(r)
    return out


def hexnut(x, y, z0, af, h, bore, axis="z", blind=False):
    """Hex nut across flats af, height h, with a bore; base at z0 along +axis (axis 'z', '-z', 'y', '-y')."""
    n = b.extrude(b.RegularPolygon(af / math.sqrt(3), 6), amount=h)
    if blind:       # acorn nut: bore open at the base only, domed top
        n = n - b.Pos(0, 0, -0.01) * b.Cylinder(bore / 2, h * 0.7, align=(b.Align.CENTER, b.Align.CENTER, b.Align.MIN))
        n = n + b.Pos(0, 0, h) * (b.Sphere(af / 2 * 0.95) & b.Pos(0, 0, af) * b.Box(2 * af, 2 * af, 2 * af))
    else:
        n = n - b.Cylinder(bore / 2, 4 * h)
    rot = {"z": b.Rot(0, 0, 0), "-z": b.Rot(180, 0, 0), "y": b.Rot(-90, 0, 0), "-y": b.Rot(90, 0, 0)}[axis]
    return b.Pos(x, y, z0) * rot * n


def nut_local(af, h, bore, kind="plain"):
    """A nut in its own frame, from z = 0 to its height: plain hex, 'nyloc' (hex with a rounded nylon collar)
    or 'acorn' (domed, blind). Its bore is a clearance fit on a shank of diameter `bore`."""
    n = b.extrude(b.RegularPolygon(af / math.sqrt(3), 6), amount=h)
    if kind == "acorn":
        n = n - b.Pos(0, 0, -0.01) * b.Cylinder(bore / 2, h * 0.75, align=(b.Align.CENTER, b.Align.CENTER, b.Align.MIN))
        n = n + b.Pos(0, 0, h) * (b.Sphere(af / 2 * 0.95) & b.Pos(0, 0, af) * b.Box(2 * af, 2 * af, 2 * af))
        return n
    if kind == "nyloc":
        collar = b.Pos(0, 0, h) * b.Cylinder(af / 2 * 0.9, h * 0.45, align=(b.Align.CENTER, b.Align.CENTER, b.Align.MIN))
        n = n + collar
        return n - b.Cylinder(bore / 2, 4 * h)
    return n - b.Cylinder(bore / 2, 4 * h)


def pan_screw(d, length, head_d=None, head_h=None):
    """Pan-head machine screw, head on the XY plane from z = 0 up, shank down to -length."""
    head_d = head_d or 1.9 * d
    head_h = head_h or 0.65 * d
    head = b.Cylinder(head_d / 2, head_h, align=(b.Align.CENTER, b.Align.CENTER, b.Align.MIN))
    try:
        head = b.fillet(head.edges().sort_by(b.Axis.Z)[-1], head_h * 0.4)
    except Exception:
        pass
    shank = b.Pos(0, 0, -length / 2) * b.Cylinder(d / 2, length)
    try:
        shank = b.chamfer(shank.edges().sort_by(b.Axis.Z)[0], d * 0.08)
    except Exception:
        pass
    return head + shank


def button_screw(d, length):
    """ISO 7380 button-head screw: low dome head from z = 0 up, hex socket, shank down to -length."""
    hd, hh = 1.75 * d, 0.55 * d
    R = (hd * hd / 4 + hh * hh) / (2 * hh)
    dome = b.Pos(0, 0, hh - R) * b.Sphere(R)
    dome = dome & b.Pos(0, 0, hh / 2) * b.Box(hd, hd, hh)
    shank = b.Pos(0, 0, -length / 2) * b.Cylinder(d / 2, length)
    try:
        shank = b.chamfer(shank.edges().sort_by(b.Axis.Z)[0], d * 0.08)
    except Exception:
        pass
    sock = b.Pos(0, 0, hh - 0.25 * d) * b.extrude(b.RegularPolygon(0.3 * d, 6), amount=0.5 * d)
    return (dome + shank) - sock


def ring_band(points, w, t, z):
    """A thin strap band (width w, thickness t) whose centerline is the closed polygon points, at height z."""
    wire = b.Wire.make_polygon([b.Vector(x, y, 0) for x, y in points], close=True)
    outer = wire.offset_2d(t / 2, kind=b.Kind.INTERSECTION)
    inner = wire.offset_2d(-t / 2, kind=b.Kind.INTERSECTION)
    face = b.Face(outer, [inner])
    return b.Pos(0, 0, z - w / 2) * b.extrude(face, amount=w)


def band_path(r, sx, sy_in, sy_out, front, n=40):
    """Centerline of a band round the back of a pole of radius r (centred at the origin, the
    clamped part on +X): from the pole it runs to (sx, +/-sy) at x = sy_in, through slots to
    x = sy_out and across the front at x = front. Returns 2D points, counter-clockwise."""
    def tangent(px, py):
        d = math.hypot(px, py)
        a = math.atan2(py, px)
        da = math.acos(r / d)
        return a + da if py > 0 else a - da
    a1 = tangent(sy_in, sx)
    a2 = tangent(sy_in, -sx) + 2 * math.pi
    pts = [(front, -sx), (front, sx), (sy_out, sx), (sy_in, sx)]
    for i in range(n + 1):
        a = a1 + (a2 - a1) * i / n
        pts.append((r * math.cos(a), r * math.sin(a)))
    pts += [(sy_in, -sx), (sy_out, -sx)]
    return pts


def brk(shape, r=0.5):
    """Edge break (cad_parts.break_edges) that never raises."""
    import cad_parts
    try:
        return cad_parts.break_edges(shape, r)
    except Exception:
        return shape
