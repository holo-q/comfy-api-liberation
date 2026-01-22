"""Runway endpoint mappings."""

MAPPINGS = {
    r'^/proxy/runway/image_to_video$': {
        'provider': 'runway',
        'url_template': 'https://api.dev.runwayml.com/v1/image_to_video',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/runway/text_to_image$': {
        'provider': 'runway',
        'url_template': 'https://api.dev.runwayml.com/v1/text_to_image',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/runway/tasks$': {
        'provider': 'runway',
        'url_template': 'https://api.dev.runwayml.com/v1/tasks',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/runway/tasks/([^/]+)$': {
        'provider': 'runway',
        'url_template': 'https://api.dev.runwayml.com/v1/tasks/{0}',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
}
