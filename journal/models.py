from django.db import models
from django.conf import settings
from django.core.cache import cache

class Entry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='entries')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    duration_str = models.CharField(max_length=50, default="0s")

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Journal Entries"

    def __str__(self):
        return f"{self.title} ({self.user.username})"

class SiteConfiguration(models.Model):
    site_name = models.CharField(max_length=100, default="Journal App")
    maintenance_mode = models.BooleanField(default=False, help_text="If active, only admins can access the site.")
    allow_registration = models.BooleanField(default=True)
    welcome_message = models.TextField(default="Welcome to your personal secure journal.")
    
    # Singleton pattern enforcement
    def save(self, *args, **kwargs):
        self.pk = 1
        super(SiteConfiguration, self).save(*args, **kwargs)
        cache.set('site_config', self)

    def delete(self, *args, **kwargs):
        pass # Prevent deletion

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Site Configuration"
