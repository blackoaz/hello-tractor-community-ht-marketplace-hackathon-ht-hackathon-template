from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'', 'main.urls', name='root'),
    host(r'main', 'main.urls', name='main'),
    host(r'sellers', 'sellers.urls', name='sellers'),
    host(r'admin', 'admin_panel.urls', name='admin'),
)
