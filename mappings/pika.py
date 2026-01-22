"""Pika endpoint mappings."""

# Pika uses versioned endpoints like {PIKA_API_VERSION}

MAPPINGS = {
    r'^/proxy/pika/generate/v\d+/t2v$': {
        'provider': 'pika',
        'url_template': 'https://api.pika.art/v1/generate/t2v',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/pika/generate/v\d+/i2v$': {
        'provider': 'pika',
        'url_template': 'https://api.pika.art/v1/generate/i2v',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/pika/generate/v\d+/pikaframes$': {
        'provider': 'pika',
        'url_template': 'https://api.pika.art/v1/generate/pikaframes',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/pika/generate/v\d+/pikascenes$': {
        'provider': 'pika',
        'url_template': 'https://api.pika.art/v1/generate/pikascenes',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/pika/generate/pikadditions$': {
        'provider': 'pika',
        'url_template': 'https://api.pika.art/v1/generate/pikadditions',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/pika/generate/pikaffects$': {
        'provider': 'pika',
        'url_template': 'https://api.pika.art/v1/generate/pikaffects',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/pika/generate/pikaswaps$': {
        'provider': 'pika',
        'url_template': 'https://api.pika.art/v1/generate/pikaswaps',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/pika/videos$': {
        'provider': 'pika',
        'url_template': 'https://api.pika.art/v1/videos',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/pika/videos/([^/]+)$': {
        'provider': 'pika',
        'url_template': 'https://api.pika.art/v1/videos/{0}',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
}
