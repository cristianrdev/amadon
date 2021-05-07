from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('checkout', views.checkout),
    path('refresh_checkout', views.refresh_checkout)
]
