# s3_backup
A Django app that backs up the database into an AWS S3 bucket.

MIT license.

Set the following settings in your setttings.py:

```
S3_BACKUP_BUCKET_NAME - the name of the S3 bucket to back up to
S3_BACKUP_ACCESS_KEY_ID - your S3 access key
S3_BACKUP_SECRET_KEY - your S3 secret key
```

Add `s3_backup` to your `INSTALLED_APPS`.

Run `manage.py migrate` (or `manage.py migrate s3_backup`) to create models in the DB.

Update your cron file and add something like:

```
1  */11  *  *  *  cd /home/your_project_dir; /path/to/your/python manage.py do_s3_backup
```

Done.
