from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include('tests.urls')),
    path('admin/', admin.site.urls),
    path('auth', include('tests.urls')),
]
