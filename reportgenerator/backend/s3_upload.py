"""
S3 Upload Utility for Tokamak Network Biweekly Reports.

Uploads full HTML reports to S3 so Gmail can link to them
(bypassing the 102KB email clipping limit).
"""

import os
from datetime import datetime

import boto3
from botocore.exceptions import ClientError


# Defaults from environment
_DEFAULT_BUCKET = os.getenv("S3_BUCKET", "tokamak-reports")
_DEFAULT_PREFIX = os.getenv("S3_REPORT_PREFIX", "reports/biweekly")
_DEFAULT_REGION = os.getenv("AWS_REGION", "ap-northeast-2")


def upload_html_to_s3(
    html_content: str,
    bucket: str = "",
    key: str = "",
    region: str = "",
) -> str:
    """Upload an HTML report to S3 and return its public URL.

    Args:
        html_content: The full HTML string to upload.
        bucket: S3 bucket name. Falls back to S3_BUCKET env var.
        key: S3 object key (e.g. "reports/biweekly-3-2026-02-01.html").
             Auto-generated from timestamp if empty.
        region: AWS region. Falls back to AWS_REGION env var.

    Returns:
        Public URL of the uploaded object.

    Raises:
        ClientError: If the S3 upload fails.
    """
    bucket = bucket or _DEFAULT_BUCKET
    region = region or _DEFAULT_REGION

    if not key:
        ts = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        key = f"{_DEFAULT_PREFIX}-{ts}.html"

    s3 = boto3.client(
        "s3",
        region_name=region,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=html_content.encode("utf-8"),
        ContentType="text/html; charset=utf-8",
    )

    url = f"https://{bucket}.s3.{region}.amazonaws.com/{key}"
    return url
