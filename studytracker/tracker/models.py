from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    date_time = models.DateTimeField(default=timezone.now)
    duration = models.FloatField(help_text="Duration in hours")
    productivity_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    
    def __str__(self):
        return f"{self.subject} - {self.date_time.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['-date_time']
