from django.db import models


class S3Backup(models.Model):
    s3_file = models.CharField(max_length=300, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
