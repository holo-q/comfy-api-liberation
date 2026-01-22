"""Luma AI endpoint mappings."""

MAPPINGS = {
    r'^/proxy/luma/generations$': {
        'provider': 'luma',
        'url_template': 'https://api.lumalabs.ai/dream-machine/v1/generations',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/luma/generations/image$': {
        'provider': 'luma',
        'url_template': 'https://api.lumalabs.ai/dream-machine/v1/generations/image',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/luma/generations/([^/]+)$': {
        'provider': 'luma',
        'url_template': 'https://api.lumalabs.ai/dream-machine/v1/generations/{0}',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
}
