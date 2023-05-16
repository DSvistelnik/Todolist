from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include(('core.urls', 'core'))),
    path('goals/', include(('goals.urls', 'goals'))),
    path("oauth/", include("social_django.urls", namespace="social")),
    path('bot/', include(('bot.urls', 'bot'), namespace='bot')),
]

if settings.DEBUG:
    urlpatterns += [
        path('api-auth/', include('rest_framework.urls'))
    ]
