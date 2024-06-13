import os

from minio import Minio
from dotenv import load_dotenv

env = os.environ.get
load_dotenv('./.env')

MINIO_URL = env('MINIO_URL').lower().replace('http://', '')
MINIO_ACCESS = env('MINIO_ACCESS')
MINIO_SECRET = env('MINIO_SECRET')

def get_minio_client() -> Minio:
    """
    Minio client creation
    """
    minio_client = Minio(
        endpoint=MINIO_URL,
        access_key=MINIO_ACCESS,
        secret_key=MINIO_SECRET,
        secure=False
    )
    return minio_client
