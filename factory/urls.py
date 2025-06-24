from django.urls import path
from .views import product_upload
from . import views

urlpatterns = [
    path('upload/', product_upload, name='product-upload'),
    path('live/', views.live_manufacturing_display, name='live-manufacturing-display'),
]
