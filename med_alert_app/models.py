from django.db import models
from django.contrib.auth.models import User


class SiteAdmin(models.Model):
    user = models.ForeignKey(User, related_name='siteadmin', on_delete=models.CASCADE)


class Report(models.Model):
    upload_time = models.DateTimeField(auto_now_add=True, null=True)
    been_viewed = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    offenders_names = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    date_time_of_offense = models.TextField()
    offense_description = models.TextField()
    action_desired = models.TextField()
    resolved_action = models.TextField(blank=True, null=True)
    edited = models.BooleanField(default=False)


class Document(models.Model):
    upload = models.FileField(null=True, blank=True)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, null=True, default=None)

