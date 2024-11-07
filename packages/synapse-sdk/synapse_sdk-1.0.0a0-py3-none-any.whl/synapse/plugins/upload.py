import os
import re
import subprocess
import tempfile
import hashlib
from pathlib import Path

import boto3


def calculate_checksum(file_path):
    md5_hash = hashlib.md5()
    with open(file_path, 'rb') as f:
        for byte_block in iter(lambda: f.read(4096), b''):
            md5_hash.update(byte_block)
    checksum = md5_hash.hexdigest()
    return f'dev-{checksum}'


def upload_to_s3(file_path, bucket_name, object_name, endpoint_url, access_key, secret_key):
    s3_client = boto3.client(
        's3',
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    s3_client.upload_file(file_path, bucket_name, object_name)


def upload_path(
    source_path,
    endpoint_url=None,
    bucket_name=None,
    access_key=None,
    secret_key=None,
    base_url=None,
):
    if not endpoint_url:
        endpoint_url = os.environ['PLUGIN_UPLOAD_S3_ENDPOINT_URL']
    if not bucket_name:
        bucket_name = os.environ['PLUGIN_UPLOAD_S3_BUCKET_NAME']
    if not access_key:
        access_key = os.environ['PLUGIN_UPLOAD_S3_ACCESS_KEY']
    if not secret_key:
        secret_key = os.environ['PLUGIN_UPLOAD_S3_SECRET_KEY']
    if not base_url:
        base_url = os.environ['PLUGIN_UPLOAD_S3_BASE_URL']

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_archive_path = os.path.join(temp_dir, 'archive.zip')
        command = f'git ls-files --others --exclude-standard --cached  | zip -q --names-stdin {temp_archive_path}'

        subprocess.run(command, cwd=source_path, shell=True, check=True)

        checksum = calculate_checksum(temp_archive_path)
        # TODO subpath param으로 받기
        s3_object_name = f'assets/{checksum}.zip'

        upload_to_s3(temp_archive_path, bucket_name, s3_object_name, endpoint_url, access_key, secret_key)
        return f'{base_url}/{bucket_name}/{s3_object_name}'


def change_whl_version(whl_name, new_version):
    pattern = r'^(?P<distribution>.+?)-(?P<version>\d+(\.\d+)*)(?P<rest>-.+\.whl)$'
    return re.sub(pattern, rf'\g<distribution>-{new_version}\g<rest>', whl_name)


def build_and_upload(source_path, endpoint_url, bucket_name, access_key, secret_key, base_url, virtualenv_path='.venv'):
    # TODO 이미 빌드한 whl이 있으면 skip
    subprocess.run(f'{virtualenv_path}/bin/python -m build --wheel', cwd=source_path, shell=True, check=True)

    whl_file = next(Path(source_path, 'dist').glob('*.whl'), None)
    checksum = calculate_checksum(whl_file)

    # TODO subpath param으로 받기
    s3_object_name = f'assets/{change_whl_version(whl_file.name, checksum)}'

    upload_to_s3(str(whl_file), bucket_name, s3_object_name, endpoint_url, access_key, secret_key)
    return f'{base_url}/{bucket_name}/{s3_object_name}'
