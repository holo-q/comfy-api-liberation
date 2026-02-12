"""xAI / Grok endpoint mappings.

Covers image generation, image editing, video generation,
video status polling, and video editing via the xAI API.

Source proxy paths extracted from:
  comfy_api_nodes/nodes_grok.py (GrokImageNode, GrokImageEditNode,
  GrokVideoNode, GrokVideoEditNode)
"""

MAPPINGS = {
    # Image generation (grok-imagine-image-beta)
    r'^/proxy/xai/v1/images/generations$': {
        'provider': 'grok',
        'url_template': 'https://api.x.ai/v1/images/generations',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    # Image editing (grok-imagine-image-beta)
    r'^/proxy/xai/v1/images/edits$': {
        'provider': 'grok',
        'url_template': 'https://api.x.ai/v1/images/edits',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    # Video generation (grok-imagine-video-beta)
    r'^/proxy/xai/v1/videos/generations$': {
        'provider': 'grok',
        'url_template': 'https://api.x.ai/v1/videos/generations',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    # Video editing (grok-imagine-video-beta)
    # NOTE: must precede the catch-all ([^/]+) pattern below, otherwise
    # /videos/edits would be swallowed by the status-polling regex.
    r'^/proxy/xai/v1/videos/edits$': {
        'provider': 'grok',
        'url_template': 'https://api.x.ai/v1/videos/edits',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    # Video status polling — poll_op hits /proxy/xai/v1/videos/{request_id}
    r'^/proxy/xai/v1/videos/([^/]+)$': {
        'provider': 'grok',
        'url_template': 'https://api.x.ai/v1/videos/{0}',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
}
