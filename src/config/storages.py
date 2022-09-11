from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class PublicMediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False
    custom_domain = f"{settings.S3_EXTERNAL_DOMAIN}/{settings.AWS_STORAGE_BUCKET_NAME}"
