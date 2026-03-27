
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('app_quotes.urls')),
    path('app_quotes/', include('app_quotes.urls')),
    path('app_auth/', include('app_auth.urls')),
    path('admin/', admin.site.urls),
]
