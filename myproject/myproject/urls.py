from django.contrib import admin
from django.urls import path, include
from .swagger_auth import schema_view


urlpatterns = [
    path('', include('dentistry.urls')),
    path('admin/', admin.site.urls),
    path('',
        include([
            path('swagger/', schema_view.with_ui('swagger', cache_timeout=0))
        ])
    ),
]
