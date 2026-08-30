"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Including the dashboard app URLs
    path('', include('dashboard.urls')), 
]