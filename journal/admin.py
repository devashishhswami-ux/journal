from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Entry, SiteConfiguration
from django.utils.html import format_html


class EntryInline(admin.TabularInline):
    """Inline display of journal entries for each user"""
    model = Entry
    extra = 0
    fields = ('title', 'created_at', 'ip_address', 'view_entry_link')
    readonly_fields = ('created_at', 'view_entry_link')
    can_delete = False
    show_change_link = True
    
    def view_entry_link(self, obj):
        if obj.pk:
            return format_html(
                '<a href="/admin/journal/entry/{}/change/" target="_blank">View Full Entry</a>',
                obj.pk
            )
        return "-"
    view_entry_link.short_description = "Actions"


class CustomUserAdmin(BaseUserAdmin):
    """Enhanced User admin showing journal entry counts and user info"""
    list_display = ('username', 'email', 'entry_count', 'date_joined', 'is_active', 'is_staff')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    inlines = [EntryInline]
    
    def entry_count(self, obj):
        """Display number of journal entries for this user"""
        count = obj.entries.count()
        if count > 0:
            return format_html(
                '<a href="/admin/journal/entry/?user__id__exact={}">{} entries</a>',
                obj.pk,
                count
            )
        return "0 entries"
    entry_count.short_description = "Journal Entries"
    entry_count.admin_order_field = 'entries__count'


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    """Enhanced Entry admin with IP tracking and user info"""
    list_display = ('title', 'user_link', 'created_at', 'ip_address', 'word_count', 'duration_str')
    list_filter = ('created_at', 'user')
    search_fields = ('title', 'content', 'user__username', 'ip_address')
    readonly_fields = ('created_at', 'updated_at', 'ip_address', 'word_count', 'content_preview')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Entry Information', {
            'fields': ('user', 'title', 'content')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'duration_str', 'ip_address'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('word_count', 'content_preview'),
            'classes': ('collapse',)
        }),
    )
    
    def user_link(self, obj):
        """Clickable link to user's admin page"""
        return format_html(
            '<a href="/admin/auth/user/{}/change/">{}</a>',
            obj.user.pk,
            obj.user.username
        )
    user_link.short_description = "User"
    user_link.admin_order_field = 'user__username'
    
    def word_count(self, obj):
        """Display word count of entry content"""
        from django.utils.html import strip_tags
        text = strip_tags(obj.content)
        return len(text.split())
    word_count.short_description = "Word Count"
    
    def content_preview(self, obj):
        """Show first 200 characters of content"""
        from django.utils.html import strip_tags
        text = strip_tags(obj.content)
        if len(text) > 200:
            return text[:200] + "..."
        return text
    content_preview.short_description = "Content Preview"


@admin.register(SiteConfiguration)
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
