from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('api/query/', views.api_query, name='api_query'),
    path('api/whatif/', views.api_whatif, name='api_whatif'),
    path('api/correlation-summary/', views.api_correlation_summary, name='api_correlation_summary'),
]