from storages.backends.s3boto3 import S3Boto3Storage
from . import settings

class PublicMediaStorage(S3Boto3Storage):
    """فایل‌های عمومی - همه می‌تونن ببینن"""
    location = 'sorna-public'
    default_acl = 'public-read'
    file_overwrite = False

class LogoStorage(S3Boto3Storage):
    """فایل‌های عمومی - همه می‌تونن ببینن"""
    location = 'sorna-public-logo'
    default_acl = 'public-read'
    file_overwrite = False
 

class PrivateMediaStorage(S3Boto3Storage):
    """فایل‌های خصوصی - نیاز به احراز هویت"""
    location = 'sorna-private'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False  # لینک مستقیم کار نمی‌کنه
    querystring_auth = True
 

class CKEditorMediaStorage(S3Boto3Storage):
    location = 'uploads/ckeditor'
    default_acl = 'public-read'
    file_overwrite = False