"""Geometry for the comparator's two drawings: the quality constellation
and the engine orbit. Positions only; every value drawn comes from the
dataset or from decision/'s own output.

Constellation: one per model, four axes (one per editorial quality
dimension), four fixed rings for SCHEMA.md's low/medium/high/very_high
scale. A vertex always sits on a ring, never between two: the scale is
discrete, so the drawing is too. The shape is not a score.

Orbit: the same rings as the result page's decision graph (graph.js).
Every catalog model is a dot on the ring the engine put it in for the
context; the selected models are lit. Angle inside a ring carries no
meaning: dots are spread evenly.
"""

import math

from decision.domain import AIModel

CONSTELLATION_SIZE = 240
_C = CONSTELLATION_SIZE / 2
_RING_STEP = 22
_AXES = (  # clockwise from the top
    ("reasoning", "Reasoning"),
    ("coding", "Coding"),
    ("creative_writing", "Writing"),
    ("instruction_following", "Instructions"),
)
_LEVELS = ("low", "medium", "high", "very high")

ORBIT_SIZE = 400
_O = ORBIT_SIZE / 2
_ORBIT_RINGS = (("alt", 74), ("tied", 114), ("out", 152), ("ex", 186))


def _fmt(points: list[tuple[float, float]]) -> str:
    return " ".join(f"{x:g},{y:g}" for x, y in points)


def _vertices(model: AIModel) -> list[dict]:
    directions = ((0, -1), (1, 0), (0, 1), (-1, 0))
    vertices = []
    for (attr, label), (dx, dy) in zip(_AXES, directions):
        ordinal = getattr(model.quality, attr).ordinal
        radius = _RING_STEP * (ordinal + 1)
        vertices.append({"x": _C + dx * radius, "y": _C + dy * radius, "title": f"{label}: {_LEVELS[ordinal]}"})
    return vertices


def constellation_frame() -> dict:
    """Rings and axis labels shared by every constellation."""
    edge = _RING_STEP * len(_LEVELS)
    label_at = edge + 14
    return {
        "size": CONSTELLATION_SIZE,
        # Wider than tall: the side labels sit outside the outer ring.
        "view_box": f"-48 0 {CONSTELLATION_SIZE + 96} {CONSTELLATION_SIZE}",
        "center": _C,
        "rings": [{"r": _RING_STEP * (i + 1), "label": level} for i, level in enumerate(_LEVELS)],
        "edge": edge,
        "labels": [
            {"text": _AXES[0][1], "x": _C, "y": _C - label_at, "anchor": "middle"},
            {"text": _AXES[1][1], "x": _C + label_at, "y": _C + 4, "anchor": "start"},
            {"text": _AXES[2][1], "x": _C, "y": _C + label_at + 8, "anchor": "middle"},
            {"text": _AXES[3][1], "x": _C - label_at, "y": _C + 4, "anchor": "end"},
        ],
    }


def constellations(selected: list[AIModel]) -> list[dict]:
    """One shape per model, with the other selected models' shapes as ghosts."""
    shapes = [_vertices(model) for model in selected]
    points = [_fmt([(v["x"], v["y"]) for v in shape]) for shape in shapes]
    return [
        {
            "model": model,
            "series": index + 1,
            "points": points[index],
            "vertices": shapes[index],
            "ghosts": [p for other, p in enumerate(points) if other != index],
        }
        for index, model in enumerate(selected)
    ]


def orbit(fit: dict, selected: list[AIModel]) -> dict:
    """Dot positions for every catalog model; the selected ones carry a series number."""
    series = {model.id: index + 1 for index, model in enumerate(selected)}
    cells = {model.id: cell for model, cell in zip(selected, fit["cells"])}

    def node(model: AIModel, ring: str, x: float, y: float) -> dict:
        cell = cells.get(model.id)
        mark = None
        if cell:
            mark = "×" if ring == "ex" else f"#{cell['rank']}"
        return {"x": round(x, 1), "y": round(y, 1), "ring": ring, "name": model.name, "series": series.get(model.id), "mark": mark}

    nodes = [node(model, "center", _O, _O) for model in fit["rings"]["center"]]
    for ring_index, (ring, radius) in enumerate(_ORBIT_RINGS):
        members = fit["rings"][ring]
        offset = -90 + ring_index * 23
        for k, model in enumerate(members):
            angle = math.radians(offset + 360 * k / len(members))
            nodes.append(node(model, ring, _O + radius * math.cos(angle), _O + radius * math.sin(angle)))
    # Lit dots last, so they are drawn on top.
    nodes.sort(key=lambda n: n["series"] is not None)
    return {
        "size": ORBIT_SIZE,
        "center": _O,
        "rings": [{"ring": ring, "r": radius} for ring, radius in _ORBIT_RINGS],
        "nodes": nodes,
    }


def podium(fit: dict, selected: list[AIModel]) -> list[dict]:
    """The selected models in the engine's order; excluded ones last."""
    entries = [
        {"model": model, "series": index + 1, "cell": cell}
        for index, (model, cell) in enumerate(zip(selected, fit["cells"]))
    ]
    return sorted(entries, key=lambda e: (e["cell"]["rank"] is None, e["cell"]["rank"] or 0))
