from storages.backends.s3boto3 import S3Boto3Storage
from . import settings

class PublicMediaStorage(S3Boto3Storage):
    """فایل‌های عمومی - همه می‌تونن ببینن"""
    location = 'sorna/sorna-public'
    default_acl = 'public-read'
    file_overwrite = False
 

class PrivateMediaStorage(S3Boto3Storage):
    """فایل‌های خصوصی - نیاز به احراز هویت"""
    location = 'sorna/sorna-private'
    default_acl = 'private-read'
    file_overwrite = False
    custom_domain = False  # لینک مستقیم کار نمی‌کنه
 

class CKEditorMediaStorage(S3Boto3Storage):
    location = 'sorna/uploads/ckeditor'
    default_acl = 'public-read'
    file_overwrite = False