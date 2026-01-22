"""MiniMax endpoint mappings."""

MAPPINGS = {
    r'^/proxy/minimax/video_generation$': {
        'provider': 'minimax',
        'url_template': 'https://api.minimax.chat/v1/video_generation',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/minimax/query/video_generation$': {
        'provider': 'minimax',
        'url_template': 'https://api.minimax.chat/v1/query/video_generation',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/minimax/files/retrieve$': {
        'provider': 'minimax',
        'url_template': 'https://api.minimax.chat/v1/files/retrieve',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
}
