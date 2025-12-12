from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Entry, SiteConfiguration


class CustomUserAdmin(BaseUserAdmin):
    """Simplified User admin showing email and essential info"""
    list_display = ('email', 'entry_count', 'date_joined', 'is_active')
    list_filter = ('is_active', 'date_joined')
    search_fields = ('email', 'username')
    ordering = ('-date_joined',)
    
    def entry_count(self, obj):
        """Display number of journal entries"""
        return obj.entries.count()
    entry_count.short_description = "Journals"


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
