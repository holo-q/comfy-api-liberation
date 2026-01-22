"""
ComfyUI nodes for API key management.
"""


class APIKeyManager:
    """
    Node to manage API keys within ComfyUI.
    Keys are stored securely in config, NOT in the workflow file.
    """

    @classmethod
    def INPUT_TYPES(cls):
        from .config import PROVIDERS
        providers = sorted(PROVIDERS)

        return {
            "required": {
                "provider": (providers, {"default": "google"}),
                "action": (["check", "set", "clear"], {"default": "check"}),
            },
            "optional": {
                "api_key": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Enter API key (not saved in workflow)"
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status",)
    FUNCTION = "manage_key"
    CATEGORY = "api-liberation"
    OUTPUT_NODE = True

    def manage_key(self, provider: str, action: str, api_key: str = ""):
        from .config import set_api_key, get_api_key, delete_api_key

        if action == "set":
            if not api_key:
                return ("⚠ No key provided",)
            set_api_key(provider, api_key)
            return (f"✓ {provider} key saved",)

        elif action == "check":
            has_key = bool(get_api_key(provider))
            status = "✓ configured" if has_key else "✗ not set"
            return (f"{provider}: {status}",)

        elif action == "clear":
            delete_api_key(provider)
            return (f"✓ {provider} key cleared",)

        return ("Unknown action",)


class APIKeyStatus:
    """
    Node to check status of all API keys at once.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {}}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status_report",)
    FUNCTION = "get_status"
    CATEGORY = "api-liberation"

    def get_status(self):
        from .config import get_all_key_status

        status = get_all_key_status()
        lines = ["=== API Key Status ==="]

        configured = []
        missing = []

        for provider, info in sorted(status.items()):
            if info["configured"]:
                source = info.get("source") or "config-file"
                configured.append(f"  ✓ {provider} ({source})")
            else:
                missing.append(f"  ✗ {provider}")

        if configured:
            lines.append("\nConfigured:")
            lines.extend(configured)

        if missing:
            lines.append("\nNot configured:")
            lines.extend(missing)

        return ("\n".join(lines),)


class LiberationStatus:
    """
    Node to check liberation extension status.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {}}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status",)
    FUNCTION = "get_status"
    CATEGORY = "api-liberation"

    def get_status(self):
        from .patches import is_patched
        from .discovery import detect_unmapped_endpoints
        from .mappings import ENDPOINT_MAP

        unmapped = detect_unmapped_endpoints(ENDPOINT_MAP)

        lines = [
            "=== Liberation Status ===",
            f"Patches: {'✓ Active' if is_patched() else '✗ Inactive'}",
            f"Mapped providers: {len(ENDPOINT_MAP)}",
            f"Unmapped endpoints: {len(unmapped)}",
        ]

        if unmapped:
            lines.append("\nUnmapped (using Comfy proxy):")
            for ep in sorted(list(unmapped)[:10]):  # Show first 10
                lines.append(f"  - {ep}")
            if len(unmapped) > 10:
                lines.append(f"  ... and {len(unmapped) - 10} more")

        return ("\n".join(lines),)


# Node registration
NODE_CLASS_MAPPINGS = {
    "APIKeyManager": APIKeyManager,
    "APIKeyStatus": APIKeyStatus,
    "LiberationStatus": LiberationStatus,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "APIKeyManager": "🔑 API Key Manager",
    "APIKeyStatus": "📋 API Key Status",
    "LiberationStatus": "🔓 Liberation Status",
}
