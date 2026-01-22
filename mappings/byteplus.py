"""BytePlus (ByteDance) endpoint mappings."""

MAPPINGS = {
    r'^/proxy/byteplus/api/v3/images/generations$': {
        'provider': 'byteplus',
        'url_template': 'https://api.byteplus.com/api/v3/images/generations',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/byteplus/api/v3/contents/generations/tasks$': {
        'provider': 'byteplus',
        'url_template': 'https://api.byteplus.com/api/v3/contents/generations/tasks',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/byteplus/api/v3/contents/generations/tasks/([^/]+)$': {
        'provider': 'byteplus',
        'url_template': 'https://api.byteplus.com/api/v3/contents/generations/tasks/{0}',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
}
