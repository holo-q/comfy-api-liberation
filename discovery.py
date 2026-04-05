"""
Auto-discovery of proxy endpoints in ComfyUI.
Scans comfy_api_nodes/*.py for /proxy/* patterns to detect unmapped endpoints.
"""
import re
import logging
from pathlib import Path

log = logging.getLogger("comfy-api-liberation")


def _normalize_proxy_path_for_matching(proxy_path: str) -> str:
    """
    Normalize symbolic placeholders in extracted proxy paths.

    Generic placeholders still collapse to a single path segment, but version
    placeholders such as `{KLING_API_VERSION}` are rewritten to concrete
    version-like values so regexes like `v\\d+` can match during coverage checks.
    """
    def repl(match: re.Match[str]) -> str:
        name = match.group(1)
        if "VERSION" in name.upper():
            return "v1"
        return "[^/]+"

    return re.sub(r"\{([^}]+)\}", repl, proxy_path)


def scan_proxy_endpoints() -> set[str]:
    """
    Scan comfy_api_nodes/*.py for /proxy/* string literals.
    Returns set of all proxy paths found.
    """
    proxy_paths = set()

    try:
        import comfy_api_nodes
        nodes_dir = Path(comfy_api_nodes.__file__).parent

        for py_file in nodes_dir.glob("nodes_*.py"):
            try:
                content = py_file.read_text()
                # Extract all "/proxy/..." string literals
                matches = re.findall(r'"/proxy/[^"]+', content)
                for match in matches:
                    # Clean up the path (remove quotes, normalize)
                    path = match.strip('"')
                    # Normalize dynamic parts like {model} to wildcards for comparison
                    proxy_paths.add(path)
            except Exception as e:
                log.debug(f"Failed to scan {py_file}: {e}")

    except ImportError:
        log.warning("comfy_api_nodes not found - cannot scan for proxy endpoints")

    return proxy_paths


def detect_unmapped_endpoints(endpoint_map: dict) -> set[str]:
    """
    Find proxy endpoints that don't have mappings in our registry.

    Args:
        endpoint_map: Dict of regex pattern → mapping info

    Returns:
        Set of proxy paths that aren't covered by any mapping pattern
    """
    all_proxies = scan_proxy_endpoints()
    patterns = list(endpoint_map.keys())

    unmapped = set()
    for proxy_path in all_proxies:
        # Check if any pattern matches this proxy path
        matched = False
        normalized_path = _normalize_proxy_path_for_matching(proxy_path)
        for pattern in patterns:
            try:
                if re.match(pattern, proxy_path) or re.match(pattern, normalized_path):
                    matched = True
                    break
                # Some node files expose base prefix constants such as
                # "/proxy/vertexai/gemini" while requests always append a model
                # segment at runtime. Treat those base prefixes as covered when a
                # registered regex maps a more specific child path.
                prefix_pattern = "^" + re.escape(proxy_path.rstrip("/")) + "/"
                if pattern.startswith(prefix_pattern):
                    matched = True
                    break
            except re.error:
                continue

        if not matched:
            unmapped.add(proxy_path)

    return unmapped


def get_proxy_coverage_report(endpoint_map: dict) -> str:
    """Generate a human-readable coverage report."""
    all_proxies = scan_proxy_endpoints()
    unmapped = detect_unmapped_endpoints(endpoint_map)
    mapped = all_proxies - unmapped

    lines = [
        "=== API Liberation Coverage Report ===",
        f"Total proxy endpoints found: {len(all_proxies)}",
        f"Mapped (direct routing): {len(mapped)}",
        f"Unmapped (using Comfy proxy): {len(unmapped)}",
        "",
    ]

    if unmapped:
        lines.append("Unmapped endpoints:")
        for ep in sorted(unmapped):
            lines.append(f"  - {ep}")

    return "\n".join(lines)
