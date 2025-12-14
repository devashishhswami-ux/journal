from django.contrib import admin
from django.urls import path, include
from journal.views import RateLimitedPasswordResetView
from journal.admin import admin_site  # Import custom admin site

urlpatterns = [
    path('admin/', admin_site.urls),  # Use custom admin site
    # Custom password reset with rate limiting (must be before allauth urls)
    path('accounts/password/reset/', RateLimitedPasswordResetView.as_view(), name='account_reset_password'),
    path('accounts/', include('allauth.urls')), # Google Login
    path('', include('journal.urls')), # Main App
]

