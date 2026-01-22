"""Moonvalley endpoint mappings."""

MAPPINGS = {
    r'^/proxy/moonvalley/uploads$': {
        'provider': 'moonvalley',
        'url_template': 'https://api.moonvalley.ai/v1/uploads',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/moonvalley/prompts$': {
        'provider': 'moonvalley',
        'url_template': 'https://api.moonvalley.ai/v1/prompts',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/moonvalley/prompts/([^/]+)$': {
        'provider': 'moonvalley',
        'url_template': 'https://api.moonvalley.ai/v1/prompts/{0}',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/moonvalley/prompts/text-to-video$': {
        'provider': 'moonvalley',
        'url_template': 'https://api.moonvalley.ai/v1/prompts/text-to-video',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/moonvalley/prompts/image-to-video$': {
        'provider': 'moonvalley',
        'url_template': 'https://api.moonvalley.ai/v1/prompts/image-to-video',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/moonvalley/prompts/video-to-video$': {
        'provider': 'moonvalley',
        'url_template': 'https://api.moonvalley.ai/v1/prompts/video-to-video',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
}
