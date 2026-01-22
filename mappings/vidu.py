"""Vidu endpoint mappings."""

MAPPINGS = {
    r'^/proxy/vidu/text2video$': {
        'provider': 'vidu',
        'url_template': 'https://api.vidu.studio/v1/text2video',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/vidu/img2video$': {
        'provider': 'vidu',
        'url_template': 'https://api.vidu.studio/v1/img2video',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/vidu/reference2video$': {
        'provider': 'vidu',
        'url_template': 'https://api.vidu.studio/v1/reference2video',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/vidu/start-end2video$': {
        'provider': 'vidu',
        'url_template': 'https://api.vidu.studio/v1/start-end2video',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/vidu/tasks/([^/]+)/creations$': {
        'provider': 'vidu',
        'url_template': 'https://api.vidu.studio/v1/tasks/{0}/creations',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
}
