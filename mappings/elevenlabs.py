"""ElevenLabs endpoint mappings.

This mirrors the current core ComfyUI ElevenLabs proxy surface so liberation
can route those nodes directly with vendor auth instead of falling back to the
Comfy proxy.
"""

MAPPINGS = {
    r"^/proxy/elevenlabs/v1/speech-to-text$": {
        "provider": "elevenlabs",
        "url_template": "https://api.elevenlabs.io/v1/speech-to-text",
        "auth_fn": lambda key: {"xi-api-key": key},
        "request_transform": None,
        "response_transform": None,
    },
    r"^/proxy/elevenlabs/v1/text-to-speech/([^/]+)$": {
        "provider": "elevenlabs",
        "url_template": "https://api.elevenlabs.io/v1/text-to-speech/{0}",
        "auth_fn": lambda key: {"xi-api-key": key},
        "request_transform": None,
        "response_transform": None,
    },
    r"^/proxy/elevenlabs/v1/audio-isolation$": {
        "provider": "elevenlabs",
        "url_template": "https://api.elevenlabs.io/v1/audio-isolation",
        "auth_fn": lambda key: {"xi-api-key": key},
        "request_transform": None,
        "response_transform": None,
    },
    r"^/proxy/elevenlabs/v1/sound-generation$": {
        "provider": "elevenlabs",
        "url_template": "https://api.elevenlabs.io/v1/sound-generation",
        "auth_fn": lambda key: {"xi-api-key": key},
        "request_transform": None,
        "response_transform": None,
    },
    r"^/proxy/elevenlabs/v1/voices/add$": {
        "provider": "elevenlabs",
        "url_template": "https://api.elevenlabs.io/v1/voices/add",
        "auth_fn": lambda key: {"xi-api-key": key},
        "request_transform": None,
        "response_transform": None,
    },
    r"^/proxy/elevenlabs/v1/speech-to-speech/([^/]+)$": {
        "provider": "elevenlabs",
        "url_template": "https://api.elevenlabs.io/v1/speech-to-speech/{0}",
        "auth_fn": lambda key: {"xi-api-key": key},
        "request_transform": None,
        "response_transform": None,
    },
    r"^/proxy/elevenlabs/v1/text-to-dialogue$": {
        "provider": "elevenlabs",
        "url_template": "https://api.elevenlabs.io/v1/text-to-dialogue",
        "auth_fn": lambda key: {"xi-api-key": key},
        "request_transform": None,
        "response_transform": None,
    },
}
