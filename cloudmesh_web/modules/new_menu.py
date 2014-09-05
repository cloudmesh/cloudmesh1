super_duper_sidebar_pages = [
    ["Cloudmesh", None, None, ['all'],
        [
            ["Home", "/", None],
            ["Status", "/status", None],
            ["Profile", "/profile/", None],
    ],
    ],
    ["Clouds", "cm/refresh", "365_restart", ['all'],
        [
            ["Refresh", "/cm/refresh", None],
            ["VMs", "/mesh/servers", None],
            ["Images", "/mesh/images", None],
            ["Flavors", "/mesh/flavors/", None],
    ],
    ],
    ["HPC Queues", None, None, ['all'],
        [
            ["Jobs", "/mesh/qstat", None],
            ["Queues Info", "/mesh/qinfo", None],
            ["Rack Diagram", "/inventory/rack", None],
    ]
    ],

    ["Admin", None, None, ['admin'],
        [
            ["Admin", "/admin", None],
            ["Users - LDAP", "/users/ldap", None],
            ["Users - Cloud", "/mesh/users/", None],
            ["Register - Cloud", "/mesh/register/clouds", None],
    ]
    ],
    ["Admin - Inventory", None, None, ['admin'],
        [
            ["Overview", "/inventory/", None],
            ["Table", "/inventory/summary", None],
            ["Images", "/inventory/images", None],
    ],
    ],
    ["Admin - Provision", None, None, ['admin', 'rain'],
        [
            ["Policy", "/provision/policy", None],
            ["Overview", "/provision/summary/", None],
            ["Form", "/provision/", None],
    ],
    ],
    ["Admin - Launcher", None, None, ['admin', 'rain'],
        [
            ["Launcher", "/cm/launch", None],
            ["Register", "/cm/register", None],
    ]
    ],
]
