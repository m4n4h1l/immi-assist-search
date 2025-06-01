# in clients/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # The root URL will now point to a new public_homepage view
    path('', views.public_homepage, name='public_homepage'),

    # The secure client list will be at /dashboard/
    path('dashboard/', views.dashboard, name='dashboard'),

    # The other URLs remain the same
    path('add-notice/', views.add_notice, name='add_notice'),
    path('client/<int:client_id>/', views.client_detail, name='client_detail'),
]