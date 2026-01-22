"""Wan (Alibaba DashScope) endpoint mappings."""

MAPPINGS = {
    r'^/proxy/wan/api/v1/services/aigc/text2image/image-synthesis$': {
        'provider': 'wan',
        'url_template': 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/wan/api/v1/services/aigc/image2image/image-synthesis$': {
        'provider': 'wan',
        'url_template': 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/wan/api/v1/services/aigc/video-generation/video-synthesis$': {
        'provider': 'wan',
        'url_template': 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
    r'^/proxy/wan/api/v1/tasks/([^/]+)$': {
        'provider': 'wan',
        'url_template': 'https://dashscope.aliyuncs.com/api/v1/tasks/{0}',
        'auth_fn': lambda key: {'Authorization': f'Bearer {key}'},
        'request_transform': None,
        'response_transform': None,
    },
}
