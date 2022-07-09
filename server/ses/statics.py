
constant_routes = [
    {
        'path': '/redirect',
        'component': 'layout/Layout',
        'hidden': True,
        'children': [
            {
                'path': '/redirect/:path*',
                'component': 'views/redirect/index'
            }
        ]
    },
    {
        'path': '/login',
        'component': 'views/login/index',
        'hidden': True
    },
    {
        'path': '/auth-redirect',
        'component': 'views/login/auth-redirect',
        'hidden': True
    },
    {
        'path': '/404',
        'component': 'views/error-page/404',
        'hidden': True
    },
    {
        'path': '/401',
        'component': 'views/error-page/401',
        'hidden': True
    },
    {
        'path': '',
        'component': 'layout/Layout',
        'redirect': 'dashboard',
        'children': [
            {
                'path': 'dashboard',
                'component': 'views/dashboard/index',
                'name': 'Dashboard',
                'meta': {'title': 'Dashboard', 'icon': 'dashboard', 'affix': True}
            }
        ]
    },
]
