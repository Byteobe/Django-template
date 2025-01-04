from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


from main.urls import apiurls as main_api_urls

from users.urls import apiurls as users_api_urls
from authentication.urls import apiurls as authentication_api_urls


api_urls = ([
    path('main/', include(main_api_urls, namespace='main')),
    path("authentication/", include(authentication_api_urls, namespace='authentication')),
    path('users/', include(users_api_urls, namespace='users')),
], 'api')

urlpatterns = [
    path('', include('main.urls')),
    path('api/', include(api_urls, namespace='api')),
    path('admin/', admin.site.urls),
    path('documentation/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('documentation/api/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]


if not settings.IS_PRODUCTION:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
