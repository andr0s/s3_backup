from django.contrib import admin

from s3_backup.models import S3Backup


class S3BackupAdmin(admin.ModelAdmin):
    list_display = ('s3_file', 'created_at')


admin.site.register(S3Backup, S3BackupAdmin)
