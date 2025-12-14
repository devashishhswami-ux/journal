from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from .models import Entry, SiteConfiguration


class SocialAccountInline(admin.TabularInline):
    """Inline display of social accounts for users"""
    model = SocialAccount
    extra = 0
    readonly_fields = ('provider', 'uid', 'get_profile_link', 'date_joined')
    fields = ('provider', 'uid', 'get_profile_link', 'date_joined')
    can_delete = False
    
    def get_profile_link(self, obj):
        """Link to view full social account details"""
        if obj.pk:
            url = reverse('admin:socialaccount_socialaccount_change', args=[obj.pk])
            return format_html('<a href="{}">View Details</a>', url)
        return '-'
    get_profile_link.short_description = 'Profile Details'


class CustomUserAdmin(BaseUserAdmin):
    """Enhanced User admin showing email, social accounts, and journal info"""
    list_display = ('email', 'get_social_accounts', 'entry_count', 'date_joined', 'is_active')
    list_filter = ('is_active', 'date_joined', 'socialaccount__provider')
    search_fields = ('email', 'username', 'socialaccount__uid')
    ordering = ('-date_joined',)
    inlines = [SocialAccountInline]
    
    def entry_count(self, obj):
        """Display number of journal entries"""
        return obj.entries.count()
    entry_count.short_description = "Journals"
    
    def get_social_accounts(self, obj):
        """Display linked social accounts with icons"""
        accounts = obj.socialaccount_set.all()
        if not accounts:
            return format_html('<span style="color: #999;">Email/Password</span>')
        
        icons = {
            'google': '🔵',
            'facebook': '🔷',
            'github': '⚫',
            'twitter': '🐦',
        }
        
        html_parts = []
        for account in accounts:
            icon = icons.get(account.provider, '🔗')
            html_parts.append(f'{icon} {account.provider.title()}')
        
        return format_html(' | '.join(html_parts))
    get_social_accounts.short_description = "Login Method"


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    """Simplified Entry admin with essential info"""
    list_display = ('title', 'user_email', 'created_at', 'ip_address')
    list_filter = ('created_at',)
    search_fields = ('title', 'content', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'ip_address')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Entry Information', {
            'fields': ('user', 'title', 'content')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'ip_address', 'duration_str')
        }),
    )
    
    def user_email(self, obj):
        """Display user's email"""
        return obj.user.email if obj.user else '-'
    user_email.short_description = "User Email"


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    """Simple site configuration admin"""
    list_display = ('site_name', 'maintenance_mode', 'allow_registration')
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteConfiguration.objects.exists()


# Unregister the default User admin and register custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Customize admin site header
admin.site.site_header = "Journal Pro Admin"
admin.site.site_title = "Journal Admin"
admin.site.index_title = "Welcome to Journal Pro Administration"


# Custom SocialAccount Admin configuration
class CustomSocialAccountAdmin(admin.ModelAdmin):
    """Detailed social account information admin"""
    list_display = ('user_email', 'provider', 'uid', 'get_profile_picture', 'date_joined')
    list_filter = ('provider', 'date_joined')
    search_fields = ('user__email', 'uid', 'extra_data')
    readonly_fields = (
        'user', 'provider', 'uid', 'date_joined', 'last_login',
        'get_profile_picture', 'get_email', 'get_name', 'get_locale',
        'get_country', 'get_all_data'
    )
    ordering = ('-date_joined',)
    
    fieldsets = (
        ('Account Information', {
            'fields': ('user', 'provider', 'uid', 'date_joined', 'last_login')
        }),
        ('Profile Information', {
            'fields': ('get_profile_picture', 'get_name', 'get_email', 'get_locale', 'get_country'),
            'description': 'Information obtained from the social provider'
        }),
        ('Raw Data', {
            'fields': ('get_all_data',),
            'classes': ('collapse',),
            'description': 'Complete JSON data from provider'
        }),
    )
    
    def user_email(self, obj):
        """Display user's email"""
        return obj.user.email if obj.user else '-'
    user_email.short_description = "User Email"
    
    def get_profile_picture(self, obj):
        """Display profile picture from Google"""
        data = obj.extra_data or {}
        picture_url = data.get('picture', '')
        if picture_url:
            return format_html('<img src="{}" style="width: 60px; height: 60px; border-radius: 50%; border: 2px solid #4285f4;" />', picture_url)
        return '-'
    get_profile_picture.short_description = "Profile Picture"
    
    def get_email(self, obj):
        """Get email from extra data"""
        data = obj.extra_data or {}
        email = data.get('email', '-')
        verified = data.get('verified_email', False)
        if verified:
            return format_html('<span style="color: green;">✓ {}</span>', email)
        return email
    get_email.short_description = "Email (from provider)"
    
    def get_name(self, obj):
        """Get full name from extra data"""
        data = obj.extra_data or {}
        name = data.get('name', data.get('given_name', '-'))
        return name
    get_name.short_description = "Full Name"
    
    def get_locale(self, obj):
        """Get locale/language preference"""
        data = obj.extra_data or {}
        return data.get('locale', '-')
    get_locale.short_description = "Locale/Language"
    
    def get_country(self, obj):
        """Get country if available"""
        data = obj.extra_data or {}
        # Google doesn't always provide country, but we try common fields
        country = data.get('country', data.get('location', '-'))
        return country
    get_country.short_description = "Country/Location"
    
    def get_all_data(self, obj):
        """Display all extra data in formatted JSON"""
        import json
        data = obj.extra_data or {}
        formatted_json = json.dumps(data, indent=2, ensure_ascii=False)
        return format_html('<pre style="background: #f5f5f5; padding: 10px; border-radius: 5px;">{}</pre>', formatted_json)
    get_all_data.short_description = "Complete Profile Data (JSON)"


# Register the custom SocialAccount admin (replaces allauth default)
# This needs to be done after allauth has loaded, so we do it via apps.py ready() method
try:
    admin.site.unregister(SocialAccount)
    admin.site.register(SocialAccount, CustomSocialAccountAdmin)
except Exception:
    # If already unregistered or not yet registered, will be handled in apps.py
    pass
