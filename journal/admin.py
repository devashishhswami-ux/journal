from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse, path
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from .models import Entry, SiteConfiguration
import json


class CustomAdminSite(AdminSite):
    """Custom Admin Site with enhanced dashboard"""
    site_header = "Journal Pro Admin"
    site_title = "Journal Admin"
    index_title = "Dashboard"
    index_template = 'admin/index.html'  # Use custom dashboard template
    
    def index(self, request, extra_context=None):
        """Custom index view with statistics"""
        extra_context = extra_context or {}
        
        # Get site configuration
        site_config = SiteConfiguration.load()
        
        # Calculate statistics
        total_users = User.objects.count()
        total_entries = Entry.objects.count()
        google_users = SocialAccount.objects.filter(provider='google').values('user').distinct().count()
        
        # Today's activity
        today = timezone.now().date()
        today_start = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
        
        new_users_today = User.objects.filter(date_joined__gte=today_start).count()
        entries_today = Entry.objects.filter(created_at__gte=today_start).count()
        
        # Active users today (created entries today)
        active_users_today = Entry.objects.filter(
            created_at__gte=today_start
        ).values('user').distinct().count()
        
        # Recent entries (last 10)
        recent_entries = Entry.objects.select_related('user').order_by('-created_at')[:10]
        
        # Add to context
        extra_context.update({
            'site_config': site_config,
            'total_users': total_users,
            'total_entries': total_entries,
            'google_users': google_users,
            'new_users_today': new_users_today,
            'entries_today': entries_today,
            'active_users_today': active_users_today,
            'recent_entries': recent_entries,
        })
        
        return super().index(request, extra_context)
    
    def get_urls(self):
        """Add custom admin URLs"""
        urls = super().get_urls()
        custom_urls = [
            path('toggle-maintenance/', self.admin_view(self.toggle_maintenance), name='toggle_maintenance'),
            path('get-stats/', self.admin_view(self.get_stats), name='get_stats'),
        ]
        return custom_urls + urls
    
    def toggle_maintenance(self, request):
        """AJAX endpoint to toggle maintenance mode"""
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                maintenance_mode = data.get('maintenance_mode', False)
                
                # Update site configuration
                config = SiteConfiguration.load()
                config.maintenance_mode = maintenance_mode
                config.save()
                
                return JsonResponse({
                    'success': True,
                    'maintenance_mode': maintenance_mode,
                    'message': f'Maintenance mode {"enabled" if maintenance_mode else "disabled"}'
                })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'message': str(e)
                }, status=400)
        
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)
    
    def get_stats(self, request):
        """AJAX endpoint to get updated statistics"""
        total_users = User.objects.count()
        total_entries = Entry.objects.count()
        google_users = SocialAccount.objects.filter(provider='google').values('user').distinct().count()
        
        today = timezone.now().date()
        today_start = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
        active_users_today = Entry.objects.filter(
            created_at__gte=today_start
        ).values('user').distinct().count()
        
        return JsonResponse({
            'total_users': total_users,
            'total_entries': total_entries,
            'google_users': google_users,
            'active_users_today': active_users_today,
        })


# Use custom admin site
admin_site = CustomAdminSite(name='admin')


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


admin_site.register(Entry, EntryAdmin)


class SiteConfigurationAdmin(admin.ModelAdmin):
    """Simple site configuration admin"""
    list_display = ('site_name', 'maintenance_mode', 'allow_registration')
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteConfiguration.objects.exists()


admin_site.register(SiteConfiguration, SiteConfigurationAdmin)


# Register User admin with custom admin site
admin_site.register(User, CustomUserAdmin)


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


# Register the custom SocialAccount admin with custom admin site
admin_site.register(SocialAccount, CustomSocialAccountAdmin)
