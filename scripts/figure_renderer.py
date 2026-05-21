#!/usr/bin/env python3
"""Deterministic FigureSpec JSON -> SVG renderer.

This is a lightweight local port of the upstream idea, adapted to this repo's
`scripts/` layout. It is intended for publication-style workflow and
architecture figures where reproducibility matters more than illustration.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, tostring


DEFAULT_STYLE = {
    "font_family": "Helvetica, Arial, sans-serif",
    "font_size": 14,
    "background": "#FFFFFF",
    "palette": [
        "#1D4ED8",
        "#059669",
        "#9333EA",
        "#EA580C",
        "#B91C1C",
        "#0F766E",
        "#7C3AED",
    ],
}

DEFAULT_NODE = {
    "width": 132,
    "height": 52,
    "shape": "rounded",
    "stroke": "#334155",
    "fill": None,
    "text_color": "#0F172A",
}

DEFAULT_EDGE = {
    "style": "solid",
    "color": "#475569",
    "thickness": 2,
    "curve": False,
}

DEFAULT_GROUP = {
    "fill": "#F8FAFC",
    "stroke": "#CBD5E1",
    "padding": 28,
}

HEX_COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")
ALLOWED_SHAPES = {"rect", "rounded", "circle", "ellipse", "diamond"}
ALLOWED_EDGE_STYLES = {"solid", "dashed", "dotted"}


def load_spec(path: str) -> dict[str, Any]:
    with open(path) as handle:
        spec = json.load(handle)
    if not isinstance(spec, dict):
        raise ValueError("Figure spec must be a JSON object")
    return spec


def sanitize_text(text: Any) -> str:
    value = str(text)
    value = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", value)
    return value


def sanitize_color(value: Any, fallback: str) -> str:
    if isinstance(value, str) and HEX_COLOR_RE.match(value):
        return value
    return fallback


def lighten(color: str, weight: float = 0.82) -> str:
    color = color.lstrip("#")
    r = int(color[0:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:6], 16)
    r = min(255, int(r + (255 - r) * weight))
    g = min(255, int(g + (255 - g) * weight))
    b = min(255, int(b + (255 - b) * weight))
    return f"#{r:02x}{g:02x}{b:02x}"


def approx_text_width(text: str, font_size: float) -> float:
    width = 0.0
    for char in text:
        width += font_size * (1.0 if ord(char) > 0x2E80 else 0.58)
    return width


def validate_spec(spec: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    canvas = spec.get("canvas", {})
    if not isinstance(canvas, dict):
        issues.append("CRITICAL: canvas must be a dict")
        canvas = {}

    for dim in ("width", "height"):
        value = canvas.get(dim)
        if not isinstance(value, (int, float)) or value <= 0:
            issues.append(f"CRITICAL: canvas.{dim} must be a positive number")

    nodes = spec.get("nodes", [])
    edges = spec.get("edges", [])
    groups = spec.get("groups", [])
    labels = spec.get("labels", [])

    if not isinstance(nodes, list):
        issues.append("CRITICAL: nodes must be a list")
        nodes = []
    if not isinstance(edges, list):
        issues.append("CRITICAL: edges must be a list")
        edges = []
    if not isinstance(groups, list):
        issues.append("CRITICAL: groups must be a list")
        groups = []
    if not isinstance(labels, list):
        issues.append("CRITICAL: labels must be a list")
        labels = []

    node_ids: set[str] = set()
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            issues.append(f"CRITICAL: nodes[{index}] must be an object")
            continue
        node_id = node.get("id")
        if not isinstance(node_id, str) or not node_id:
            issues.append(f"CRITICAL: nodes[{index}] is missing a valid id")
        elif node_id in node_ids:
            issues.append(f"CRITICAL: duplicate node id '{node_id}'")
        else:
            node_ids.add(node_id)
        for key in ("x", "y"):
            if not isinstance(node.get(key), (int, float)):
                issues.append(f"CRITICAL: node '{node_id or index}' is missing numeric {key}")
        shape = node.get("shape", DEFAULT_NODE["shape"])
        if shape not in ALLOWED_SHAPES:
            issues.append(f"CRITICAL: node '{node_id or index}' has invalid shape '{shape}'")

    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            issues.append(f"CRITICAL: edges[{index}] must be an object")
            continue
        source = edge.get("from")
        target = edge.get("to")
        if source not in node_ids:
            issues.append(f"CRITICAL: edge {index} references unknown source '{source}'")
        if target not in node_ids:
            issues.append(f"CRITICAL: edge {index} references unknown target '{target}'")
        style = edge.get("style", DEFAULT_EDGE["style"])
        if style not in ALLOWED_EDGE_STYLES:
            issues.append(f"CRITICAL: edge {index} has invalid style '{style}'")

    for index, group in enumerate(groups):
        if not isinstance(group, dict):
            issues.append(f"CRITICAL: groups[{index}] must be an object")
            continue
        group_nodes = group.get("node_ids", [])
        if not isinstance(group_nodes, list) or not group_nodes:
            issues.append(f"CRITICAL: group {index} must define non-empty node_ids")
            continue
        for node_id in group_nodes:
            if node_id not in node_ids:
                issues.append(f"CRITICAL: group {index} references unknown node '{node_id}'")

    for index, label in enumerate(labels):
        if not isinstance(label, dict):
            issues.append(f"CRITICAL: labels[{index}] must be an object")
            continue
        for key in ("text", "x", "y"):
            if key == "text":
                if not isinstance(label.get(key), str):
                    issues.append(f"CRITICAL: labels[{index}] must define text")
            elif not isinstance(label.get(key), (int, float)):
                issues.append(f"CRITICAL: labels[{index}] must define numeric {key}")

    return issues


def merge_style(spec: dict[str, Any]) -> dict[str, Any]:
    style = dict(DEFAULT_STYLE)
    if isinstance(spec.get("style"), dict):
        style.update(spec["style"])
    style["background"] = sanitize_color(style.get("background"), DEFAULT_STYLE["background"])
    palette = style.get("palette")
    if not isinstance(palette, list) or not palette:
        style["palette"] = list(DEFAULT_STYLE["palette"])
    else:
        style["palette"] = [sanitize_color(color, DEFAULT_STYLE["palette"][0]) for color in palette]
    return style


def node_map(spec: dict[str, Any], style: dict[str, Any]) -> dict[str, dict[str, Any]]:
    nodes: dict[str, dict[str, Any]] = {}
    palette = style["palette"]
    for index, raw in enumerate(spec.get("nodes", [])):
        node = dict(DEFAULT_NODE)
        node.update(raw)
        node["label"] = sanitize_text(node.get("label", node["id"]))
        node["shape"] = node.get("shape", DEFAULT_NODE["shape"])
        node["stroke"] = sanitize_color(node.get("stroke"), DEFAULT_NODE["stroke"])
        if node.get("fill") is None:
            node["fill"] = lighten(palette[index % len(palette)])
        else:
            node["fill"] = sanitize_color(node.get("fill"), lighten(palette[index % len(palette)]))
        node["text_color"] = sanitize_color(node.get("text_color"), DEFAULT_NODE["text_color"])
        node["font_size"] = node.get("font_size") or style["font_size"]
        nodes[node["id"]] = node
    return nodes


def clip_to_shape(node: dict[str, Any], target_x: float, target_y: float) -> tuple[float, float]:
    cx = float(node["x"])
    cy = float(node["y"])
    dx = target_x - cx
    dy = target_y - cy
    if dx == 0 and dy == 0:
        return cx, cy

    shape = node["shape"]
    width = float(node["width"])
    height = float(node["height"])

    if shape == "circle":
        radius = max(width, height) / 2
        angle = math.atan2(dy, dx)
        return cx + radius * math.cos(angle), cy + radius * math.sin(angle)

    if shape == "ellipse":
        angle = math.atan2(dy, dx)
        return cx + (width / 2) * math.cos(angle), cy + (height / 2) * math.sin(angle)

    if shape == "diamond":
        a = width / 2
        b = height / 2
        denom = abs(dx) * b + abs(dy) * a
        if denom == 0:
            return cx, cy
        scale = (a * b) / denom
        return cx + dx * scale, cy + dy * scale

    half_w = width / 2
    half_h = height / 2
    if abs(dx) * half_h > abs(dy) * half_w:
        scale = half_w / abs(dx)
    else:
        scale = half_h / abs(dy)
    return cx + dx * scale, cy + dy * scale


def render_text(parent: Element, text: str, x: float, y: float, font_size: float, color: str, family: str) -> None:
    lines = text.split("\n")
    total_height = (len(lines) - 1) * font_size * 1.2
    base_y = y - total_height / 2
    for index, line in enumerate(lines):
        text_el = SubElement(
            parent,
            "text",
            {
                "x": f"{x:.1f}",
                "y": f"{base_y + index * font_size * 1.2:.1f}",
                "text-anchor": "middle",
                "dominant-baseline": "middle",
                "font-family": family,
                "font-size": f"{font_size:.1f}",
                "fill": color,
            },
        )
        text_el.text = sanitize_text(line)


def render_node(parent: Element, node: dict[str, Any], style: dict[str, Any]) -> None:
    x = float(node["x"])
    y = float(node["y"])
    width = float(node["width"])
    height = float(node["height"])
    attrs = {
        "fill": node["fill"],
        "stroke": node["stroke"],
        "stroke-width": "1.8",
    }

    if node["shape"] in {"rect", "rounded"}:
        attrs.update(
            {
                "x": f"{x - width / 2:.1f}",
                "y": f"{y - height / 2:.1f}",
                "width": f"{width:.1f}",
                "height": f"{height:.1f}",
            }
        )
        if node["shape"] == "rounded":
            attrs["rx"] = "14"
            attrs["ry"] = "14"
        SubElement(parent, "rect", attrs)
    elif node["shape"] == "circle":
        SubElement(parent, "circle", {"cx": f"{x:.1f}", "cy": f"{y:.1f}", "r": f"{max(width, height)/2:.1f}", **attrs})
    elif node["shape"] == "ellipse":
        SubElement(parent, "ellipse", {"cx": f"{x:.1f}", "cy": f"{y:.1f}", "rx": f"{width/2:.1f}", "ry": f"{height/2:.1f}", **attrs})
    else:
        top = (x, y - height / 2)
        right = (x + width / 2, y)
        bottom = (x, y + height / 2)
        left = (x - width / 2, y)
        points = " ".join(f"{px:.1f},{py:.1f}" for px, py in (top, right, bottom, left))
        SubElement(parent, "polygon", {"points": points, **attrs})

    render_text(parent, node["label"], x, y, float(node["font_size"]), node["text_color"], style["font_family"])


def render_edge(parent: Element, edge: dict[str, Any], nodes: dict[str, dict[str, Any]], style: dict[str, Any]) -> None:
    source = nodes[edge["from"]]
    target = nodes[edge["to"]]
    sx, sy = clip_to_shape(source, float(target["x"]), float(target["y"]))
    tx, ty = clip_to_shape(target, float(source["x"]), float(source["y"]))

    stroke = sanitize_color(edge.get("color"), DEFAULT_EDGE["color"])
    thickness = float(edge.get("thickness", DEFAULT_EDGE["thickness"]))
    dash = None
    if edge.get("style") == "dashed":
        dash = "8 6"
    elif edge.get("style") == "dotted":
        dash = "2 5"

    attrs = {
        "fill": "none",
        "stroke": stroke,
        "stroke-width": f"{thickness:.1f}",
        "marker-end": "url(#arrowhead)",
    }
    if dash:
        attrs["stroke-dasharray"] = dash

    if edge.get("curve"):
        mid_x = (sx + tx) / 2
        mid_y = (sy + ty) / 2 - 40
        path_d = f"M {sx:.1f} {sy:.1f} Q {mid_x:.1f} {mid_y:.1f} {tx:.1f} {ty:.1f}"
    else:
        path_d = f"M {sx:.1f} {sy:.1f} L {tx:.1f} {ty:.1f}"
    SubElement(parent, "path", {"d": path_d, **attrs})

    label = edge.get("label")
    if label:
        label_x = (sx + tx) / 2
        label_y = (sy + ty) / 2 - (18 if edge.get("curve") else 12)
        render_text(parent, sanitize_text(label), label_x, label_y, style["font_size"] - 1, stroke, style["font_family"])


def render_groups(parent: Element, groups: list[dict[str, Any]], nodes: dict[str, dict[str, Any]], style: dict[str, Any]) -> None:
    for group in groups:
        merged = dict(DEFAULT_GROUP)
        merged.update(group)
        members = [nodes[node_id] for node_id in group["node_ids"]]
        pad = float(merged["padding"])
        min_x = min(float(node["x"]) - float(node["width"]) / 2 for node in members) - pad
        min_y = min(float(node["y"]) - float(node["height"]) / 2 for node in members) - pad
        max_x = max(float(node["x"]) + float(node["width"]) / 2 for node in members) + pad
        max_y = max(float(node["y"]) + float(node["height"]) / 2 for node in members) + pad
        SubElement(
            parent,
            "rect",
            {
                "x": f"{min_x:.1f}",
                "y": f"{min_y:.1f}",
                "width": f"{max_x - min_x:.1f}",
                "height": f"{max_y - min_y:.1f}",
                "rx": "18",
                "ry": "18",
                "fill": sanitize_color(merged["fill"], DEFAULT_GROUP["fill"]),
                "stroke": sanitize_color(merged["stroke"], DEFAULT_GROUP["stroke"]),
                "stroke-width": "1.2",
            },
        )
        if group.get("label"):
            render_text(
                parent,
                sanitize_text(group["label"]),
                min_x + 12 + approx_text_width(group["label"], style["font_size"] - 1) / 2,
                min_y + 18,
                style["font_size"] - 1,
                sanitize_color(merged.get("stroke"), DEFAULT_GROUP["stroke"]),
                style["font_family"],
            )


def render_svg(spec: dict[str, Any]) -> str:
    style = merge_style(spec)
    nodes = node_map(spec, style)
    width = float(spec["canvas"]["width"])
    height = float(spec["canvas"]["height"])

    svg = Element(
        "svg",
        {
            "xmlns": "http://www.w3.org/2000/svg",
            "width": f"{width:.0f}",
            "height": f"{height:.0f}",
            "viewBox": f"0 0 {width:.0f} {height:.0f}",
        },
    )

    defs = SubElement(svg, "defs")
    marker = SubElement(
        defs,
        "marker",
        {
            "id": "arrowhead",
            "markerWidth": "10",
            "markerHeight": "7",
            "refX": "9",
            "refY": "3.5",
            "orient": "auto",
        },
    )
    SubElement(marker, "polygon", {"points": "0 0, 10 3.5, 0 7", "fill": "#475569"})
    SubElement(svg, "rect", {"x": "0", "y": "0", "width": f"{width:.0f}", "height": f"{height:.0f}", "fill": style["background"]})

    group_layer = SubElement(svg, "g", {"id": "groups"})
    edge_layer = SubElement(svg, "g", {"id": "edges"})
    node_layer = SubElement(svg, "g", {"id": "nodes"})
    label_layer = SubElement(svg, "g", {"id": "labels"})

    render_groups(group_layer, spec.get("groups", []), nodes, style)
    for edge in spec.get("edges", []):
        merged = dict(DEFAULT_EDGE)
        merged.update(edge)
        render_edge(edge_layer, merged, nodes, style)
    for node in nodes.values():
        render_node(node_layer, node, style)
    for label in spec.get("labels", []):
        render_text(
            label_layer,
            sanitize_text(label["text"]),
            float(label["x"]),
            float(label["y"]),
            float(label.get("font_size", style["font_size"])),
            sanitize_color(label.get("color"), "#334155"),
            style["font_family"],
        )

    rough = tostring(svg, encoding="unicode")
    return minidom.parseString(rough).toprettyxml(indent="  ")


def schema_template() -> dict[str, Any]:
    return {
        "canvas": {"width": 900, "height": 320},
        "style": {
            "font_family": "Helvetica, Arial, sans-serif",
            "font_size": 14,
            "background": "#FFFFFF",
            "palette": ["#1D4ED8", "#059669", "#9333EA"],
        },
        "nodes": [
            {"id": "input", "label": "Input", "x": 120, "y": 160},
            {"id": "process", "label": "Process", "x": 320, "y": 160},
            {"id": "output", "label": "Output", "x": 520, "y": 160},
        ],
        "edges": [
            {"from": "input", "to": "process"},
            {"from": "process", "to": "output", "label": "produces"},
        ],
        "groups": [
            {"label": "Main Flow", "node_ids": ["input", "process", "output"]},
        ],
        "labels": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Render deterministic SVG figures from FigureSpec JSON.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    render_parser = subparsers.add_parser("render", help="Render a FigureSpec JSON file to SVG.")
    render_parser.add_argument("spec")
    render_parser.add_argument("--output", required=True)

    validate_parser = subparsers.add_parser("validate", help="Validate a FigureSpec JSON file.")
    validate_parser.add_argument("spec")

    subparsers.add_parser("schema", help="Print a starter FigureSpec JSON schema.")

    args = parser.parse_args()

    if args.command == "schema":
        print(json.dumps(schema_template(), indent=2))
        return 0

    spec = load_spec(args.spec)
    issues = validate_spec(spec)
    if args.command == "validate":
        if issues:
            print("\n".join(issues))
            return 1
        print("OK")
        return 0

    if issues:
        print("\n".join(issues), file=sys.stderr)
        return 1

    svg = render_svg(spec)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(svg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
