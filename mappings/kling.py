"""Kling AI endpoint mappings."""

# Note: Kling uses versioned endpoints like {KLING_API_VERSION}
# We'll match the common patterns

MAPPINGS = {
    # Image generation
    r'^/proxy/kling/v\d+/images/generations$': {
        'provider': 'kling',
        'url_template': 'https://api.klingai.com/v1/images/generations',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/kling/v\d+/images/kolors-virtual-try-on$': {
        'provider': 'kling',
        'url_template': 'https://api.klingai.com/v1/images/kolors-virtual-try-on',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/kling/v1/images/omni-image$': {
        'provider': 'kling',
        'url_template': 'https://api.klingai.com/v1/images/omni-image',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/kling/v1/images/omni-image/([^/]+)$': {
        'provider': 'kling',
        'url_template': 'https://api.klingai.com/v1/images/omni-image/{0}',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    # Video generation
    r'^/proxy/kling/v\d+/videos/text2video$': {
        'provider': 'kling',
        'url_template': 'https://api.klingai.com/v1/videos/text2video',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/kling/v\d+/videos/image2video$': {
        'provider': 'kling',
        'url_template': 'https://api.klingai.com/v1/videos/image2video',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/kling/v\d+/videos/video-extend$': {
        'provider': 'kling',
        'url_template': 'https://api.klingai.com/v1/videos/video-extend',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/kling/v\d+/videos/effects$': {
        'provider': 'kling',
        'url_template': 'https://api.klingai.com/v1/videos/effects',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/kling/v\d+/videos/lip-sync$': {
        'provider': 'kling',
        'url_template': 'https://api.klingai.com/v1/videos/lip-sync',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/kling/v1/videos/omni-video$': {
        'provider': 'kling',
        'url_template': 'https://api.klingai.com/v1/videos/omni-video',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/kling/v1/videos/omni-video/([^/]+)$': {
        'provider': 'kling',
        'url_template': 'https://api.klingai.com/v1/videos/omni-video/{0}',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
}
