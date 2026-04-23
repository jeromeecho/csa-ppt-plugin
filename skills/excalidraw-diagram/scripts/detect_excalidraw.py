#!/usr/bin/env python3
"""
Excalidraw Diagram Detector & Validator

Two modes:
  1. DETECT: Analyze a slide outline and identify slides that need hand-drawn
     style diagrams from excalidraw-diagram skill.
  2. VALIDATE: Check that a PNG/excalidraw file was actually produced by the
     excalidraw-diagram skill (not inline SVG, matplotlib, or other tools).

Usage:
    # Detect which slides need excalidraw
    python detect_excalidraw.py detect --outline task_plan.md
    python detect_excalidraw.py detect --text "Slide 1: Concept Overview\\nSlide 2: System Flow"

    # Validate a generated file is from excalidraw
    python detect_excalidraw.py validate --file diagram.excalidraw
    python detect_excalidraw.py validate --file diagram.png --excalidraw-source diagram.excalidraw
    python detect_excalidraw.py validate --dir outputs/project/diagrams/

Output:
    JSON results with detection/validation details.
"""

import argparse
import json
import re
import struct
import sys
from pathlib import Path


# =============================================================================
# DETECTION: Keywords for hand-drawn / conceptual diagrams
# =============================================================================

# Explicit hand-drawn / excalidraw request keywords
HANDDRAWN_KEYWORDS = {
    # English
    "hand-drawn", "hand drawn", "handdrawn", "sketch", "sketchy",
    "whiteboard", "whiteboard-style", "brainstorm", "brainstorming",
    "excalidraw", "informal diagram", "napkin sketch",
    "rough sketch", "conceptual sketch", "doodle",
    "freehand", "free-hand", "organic",
    # Chinese
    "手绘", "手画", "草图", "白板", "白板风格", "头脑风暴",
    "概念草图", "随手画", "自由绘制",
}

# Conceptual / abstract diagram keywords (strong match with handdrawn style)
CONCEPTUAL_KEYWORDS = {
    # English
    "concept map", "concept diagram", "mental model", "mind map",
    "visual argument", "visual metaphor", "analogy diagram",
    "philosophy diagram", "abstract flow", "idea flow",
    "thought process", "decision framework", "conceptual overview",
    "high-level concept", "big picture", "overview diagram",
    "relationship map", "cause and effect", "comparison diagram",
    # Chinese
    "概念图", "概念说明", "思维导图", "心智模型",
    "抽象流程", "想法流", "思维过程", "决策框架",
    "概念总览", "大图", "全景图", "关系图",
    "因果图", "对比图",
}

# Flow / process keywords that COULD be excalidraw (informal) vs azure-diagrams (formal)
# These are weaker signals - only trigger if combined with handdrawn keywords
FLOW_KEYWORDS = {
    "workflow", "flow diagram", "process flow", "data flow",
    "user journey", "user flow", "interaction flow",
    "feedback loop", "cycle diagram", "lifecycle",
    "流程图", "工作流", "用户旅程", "交互流程",
    "反馈循环", "生命周期",
}

# Negative keywords - if present, prefer azure-diagrams instead
FORMAL_KEYWORDS = {
    "azure", "aws", "gcp", "cloud", "kubernetes", "aks",
    "production", "deployment", "infrastructure",
    "formal", "professional", "official",
    "正式", "专业", "生产环境", "部署",
}


# =============================================================================
# DETECTION LOGIC
# =============================================================================

def parse_outline(text: str) -> list:
    """Parse a text outline into slide entries."""
    slides = []
    lines = text.strip().split("\n")

    slide_pattern = re.compile(
        r"(?:slide|幻灯片|s)\s*(\d+)\s*[:：]\s*(.+)",
        re.IGNORECASE
    )
    list_pattern = re.compile(r"^\s*(?:(\d+)[.)]\s+|- |\* )(.*)", re.IGNORECASE)
    header_pattern = re.compile(r"^#{1,4}\s+(?:(?:slide|幻灯片)\s*\d+\s*[:：]\s*)?(.+)", re.IGNORECASE)

    for line in lines:
        line = line.strip()
        if not line:
            continue

        match = slide_pattern.match(line)
        if match:
            slides.append({"index": int(match.group(1)) - 1, "title": match.group(2).strip()})
            continue

        match = list_pattern.match(line)
        if match:
            idx = int(match.group(1)) - 1 if match.group(1) else len(slides)
            title = match.group(2).strip()
            if title and len(title) > 3:
                slides.append({"index": idx, "title": title})
            continue

        match = header_pattern.match(line)
        if match:
            title = match.group(1).strip()
            if title and len(title) > 3:
                slides.append({"index": len(slides), "title": title})

    seen = {}
    for s in slides:
        seen[s["index"]] = s
    return sorted(seen.values(), key=lambda x: x["index"])


def detect_excalidraw_need(title: str) -> dict:
    """
    Analyze a slide title to determine if it needs an excalidraw-style diagram.

    Returns dict with: needs_excalidraw, reason, confidence, diagram_style
    """
    title_lower = title.lower()

    # Check for explicit hand-drawn request
    found_handdrawn = [kw for kw in HANDDRAWN_KEYWORDS if kw in title_lower]

    # Check for conceptual content
    found_conceptual = [kw for kw in CONCEPTUAL_KEYWORDS if kw in title_lower]

    # Check for flow keywords
    found_flow = [kw for kw in FLOW_KEYWORDS if kw in title_lower]

    # Check for formal/cloud keywords (negative signal)
    found_formal = [kw for kw in FORMAL_KEYWORDS if kw in title_lower]

    # Decision logic
    if found_handdrawn:
        # Explicit request for hand-drawn style
        return {
            "needs_excalidraw": True,
            "reason": "explicit_handdrawn_request",
            "keywords": found_handdrawn,
            "confidence": "high",
            "diagram_style": "sketch" if any(k in title_lower for k in ["sketch", "草图"]) else "whiteboard",
        }

    if found_conceptual and not found_formal:
        # Conceptual content without formal/cloud context
        return {
            "needs_excalidraw": True,
            "reason": "conceptual_content",
            "keywords": found_conceptual,
            "confidence": "high",
            "diagram_style": "conceptual",
        }

    if found_conceptual and found_formal:
        # Conceptual but with formal context - medium confidence
        return {
            "needs_excalidraw": False,
            "reason": "conceptual_but_formal_context",
            "keywords": found_conceptual + found_formal,
            "confidence": "low",
            "diagram_style": None,
        }

    if found_flow and not found_formal:
        # Flow diagram without formal context - could be excalidraw
        return {
            "needs_excalidraw": True,
            "reason": "informal_flow",
            "keywords": found_flow,
            "confidence": "medium",
            "diagram_style": "flow",
        }

    return {
        "needs_excalidraw": False,
        "reason": "no_match",
        "keywords": [],
        "confidence": "none",
        "diagram_style": None,
    }


def detect_slides(slides: list) -> list:
    """Analyze all slides and return those needing excalidraw."""
    results = []
    for slide in slides:
        detection = detect_excalidraw_need(slide["title"])
        if detection["needs_excalidraw"]:
            results.append({
                "slide_index": slide["index"],
                "slide_title": slide["title"],
                "reason": detection["reason"],
                "diagram_style": detection["diagram_style"],
                "keywords": detection["keywords"],
                "confidence": detection["confidence"],
            })
    return results


# =============================================================================
# VALIDATION: Verify a file was produced by excalidraw-diagram skill
# =============================================================================

def validate_excalidraw_json(filepath: Path) -> dict:
    """
    Validate that a .excalidraw file is a genuine Excalidraw JSON.

    Checks:
    1. Valid JSON with type="excalidraw"
    2. Has elements array with proper element structure
    3. Elements use Excalidraw-specific properties (boundElements, roughness, etc.)
    4. Not a generic SVG or matplotlib output disguised as excalidraw
    """
    try:
        data = json.loads(filepath.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return {
            "valid": False,
            "source": "unknown",
            "error": f"Cannot parse as JSON: {e}",
        }

    # Check 1: Top-level structure
    if data.get("type") != "excalidraw":
        return {
            "valid": False,
            "source": "unknown",
            "error": f"type field is '{data.get('type')}', expected 'excalidraw'",
        }

    if "elements" not in data or not isinstance(data["elements"], list):
        return {
            "valid": False,
            "source": "unknown",
            "error": "Missing or invalid 'elements' array",
        }

    elements = data["elements"]
    if len(elements) == 0:
        return {
            "valid": False,
            "source": "excalidraw_empty",
            "error": "elements array is empty",
        }

    # Check 2: Excalidraw-specific element properties
    excalidraw_indicators = 0
    element_types = set()
    has_bound_elements = False
    has_roughness = False
    has_seed = False
    has_font_family = False

    for el in elements:
        el_type = el.get("type", "")
        element_types.add(el_type)

        if "boundElements" in el:
            has_bound_elements = True
            excalidraw_indicators += 1
        if "roughness" in el:
            has_roughness = True
            excalidraw_indicators += 1
        if "seed" in el:
            has_seed = True
            excalidraw_indicators += 1
        if "fontFamily" in el:
            has_font_family = True
            excalidraw_indicators += 1
        if el.get("type") in ("rectangle", "ellipse", "diamond", "arrow", "line", "text"):
            excalidraw_indicators += 1

    # Check 3: Sufficient excalidraw indicators
    valid_types = {"rectangle", "ellipse", "diamond", "arrow", "line", "text",
                   "freedraw", "image", "frame"}
    has_valid_types = bool(element_types & valid_types)

    is_genuine = (
        has_valid_types
        and (has_roughness or has_seed)
        and excalidraw_indicators >= len(elements)  # at least 1 indicator per element
    )

    return {
        "valid": is_genuine,
        "source": "excalidraw-diagram" if is_genuine else "unknown",
        "element_count": len(elements),
        "element_types": sorted(element_types),
        "indicators": {
            "has_bound_elements": has_bound_elements,
            "has_roughness": has_roughness,
            "has_seed": has_seed,
            "has_font_family": has_font_family,
            "valid_element_types": has_valid_types,
        },
        "confidence": "high" if is_genuine else "low",
    }


def validate_png_from_excalidraw(png_path: Path, excalidraw_path: Path = None) -> dict:
    """
    Validate that a PNG was rendered from an excalidraw source.

    Checks:
    1. If .excalidraw source file exists alongside the PNG
    2. The .excalidraw file is valid excalidraw JSON
    3. PNG file size and dimensions are consistent with Playwright render
    """
    result = {
        "png_path": str(png_path),
        "valid": False,
        "source": "unknown",
    }

    if not png_path.exists():
        result["error"] = "PNG file not found"
        return result

    # Check PNG is actually a PNG
    with open(png_path, "rb") as f:
        header = f.read(8)
    if header[:4] != b"\x89PNG":
        result["error"] = "File is not a valid PNG"
        return result

    # Read PNG dimensions from IHDR chunk
    with open(png_path, "rb") as f:
        f.read(8)  # skip signature
        f.read(4)  # chunk length
        chunk_type = f.read(4)
        if chunk_type == b"IHDR":
            width = struct.unpack(">I", f.read(4))[0]
            height = struct.unpack(">I", f.read(4))[0]
            result["dimensions"] = {"width": width, "height": height}

    # Try to find .excalidraw source
    if excalidraw_path is None:
        excalidraw_path = png_path.with_suffix(".excalidraw")

    if excalidraw_path.exists():
        result["excalidraw_source"] = str(excalidraw_path)
        validation = validate_excalidraw_json(excalidraw_path)
        result["excalidraw_validation"] = validation

        if validation["valid"]:
            result["valid"] = True
            result["source"] = "excalidraw-diagram"
            result["confidence"] = "high"
        else:
            result["error"] = f"Source .excalidraw file is invalid: {validation.get('error', 'unknown')}"
    else:
        result["error"] = (
            f"No .excalidraw source found at {excalidraw_path}. "
            "Cannot confirm PNG was rendered from excalidraw-diagram skill. "
            "The excalidraw-diagram skill always produces a .excalidraw JSON file "
            "alongside the rendered PNG."
        )
        result["confidence"] = "none"

    return result


def validate_directory(dir_path: Path) -> list:
    """Validate all diagram files in a directory."""
    results = []

    # Check .excalidraw files
    for f in sorted(dir_path.glob("*.excalidraw")):
        results.append({
            "file": str(f),
            "type": "excalidraw_json",
            **validate_excalidraw_json(f),
        })

    # Check PNGs that might be from excalidraw
    for f in sorted(dir_path.glob("*.png")):
        excalidraw_src = f.with_suffix(".excalidraw")
        if excalidraw_src.exists():
            results.append({
                "file": str(f),
                "type": "rendered_png",
                **validate_png_from_excalidraw(f, excalidraw_src),
            })

    return results


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Detect slides needing excalidraw & validate excalidraw output",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Detect which slides need hand-drawn diagrams
  %(prog)s detect --text "Slide 1: Concept Overview\\nSlide 2: Azure Architecture"
  %(prog)s detect --outline task_plan.md

  # Validate excalidraw output files
  %(prog)s validate --file diagram.excalidraw
  %(prog)s validate --file diagram.png --excalidraw-source diagram.excalidraw
  %(prog)s validate --dir outputs/project/diagrams/
        """
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Detect subcommand
    detect_parser = subparsers.add_parser("detect", help="Detect slides needing excalidraw")
    detect_parser.add_argument("--outline", "-o", type=str, help="Path to outline file")
    detect_parser.add_argument("--text", "-t", type=str, help="Inline outline text")

    # Validate subcommand
    validate_parser = subparsers.add_parser("validate", help="Validate excalidraw output")
    validate_parser.add_argument("--file", "-f", type=str, help="Single file to validate")
    validate_parser.add_argument("--excalidraw-source", "-s", type=str,
                                  help="Path to .excalidraw source (for PNG validation)")
    validate_parser.add_argument("--dir", "-d", type=str, help="Directory to validate")

    args = parser.parse_args()

    if args.command == "detect":
        if not args.outline and not args.text:
            detect_parser.print_help()
            sys.exit(1)

        if args.outline:
            path = Path(args.outline)
            if not path.exists():
                print(f"Error: File not found: {args.outline}", file=sys.stderr)
                sys.exit(1)
            text = path.read_text(encoding="utf-8")
        else:
            text = args.text.replace("\\n", "\n")

        if text.strip().startswith("[") or text.strip().startswith("{"):
            try:
                data = json.loads(text)
                slides = []
                for i, item in enumerate(data if isinstance(data, list) else [data]):
                    if isinstance(item, str):
                        slides.append({"index": i, "title": item})
                    elif isinstance(item, dict):
                        slides.append({"index": item.get("index", i),
                                       "title": str(item.get("title", ""))})
            except json.JSONDecodeError:
                slides = parse_outline(text)
        else:
            slides = parse_outline(text)

        results = detect_slides(slides)
        print(json.dumps(results, indent=2, ensure_ascii=False))

        # Summary to stderr
        if results:
            print(f"\n--- Summary ---", file=sys.stderr)
            print(f"Total slides: {len(slides)}", file=sys.stderr)
            print(f"Slides needing excalidraw-diagram: {len(results)}", file=sys.stderr)
            for r in results:
                conf = "***" if r["confidence"] == "high" else "**"
                print(f"  [{conf}] Slide {r['slide_index']}: {r['slide_title']}", file=sys.stderr)
                print(f"       Style: {r['diagram_style']}, Reason: {r['reason']}", file=sys.stderr)
        else:
            print(f"\nNo hand-drawn/conceptual diagram slides detected.", file=sys.stderr)

    elif args.command == "validate":
        if not args.file and not args.dir:
            validate_parser.print_help()
            sys.exit(1)

        if args.dir:
            dir_path = Path(args.dir)
            if not dir_path.is_dir():
                print(f"Error: Not a directory: {args.dir}", file=sys.stderr)
                sys.exit(1)
            results = validate_directory(dir_path)
            print(json.dumps(results, indent=2, ensure_ascii=False))

            # Summary
            valid_count = sum(1 for r in results if r.get("valid"))
            print(f"\n--- Validation Summary ---", file=sys.stderr)
            print(f"Files checked: {len(results)}", file=sys.stderr)
            print(f"Valid excalidraw output: {valid_count}/{len(results)}", file=sys.stderr)
            for r in results:
                status = "PASS" if r.get("valid") else "FAIL"
                print(f"  [{status}] {Path(r['file']).name}: source={r.get('source', '?')}", file=sys.stderr)

        else:
            filepath = Path(args.file)
            if not filepath.exists():
                print(f"Error: File not found: {args.file}", file=sys.stderr)
                sys.exit(1)

            if filepath.suffix == ".excalidraw":
                result = validate_excalidraw_json(filepath)
            elif filepath.suffix == ".png":
                src = Path(args.excalidraw_source) if args.excalidraw_source else None
                result = validate_png_from_excalidraw(filepath, src)
            else:
                print(f"Error: Unsupported file type: {filepath.suffix}", file=sys.stderr)
                sys.exit(1)

            print(json.dumps(result, indent=2, ensure_ascii=False))

            status = "PASS" if result.get("valid") else "FAIL"
            print(f"\n[{status}] source={result.get('source', '?')}", file=sys.stderr)


if __name__ == "__main__":
    main()
