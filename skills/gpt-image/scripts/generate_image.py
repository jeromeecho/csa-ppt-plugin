#!/usr/bin/env python3
"""
GPT-image-2 Image Generator for CSA Presentations.

Generates images via Azure OpenAI GPT-image-2 deployment.
Designed to be called inline from Claude Code (not as a standalone script).

Configuration priority (highest → lowest):
    1. CLI arguments (--endpoint, --api-key, --deployment)
    2. config.json (in skill root: gpt-image/config.json)
    3. Environment variables (AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, GPT_IMAGE_DEPLOYMENT)

Usage (inline):
    python3 << 'EOF'
    exec(open("path/to/generate_image.py").read())
    generate_image(
        prompt="A modern data center with holographic dashboards",
        output_path="outputs/project/diagrams/cover.png",
        size="1536x1024",
        quality="high"
    )
    EOF

Usage (CLI):
    python3 generate_image.py --prompt "..." --output "path/to/image.png" \\
        --size 1536x1024 --quality high

    # First-time setup — fill in config.json:
    python3 generate_image.py config
"""

import os
import sys
import json
import base64
import argparse
import requests
from pathlib import Path

# Default configuration
DEFAULT_DEPLOYMENT = "gpt-image-2"
DEFAULT_API_VERSION = "2025-04-01-preview"
DEFAULT_SIZE = "1536x1024"
DEFAULT_QUALITY = "high"
DEFAULT_FORMAT = "png"

# PPT-optimized size presets
SIZE_PRESETS = {
    "slide-full":    "1920x1080",   # 16:9 full slide background
    "slide-right":   "1024x1024",   # Square for right-panel in 左文右图
    "slide-wide":    "1536x1024",   # 3:2 wide, fits most layouts
    "slide-tall":    "1024x1536",   # 2:3 vertical illustration
    "4k":            "3840x2160",   # 4K for print or high-res
    "banner":        "1920x640",    # Wide banner strip
    "icon-large":    "512x512",     # Large icon
}


## Config file path: gpt-image/config.json (next to scripts/)
SKILL_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = SKILL_ROOT / "config.json"


def _load_config_file():
    """Load config.json if it exists and has non-empty values."""
    if not CONFIG_PATH.exists():
        return {}
    try:
        with open(CONFIG_PATH, "r") as f:
            data = json.load(f)
        # Only return non-empty values
        return {k: v for k, v in data.items() if v}
    except (json.JSONDecodeError, IOError):
        return {}


def get_config(cli_endpoint=None, cli_api_key=None, cli_deployment=None):
    """
    Read Azure OpenAI configuration.
    Priority: CLI args > config.json > environment variables.
    """
    file_cfg = _load_config_file()

    endpoint = (
        cli_endpoint
        or file_cfg.get("azure_openai_endpoint")
        or os.environ.get("AZURE_OPENAI_ENDPOINT", "")
    )
    api_key = (
        cli_api_key
        or file_cfg.get("azure_openai_api_key")
        or os.environ.get("AZURE_OPENAI_API_KEY", "")
    )
    deployment = (
        cli_deployment
        or file_cfg.get("deployment_name")
        or os.environ.get("GPT_IMAGE_DEPLOYMENT", DEFAULT_DEPLOYMENT)
    )

    if not endpoint:
        raise EnvironmentError(
            "Azure OpenAI endpoint not configured.\n"
            f"  Option 1: Edit {CONFIG_PATH}\n"
            "  Option 2: export AZURE_OPENAI_ENDPOINT='https://your-resource.openai.azure.com/'"
        )
    if not api_key:
        raise EnvironmentError(
            "Azure OpenAI API key not configured.\n"
            f"  Option 1: Edit {CONFIG_PATH}\n"
            "  Option 2: export AZURE_OPENAI_API_KEY='your-key'"
        )

    # Ensure endpoint ends with /
    if not endpoint.endswith("/"):
        endpoint += "/"

    return endpoint, api_key, deployment


def resolve_size(size_or_preset):
    """Resolve a size string or preset name to WxH format."""
    if size_or_preset in SIZE_PRESETS:
        return SIZE_PRESETS[size_or_preset]
    # Validate WxH format
    parts = size_or_preset.lower().split("x")
    if len(parts) != 2:
        raise ValueError(f"Invalid size '{size_or_preset}'. Use WxH or a preset: {list(SIZE_PRESETS.keys())}")
    w, h = int(parts[0]), int(parts[1])
    if w % 16 != 0 or h % 16 != 0:
        raise ValueError(f"Both dimensions must be multiples of 16. Got {w}x{h}")
    if w * h < 655360:
        raise ValueError(f"Pixel count {w*h} below minimum 655,360")
    if w * h > 8294400:
        raise ValueError(f"Pixel count {w*h} above maximum 8,294,400")
    if max(w, h) > 3840:
        raise ValueError(f"Long edge {max(w,h)} exceeds 3840px limit")
    return f"{w}x{h}"


def generate_image(
    prompt,
    output_path,
    size=DEFAULT_SIZE,
    quality=DEFAULT_QUALITY,
    output_format=DEFAULT_FORMAT,
    background="auto",
    n=1,
):
    """
    Generate an image using Azure OpenAI GPT-image-2.

    Args:
        prompt: Text description of the desired image
        output_path: File path to save the generated PNG/JPEG/WEBP
        size: Image dimensions (WxH or preset name)
        quality: "low", "medium", or "high"
        output_format: "png", "jpeg", or "webp"
        background: "auto" or "transparent" (PNG only)
        n: Number of images (1-10, generates {name}_1.png, {name}_2.png, ...)

    Returns:
        List of saved file paths
    """
    endpoint, api_key, deployment = get_config()
    size = resolve_size(size)

    url = f"{endpoint}openai/deployments/{deployment}/images/generations?api-version={DEFAULT_API_VERSION}"

    body = {
        "prompt": prompt,
        "n": n,
        "size": size,
        "quality": quality,
        "output_format": output_format,
    }

    if background == "transparent" and output_format == "png":
        body["background"] = "transparent"

    print(f"Generating image...")
    print(f"  Prompt:  {prompt[:80]}{'...' if len(prompt) > 80 else ''}")
    print(f"  Size:    {size}")
    print(f"  Quality: {quality}")
    print(f"  Format:  {output_format}")

    try:
        resp = requests.post(
            url,
            headers={
                "Api-Key": api_key,
                "Content-Type": "application/json",
            },
            json=body,
            timeout=120,
        )
        resp.raise_for_status()
        result = resp.json()
    except requests.exceptions.Timeout:
        print("ERROR: Request timed out (120s). Try smaller size or lower quality.")
        return []
    except requests.exceptions.HTTPError as e:
        error_body = e.response.json() if e.response.content else {}
        print(f"ERROR: HTTP {e.response.status_code}")
        print(f"  {json.dumps(error_body, indent=2, ensure_ascii=False)}")
        return []

    if "error" in result:
        print(f"ERROR: {result['error'].get('message', result['error'])}")
        return []

    # Save images
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    saved_paths = []
    for idx, item in enumerate(result.get("data", [])):
        b64_data = item.get("b64_json", "")
        if not b64_data:
            print(f"  WARNING: Image {idx+1} has no data, skipping")
            continue

        img_bytes = base64.b64decode(b64_data)

        if n == 1:
            path = output_path
        else:
            stem = output_path.stem
            suffix = output_path.suffix
            path = output_path.parent / f"{stem}_{idx+1}{suffix}"

        with open(path, "wb") as f:
            f.write(img_bytes)

        size_kb = len(img_bytes) / 1024
        saved_paths.append(str(path))
        print(f"  Saved: {path} ({size_kb:.0f} KB)")

    return saved_paths


def edit_image(
    prompt,
    source_image_path,
    output_path,
    mask_path=None,
    size=DEFAULT_SIZE,
    quality=DEFAULT_QUALITY,
):
    """
    Edit an existing image using GPT-image-2 inpainting.

    Args:
        prompt: Description of the desired edit
        source_image_path: Path to the source image
        output_path: File path to save the edited image
        mask_path: Optional mask image (white = edit area, black = keep)
        size: Output dimensions
        quality: "low", "medium", or "high"

    Returns:
        Saved file path or None
    """
    endpoint, api_key, deployment = get_config()
    size = resolve_size(size)

    url = f"{endpoint}openai/deployments/{deployment}/images/edits?api-version={DEFAULT_API_VERSION}"

    print(f"Editing image: {source_image_path}")
    print(f"  Prompt: {prompt[:80]}{'...' if len(prompt) > 80 else ''}")

    files = {
        "image": (
            Path(source_image_path).name,
            open(source_image_path, "rb"),
            "image/png",
        ),
    }
    if mask_path:
        files["mask"] = (
            Path(mask_path).name,
            open(mask_path, "rb"),
            "image/png",
        )

    data = {
        "prompt": prompt,
        "n": 1,
        "size": size,
        "quality": quality,
    }

    try:
        resp = requests.post(
            url,
            headers={"Api-Key": api_key},
            data=data,
            files=files,
            timeout=120,
        )
        resp.raise_for_status()
        result = resp.json()
    except (requests.exceptions.Timeout, requests.exceptions.HTTPError) as e:
        print(f"ERROR: {e}")
        return None
    finally:
        for f_tuple in files.values():
            f_tuple[1].close()

    if "error" in result:
        print(f"ERROR: {result['error'].get('message', result['error'])}")
        return None

    b64_data = result["data"][0].get("b64_json", "")
    if not b64_data:
        print("ERROR: No image data in response")
        return None

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img_bytes = base64.b64decode(b64_data)
    with open(output_path, "wb") as f:
        f.write(img_bytes)

    print(f"  Saved: {output_path} ({len(img_bytes)/1024:.0f} KB)")
    return str(output_path)


def show_config():
    """Show current configuration and where each value comes from."""
    print("=== GPT-image-2 Configuration ===\n")
    print(f"Config file: {CONFIG_PATH}")

    file_cfg = _load_config_file()
    env_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
    env_key = os.environ.get("AZURE_OPENAI_API_KEY", "")
    env_deploy = os.environ.get("GPT_IMAGE_DEPLOYMENT", "")

    # Show each value and its source
    endpoint = file_cfg.get("azure_openai_endpoint") or env_endpoint
    key = file_cfg.get("azure_openai_api_key") or env_key
    deploy = file_cfg.get("deployment_name") or env_deploy or DEFAULT_DEPLOYMENT

    def source(file_val, env_val, name):
        if file_val:
            return "config.json"
        elif env_val:
            return f"env ${name}"
        else:
            return "NOT SET"

    print(f"\n  Endpoint:   {endpoint or '(empty)'}")
    print(f"    Source:   {source(file_cfg.get('azure_openai_endpoint'), env_endpoint, 'AZURE_OPENAI_ENDPOINT')}")
    print(f"\n  API Key:    {'***' + key[-4:] if key else '(empty)'}")
    print(f"    Source:   {source(file_cfg.get('azure_openai_api_key'), env_key, 'AZURE_OPENAI_API_KEY')}")
    print(f"\n  Deployment: {deploy}")
    print(f"    Source:   {source(file_cfg.get('deployment_name'), env_deploy, 'GPT_IMAGE_DEPLOYMENT')}")

    if not endpoint or not key:
        print(f"\n--- To configure, edit: {CONFIG_PATH} ---")
        print(json.dumps({
            "azure_openai_endpoint": "https://your-resource.openai.azure.com/",
            "azure_openai_api_key": "your-api-key",
            "deployment_name": "gpt-image-2",
            "api_version": "2025-04-01-preview"
        }, indent=2))


def verify_setup():
    """Check that all prerequisites are met."""
    print("=== GPT-image-2 Setup Verification ===\n")

    # Show config source
    file_cfg = _load_config_file()
    has_file_config = bool(file_cfg.get("azure_openai_endpoint") and file_cfg.get("azure_openai_api_key"))
    print(f"Config file:  {CONFIG_PATH}")
    print(f"  Status:     {'Configured' if has_file_config else 'Empty or missing — using env vars'}\n")

    try:
        endpoint, api_key, deployment = get_config()
    except EnvironmentError as e:
        print(f"ERROR: {e}")
        return False

    print(f"Endpoint:     {endpoint}")
    print(f"API Key:      ***{api_key[-4:]}")
    print(f"Deployment:   {deployment}")

    # Check Python dependencies
    print("\nDependencies:")
    deps_ok = True
    for dep in ["requests", "PIL"]:
        try:
            __import__(dep)
            print(f"  {dep}: OK")
        except ImportError:
            print(f"  {dep}: MISSING — pip install {'pillow' if dep == 'PIL' else dep}")
            deps_ok = False

    if not deps_ok:
        print("\nInstall missing dependencies: pip install requests pillow")
        return False

    # Test API connectivity
    print("\nTesting API connectivity...")
    test_url = f"{endpoint}openai/deployments/{deployment}/images/generations?api-version={DEFAULT_API_VERSION}"
    try:
        resp = requests.post(
            test_url,
            headers={"Api-Key": api_key, "Content-Type": "application/json"},
            json={"prompt": "test", "n": 1, "size": "1024x1024", "quality": "low"},
            timeout=30,
        )
        if resp.status_code == 200:
            print("  API: Connected and working!")
            return True
        elif resp.status_code == 401:
            print("  API: Authentication failed — check your API key")
        elif resp.status_code == 404:
            print(f"  API: Deployment '{deployment}' not found")
            print(f"  → Deploy gpt-image-2 in Azure AI Foundry Portal, then update deployment_name in:")
            print(f"    {CONFIG_PATH}")
        else:
            print(f"  API: Unexpected status {resp.status_code}")
            print(f"  {resp.text[:200]}")
    except requests.exceptions.ConnectionError:
        print(f"  API: Cannot connect to {endpoint}")
    except requests.exceptions.Timeout:
        print("  API: Connection timed out")

    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate images using Azure OpenAI GPT-image-2")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate a new image")
    gen_parser.add_argument("--prompt", required=True, help="Image description prompt")
    gen_parser.add_argument("--output", required=True, help="Output file path")
    gen_parser.add_argument("--size", default=DEFAULT_SIZE, help=f"Image size (default: {DEFAULT_SIZE})")
    gen_parser.add_argument("--quality", default=DEFAULT_QUALITY, choices=["low", "medium", "high"])
    gen_parser.add_argument("--format", default=DEFAULT_FORMAT, choices=["png", "jpeg", "webp"])
    gen_parser.add_argument("--background", default="auto", choices=["auto", "transparent"])
    gen_parser.add_argument("--n", type=int, default=1, help="Number of images (1-10)")

    # Edit command
    edit_parser = subparsers.add_parser("edit", help="Edit an existing image")
    edit_parser.add_argument("--prompt", required=True, help="Edit description")
    edit_parser.add_argument("--source", required=True, help="Source image path")
    edit_parser.add_argument("--output", required=True, help="Output file path")
    edit_parser.add_argument("--mask", help="Optional mask image path")
    edit_parser.add_argument("--size", default=DEFAULT_SIZE)
    edit_parser.add_argument("--quality", default=DEFAULT_QUALITY, choices=["low", "medium", "high"])

    # Config command
    subparsers.add_parser("config", help="Show current configuration and sources")

    # Verify command
    subparsers.add_parser("verify", help="Verify setup and prerequisites")

    # List presets
    subparsers.add_parser("presets", help="List available size presets")

    args = parser.parse_args()

    if args.command == "generate":
        paths = generate_image(
            prompt=args.prompt,
            output_path=args.output,
            size=args.size,
            quality=args.quality,
            output_format=args.format,
            background=args.background,
            n=args.n,
        )
        if not paths:
            sys.exit(1)

    elif args.command == "edit":
        result = edit_image(
            prompt=args.prompt,
            source_image_path=args.source,
            output_path=args.output,
            mask_path=args.mask,
            size=args.size,
            quality=args.quality,
        )
        if not result:
            sys.exit(1)

    elif args.command == "config":
        show_config()

    elif args.command == "verify":
        ok = verify_setup()
        sys.exit(0 if ok else 1)

    elif args.command == "presets":
        print("Available size presets:")
        for name, size in SIZE_PRESETS.items():
            print(f"  {name:15s}  {size}")

    else:
        parser.print_help()
