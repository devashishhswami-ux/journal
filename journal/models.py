from django.db import models
from django.conf import settings

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

    def __str__(self):
        return f"{self.title} ({self.created_at.strftime('%Y-%m-%d')})"
