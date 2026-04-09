    
from storages.backends.s3boto3 import S3Boto3Storage


class PublicMediaStorage(S3Boto3Storage):
    location = 'sorna-public'
    default_acl = 'public-read'
    file_overwrite = False
    # object_parameters = { "ContentDisposition": "inline" }


class LogoStorage(S3Boto3Storage):
    location = 'sorna-public-logo'
    default_acl = 'public-read'
    file_overwrite = False
    # object_parameters = { "ContentDisposition": "inline" }


class PrivateMediaStorage(S3Boto3Storage):
    location = 'sorna-private'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False
    querystring_auth = True
    # object_parameters = { "ContentDisposition": "inline" }


class CKEditorMediaStorage(S3Boto3Storage):
    location = 'uploads/ckeditor'
    default_acl = 'public-read'
    file_overwrite = False
    # object_parameters = { "ContentDisposition": "inline" }
