from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path('api/', include('regions.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
