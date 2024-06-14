from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def posted_time_ago(self):
        now = timezone.now()
        diff = now - self.uploaded_at
        if diff.days > 365:
            return f"{diff.days // 365} years ago"
        if diff.days > 30:
            return f"{diff.days // 30} months ago"
        if diff.days > 0:
            return f"{diff.days} days ago"
        if diff.seconds > 3600:
            return f"{diff.seconds // 3600} hours ago"
        if diff.seconds > 60:
            return f"{diff.seconds // 60} minutes ago"
        return "just now"
