import io
import json
import logging
import mimetypes
from typing import Any, Dict, Iterable, Optional, Tuple

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from django.conf import settings


logger = logging.getLogger(__name__)


def _infer_region_from_endpoint(endpoint_url: str) -> str:
    """Infer Spaces region from an endpoint URL like https://fra1.digitaloceanspaces.com."""
    try:
        host = endpoint_url.replace("https://", "").replace("http://", "")
        return host.split(".")[0]
    except Exception:  # pragma: no cover
        return "us-east-1"


def get_s3_client(
    *,
    access_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    endpoint_url: Optional[str] = None,
    region_name: Optional[str] = None,
) -> Any:
    """
    Return a boto3 S3-compatible client configured for DigitalOcean Spaces.

    Reads defaults from Django settings:
      - settings.AWS_ACCESS_KEY_ID
      - settings.AWS_SECRET_ACCESS_KEY
      - settings.AWS_S3_ENDPOINT_URL (e.g., https://fra1.digitaloceanspaces.com)
      - settings.AWS_S3_REGION_NAME (optional; inferred from endpoint if missing)
    """
    access_key = access_key or getattr(settings, "AWS_ACCESS_KEY_ID", None)
    secret_key = secret_key or getattr(settings, "AWS_SECRET_ACCESS_KEY", None)
    endpoint_url = endpoint_url or getattr(settings, "AWS_S3_ENDPOINT_URL", None)

    if not endpoint_url:
        raise ValueError("AWS_S3_ENDPOINT_URL no está configurado en settings")

    if not access_key or not secret_key:
        raise ValueError(
            "Credenciales de Spaces no configuradas. Define AWS_ACCESS_KEY_ID y AWS_SECRET_ACCESS_KEY."
        )

    region_name = (
        region_name
        or getattr(settings, "AWS_S3_REGION_NAME", None)
        or _infer_region_from_endpoint(endpoint_url)
    )

    # Force AWS v4 signing for Spaces
    cfg = Config(signature_version="s3v4")
    return boto3.client(
        "s3",
        region_name=region_name,
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=cfg,
    )


def get_bucket_name(default: Optional[str] = None) -> str:
    bucket = getattr(settings, "AWS_STORAGE_BUCKET_NAME", default)
    if not bucket:
        raise ValueError("AWS_STORAGE_BUCKET_NAME no está configurado en settings")
    return bucket


def _guess_content_type(key: str, fallback: str = "application/octet-stream") -> str:
    ctype, _ = mimetypes.guess_type(key)
    return ctype or fallback


def put_bytes(
    key: str,
    data: bytes | str,
    *,
    bucket: Optional[str] = None,
    content_type: Optional[str] = None,
    cache_control: Optional[str] = None,
    content_disposition: Optional[str] = None,
    acl: Optional[str] = None,  # e.g., "private" | "public-read"
    metadata: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """Upload raw bytes or string to Spaces using PutObject."""
    s3 = get_s3_client()
    bucket = bucket or get_bucket_name()
    if isinstance(data, str):
        data = data.encode("utf-8")
    extra: Dict[str, Any] = {}
    if content_type:
        extra["ContentType"] = content_type
    else:
        extra["ContentType"] = _guess_content_type(key)
    if cache_control:
        extra["CacheControl"] = cache_control
    if content_disposition:
        extra["ContentDisposition"] = content_disposition
    if acl:
        extra["ACL"] = acl
    if metadata:
        extra["Metadata"] = metadata
    try:
        resp = s3.put_object(Bucket=bucket, Key=key, Body=data, **extra)
        return resp
    except ClientError as e:  # pragma: no cover - runtime path
        logger.exception("Error subiendo objeto a Spaces: %s", e)
        raise


def upload_file(
    file_path: str,
    key: str,
    *,
    bucket: Optional[str] = None,
    content_type: Optional[str] = None,
    cache_control: Optional[str] = None,
    content_disposition: Optional[str] = None,
    acl: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
) -> None:
    """Upload a local file path using the high-level Transfer Manager."""
    s3 = get_s3_client()
    bucket = bucket or get_bucket_name()
    extra_args: Dict[str, Any] = {}
    extra_args["ContentType"] = content_type or _guess_content_type(key)
    if cache_control:
        extra_args["CacheControl"] = cache_control
    if content_disposition:
        extra_args["ContentDisposition"] = content_disposition
    if acl:
        extra_args["ACL"] = acl
    if metadata:
        extra_args["Metadata"] = metadata

    try:
        s3.upload_file(file_path, bucket, key, ExtraArgs=extra_args)
    except ClientError as e:  # pragma: no cover
        logger.exception("Error subiendo archivo a Spaces: %s", e)
        raise


def download_file(key: str, dest_path: str, *, bucket: Optional[str] = None) -> None:
    s3 = get_s3_client()
    bucket = bucket or get_bucket_name()
    try:
        s3.download_file(bucket, key, dest_path)
    except ClientError as e:  # pragma: no cover
        logger.exception("Error descargando archivo de Spaces: %s", e)
        raise


def get_object_bytes(key: str, *, bucket: Optional[str] = None) -> bytes:
    s3 = get_s3_client()
    bucket = bucket or get_bucket_name()
    try:
        resp = s3.get_object(Bucket=bucket, Key=key)
        return resp["Body"].read()
    except ClientError as e:  # pragma: no cover
        logger.exception("Error obteniendo objeto de Spaces: %s", e)
        raise


def head_object(key: str, *, bucket: Optional[str] = None) -> Dict[str, Any]:
    s3 = get_s3_client()
    bucket = bucket or get_bucket_name()
    try:
        return s3.head_object(Bucket=bucket, Key=key)
    except ClientError as e:  # pragma: no cover
        logger.exception("Error en HEAD de objeto en Spaces: %s", e)
        raise


def delete_object(key: str, *, bucket: Optional[str] = None) -> None:
    s3 = get_s3_client()
    bucket = bucket or get_bucket_name()
    try:
        s3.delete_object(Bucket=bucket, Key=key)
    except ClientError as e:  # pragma: no cover
        logger.exception("Error eliminando objeto en Spaces: %s", e)
        raise


def list_objects(
    *,
    prefix: Optional[str] = None,
    marker: Optional[str] = None,
    max_keys: int = 1000,
    bucket: Optional[str] = None,
) -> Tuple[Iterable[Dict[str, Any]], bool, Optional[str]]:
    """
    List objects using ListObjects (V1) — V2 is not supported by Spaces.

    Returns (items, is_truncated, next_marker)
    """
    s3 = get_s3_client()
    bucket = bucket or get_bucket_name()
    kwargs: Dict[str, Any] = {"Bucket": bucket, "MaxKeys": max_keys}
    if prefix:
        kwargs["Prefix"] = prefix
    if marker:
        kwargs["Marker"] = marker
    try:
        resp = s3.list_objects(**kwargs)
        contents = resp.get("Contents", [])
        is_truncated = resp.get("IsTruncated", False)
        next_marker = resp.get("NextMarker")
        return contents, is_truncated, next_marker
    except ClientError as e:  # pragma: no cover
        logger.exception("Error listando objetos en Spaces: %s", e)
        raise


def copy_object(
    source_key: str,
    dest_key: str,
    *,
    source_bucket: Optional[str] = None,
    dest_bucket: Optional[str] = None,
    acl: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None,
    metadata_directive: str = "COPY",  # or "REPLACE"
) -> Dict[str, Any]:
    """Copy an object within the same region/Space. Cross-region is not supported by Spaces."""
    s3 = get_s3_client()
    source_bucket = source_bucket or get_bucket_name()
    dest_bucket = dest_bucket or get_bucket_name()
    copy_source = {"Bucket": source_bucket, "Key": source_key}
    extra: Dict[str, Any] = {"MetadataDirective": metadata_directive}
    if acl:
        extra["ACL"] = acl
    if metadata and metadata_directive == "REPLACE":
        extra["Metadata"] = metadata
    try:
        return s3.copy_object(Bucket=dest_bucket, Key=dest_key, CopySource=copy_source, **extra)
    except ClientError as e:  # pragma: no cover
        logger.exception("Error copiando objeto en Spaces: %s", e)
        raise


def set_object_acl(key: str, acl: str, *, bucket: Optional[str] = None) -> None:
    s3 = get_s3_client()
    bucket = bucket or get_bucket_name()
    try:
        s3.put_object_acl(Bucket=bucket, Key=key, ACL=acl)
    except ClientError as e:  # pragma: no cover
        logger.exception("Error aplicando ACL al objeto en Spaces: %s", e)
        raise


def generate_presigned_url(
    key: str,
    *,
    bucket: Optional[str] = None,
    expires_in: int = 3600,
    http_method: str = "get_object",  # "get_object" | "put_object"
    content_type: Optional[str] = None,  # used for put_object signature
) -> str:
    """Generate a pre-signed URL to GET or PUT an object."""
    s3 = get_s3_client()
    bucket = bucket or get_bucket_name()
    params: Dict[str, Any] = {"Bucket": bucket, "Key": key}
    if http_method == "put_object" and content_type:
        params["ContentType"] = content_type
    try:
        return s3.generate_presigned_url(
            ClientMethod=http_method,
            Params=params,
            ExpiresIn=expires_in,
        )
    except ClientError as e:  # pragma: no cover
        logger.exception("Error generando URL prefirmada en Spaces: %s", e)
        raise


def public_url(key: str, *, bucket: Optional[str] = None) -> str:
    """
    Build the public URL for an object if bucket/object is public.
    Uses settings.AWS_S3_CUSTOM_DOMAIN when available for cleaner URLs.
    """
    bucket = bucket or get_bucket_name()
    custom_domain = getattr(settings, "AWS_S3_CUSTOM_DOMAIN", None)
    if custom_domain:
        return f"https://{custom_domain}/{key}"
    endpoint_url = getattr(settings, "AWS_S3_ENDPOINT_URL", "https://digitaloceanspaces.com")
    host = endpoint_url.replace("https://", "").replace("http://", "")
    return f"https://{bucket}.{host}/{key}"


# Bucket policy helpers


def get_bucket_policy(*, bucket: Optional[str] = None) -> Dict[str, Any]:
    s3 = get_s3_client()
    bucket = bucket or get_bucket_name()
    try:
        resp = s3.get_bucket_policy(Bucket=bucket)
        return json.loads(resp.get("Policy", "{}"))
    except s3.exceptions.NoSuchBucketPolicy:
        return {}
    except ClientError as e:  # pragma: no cover
        if e.response.get("Error", {}).get("Code") == "NoSuchBucketPolicy":
            return {}
        logger.exception("Error obteniendo bucket policy: %s", e)
        raise


def put_bucket_policy(policy: Dict[str, Any], *, bucket: Optional[str] = None) -> None:
    s3 = get_s3_client()
    bucket = bucket or get_bucket_name()
    try:
        s3.put_bucket_policy(Bucket=bucket, Policy=json.dumps(policy))
    except ClientError as e:  # pragma: no cover
        logger.exception("Error aplicando bucket policy: %s", e)
        raise


def delete_bucket_policy(*, bucket: Optional[str] = None) -> None:
    s3 = get_s3_client()
    bucket = bucket or get_bucket_name()
    try:
        s3.delete_bucket_policy(Bucket=bucket)
    except ClientError as e:  # pragma: no cover
        logger.exception("Error eliminando bucket policy: %s", e)
        raise


# Bucket CORS helpers


def get_bucket_cors(*, bucket: Optional[str] = None) -> Dict[str, Any]:
    s3 = get_s3_client()
    bucket = bucket or get_bucket_name()
    try:
        return s3.get_bucket_cors(Bucket=bucket)
    except s3.exceptions.NoSuchCORSConfiguration:
        return {}
    except ClientError as e:  # pragma: no cover
        if e.response.get("Error", {}).get("Code") == "NoSuchCORSConfiguration":
            return {}
        logger.exception("Error obteniendo CORS del bucket: %s", e)
        raise


def put_bucket_cors(cors_rules: Dict[str, Any], *, bucket: Optional[str] = None) -> None:
    """
    Put CORS configuration. Example cors_rules:
    {"CORSRules": [
        {"AllowedMethods": ["GET"], "AllowedOrigins": ["*"], "AllowedHeaders": ["*"]}
    ]}
    """
    s3 = get_s3_client()
    bucket = bucket or get_bucket_name()
    try:
        s3.put_bucket_cors(Bucket=bucket, CORSConfiguration=cors_rules)
    except ClientError as e:  # pragma: no cover
        logger.exception("Error configurando CORS del bucket: %s", e)
        raise


def delete_bucket_cors(*, bucket: Optional[str] = None) -> None:
    s3 = get_s3_client()
    bucket = bucket or get_bucket_name()
    try:
        s3.delete_bucket_cors(Bucket=bucket)
    except ClientError as e:  # pragma: no cover
        logger.exception("Error eliminando CORS del bucket: %s", e)
        raise


__all__ = [
    "get_s3_client",
    "get_bucket_name",
    "put_bytes",
    "upload_file",
    "download_file",
    "get_object_bytes",
    "head_object",
    "delete_object",
    "list_objects",
    "copy_object",
    "set_object_acl",
    "generate_presigned_url",
    "public_url",
    "get_bucket_policy",
    "put_bucket_policy",
    "delete_bucket_policy",
    "get_bucket_cors",
    "put_bucket_cors",
    "delete_bucket_cors",
]

