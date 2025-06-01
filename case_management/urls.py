# in case_management/urls.py

from django.contrib import admin
from django.urls import path, include
# 1. Import the built-in LoginView and LogoutView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),

    # 2. Create a specific, dedicated URL for logging in.
    #    We point it to our custom template.
    path('login/', 
        LoginView.as_view(template_name='registration/login.html'), 
        name='login'),

    # 3. Create a specific, dedicated URL for logging out.
    path('logout/', LogoutView.as_view(), name='logout'),

    # 4. We no longer need the 'accounts/' include, so it has been removed.

    # This line remains the same, handling all our app's pages
    path('', include('clients.urls')),
]