from django.contrib import admin
from django.urls import path, include
from journal.views import RateLimitedPasswordResetView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Custom password reset with rate limiting (must be before allauth urls)
    path('accounts/password/reset/', RateLimitedPasswordResetView.as_view(), name='account_reset_password'),
    path('accounts/', include('allauth.urls')), # Google Login
    path('', include('journal.urls')), # Main App
]
