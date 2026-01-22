"""Stability AI endpoint mappings."""

MAPPINGS = {
    # SD3 image generation
    r'^/proxy/stability/v2beta/stable-image/generate/sd3$': {
        'provider': 'stability',
        'url_template': 'https://api.stability.ai/v2beta/stable-image/generate/sd3',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    # Ultra image generation
    r'^/proxy/stability/v2beta/stable-image/generate/ultra$': {
        'provider': 'stability',
        'url_template': 'https://api.stability.ai/v2beta/stable-image/generate/ultra',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    # Upscale endpoints
    r'^/proxy/stability/v2beta/stable-image/upscale/conservative$': {
        'provider': 'stability',
        'url_template': 'https://api.stability.ai/v2beta/stable-image/upscale/conservative',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/stability/v2beta/stable-image/upscale/creative$': {
        'provider': 'stability',
        'url_template': 'https://api.stability.ai/v2beta/stable-image/upscale/creative',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/stability/v2beta/stable-image/upscale/fast$': {
        'provider': 'stability',
        'url_template': 'https://api.stability.ai/v2beta/stable-image/upscale/fast',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    # Audio endpoints
    r'^/proxy/stability/v2beta/audio/stable-audio-2/text-to-audio$': {
        'provider': 'stability',
        'url_template': 'https://api.stability.ai/v2beta/audio/stable-audio-2/text-to-audio',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/stability/v2beta/audio/stable-audio-2/audio-to-audio$': {
        'provider': 'stability',
        'url_template': 'https://api.stability.ai/v2beta/audio/stable-audio-2/audio-to-audio',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/stability/v2beta/audio/stable-audio-2/inpaint$': {
        'provider': 'stability',
        'url_template': 'https://api.stability.ai/v2beta/audio/stable-audio-2/inpaint',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    # Results polling
    r'^/proxy/stability/v2beta/results/(.+)$': {
        'provider': 'stability',
        'url_template': 'https://api.stability.ai/v2beta/results/{0}',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
}
