from django.urls import include, path
from django.conf import settings


urlpatterns = [
    path('api/', include('regions.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
