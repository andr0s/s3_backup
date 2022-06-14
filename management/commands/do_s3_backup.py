import os
import tempfile
import datetime
import io

import boto3
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

from s3_backup.models import S3Backup


class Command(BaseCommand):
    help = 'Dumps the database and uploads the archived backup file to S3'

    def handle(self, *args, **options):
        bucket_name = settings.S3_BACKUP_BUCKET_NAME
        aws_access_key_id = settings.S3_BACKUP_ACCESS_KEY_ID
        aws_secret_key = settings.S3_BACKUP_SECRET_KEY

        backup_file = tempfile.NamedTemporaryFile(mode='wb', delete=False)
        backup_file.close()

        buf_string = io.StringIO()
        call_command('dumpdata', indent=2, stdout=buf_string)
        buf_string.seek(0)
        with open(backup_file.name, 'w') as f:
            f.write(buf_string.read())

        # TODO: add ZIP compression?

        s3 = boto3.resource('s3',
                            aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_key)

        s3_fname = datetime.datetime.utcnow().strftime('%Y-%m-%d %H-%M-%S') + '.json'
        s3.Bucket(bucket_name).upload_file(backup_file.name, s3_fname)

        os.remove(backup_file.name)

        S3Backup.objects.create(s3_file=s3_fname)

        self.stdout.write(self.style.SUCCESS('Done, file name: %s' % s3_fname))
