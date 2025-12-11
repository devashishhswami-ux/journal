from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Entry, SiteConfiguration

User = get_user_model()

# Customize the Admin Site Header
admin.site.site_header = "Journal App Administration"
admin.site.site_title = "Journal Admin Portal"
admin.site.index_title = "Welcome to the Journal Control Panel"

# Unregister Group if not needed (optional, keeping it clean)
# admin.site.unregister(Group)

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'ip_address', 'duration_str')
    list_filter = ('created_at', 'user')
    search_fields = ('title', 'content', 'user__username', 'ip_address')
    readonly_fields = ('created_at', 'updated_at', 'ip_address')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    fieldsets = (
        ('Entry Details', {
            'fields': ('user', 'title', 'content')
        }),
        ('Meta Info', {
            'fields': ('duration_str', 'ip_address', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(SiteConfiguration)
class SiteInfoAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'allow_registration', 'maintenance_mode')
    fieldsets = (
        ('General Settings', {
            'fields': ('site_name', 'welcome_message')
        }),
        ('Access Control', {
            'fields': ('allow_registration', 'maintenance_mode'),
            'description': "<span style='color:red;'>Warning: Maintenance mode will block all non-admin users.</span>"
        }),
    )
    
    # Restrict creation/deletion to ensure singleton behavior in UI
    def has_add_permission(self, request):
        return not SiteConfiguration.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
