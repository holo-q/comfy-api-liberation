"""
Auto-discovery of proxy endpoints in ComfyUI.
Scans comfy_api_nodes/*.py for /proxy/* patterns to detect unmapped endpoints.
"""
import re
import logging
from pathlib import Path

log = logging.getLogger("comfy-api-liberation")


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
        for pattern in patterns:
            # Handle paths with template variables like {model}
            # Normalize {var} to .+ for matching
            normalized_path = re.sub(r'\{[^}]+\}', '[^/]+', proxy_path)
            try:
                if re.match(pattern, proxy_path) or re.match(pattern, normalized_path):
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
