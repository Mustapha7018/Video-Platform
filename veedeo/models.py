from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='thumbnails/', default='thumbnails/camera.jpg')
    video_file = models.FileField(upload_to='videos/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


    def posted_time_ago(self):
        now = timezone.now()
        diff = now - self.uploaded_at
        
        periods = [
            (365, "year"),
            (30, "month"),
            (1, "day"),
            (3600, "hour", True),  
            (60, "minute", True)   
        ]
        
        for period, unit, *is_seconds in periods:
            if is_seconds:
                temp = diff.seconds // period
            else:
                temp = diff.days // period
            
            if temp > 0:
                unit_plural = unit if temp == 1 else f"{unit}s"
                return f"{temp} {unit_plural} ago"
        
        return "just now"

