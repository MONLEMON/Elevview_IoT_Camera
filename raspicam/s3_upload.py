import threading
import boto3
import os
from config import BUCKET_NAME
import requests

s3_client = boto3.client("s3")

api_url = "http://18.140.53.117:8000/cameras/api/update-photo-db/"

def delete_image(image_path):
    if os.path.exists(image_path):
        os.remove(image_path)


def upload_photo_s3(image_file,user_id,camera_id):
    s3_path = "user_photos/" + image_file
    image_path = f"/home/monlemon/project/photo/{image_file}"
    try:
        s3_client.upload_file(image_path, BUCKET_NAME, s3_path)
        print(f"Uploaded: {image_file} -> s3://{BUCKET_NAME}/{s3_path}")

        try:
            data = {
                "user_id": f"{user_id}",
                "camera_id": f"{camera_id}",
                "image_url": f"https://elevviews.s3.ap-southeast-1.amazonaws.com/user_photos/{image_file}"
            }
            response = requests.post(api_url, json=data)
            response.raise_for_status()

            delete_image(image_path)
        except Exception as e:
            print(f"Post requests failed: {e}")

    except Exception as e:
        print(f"S3 Upload failed: {e}")

def verify_s3_upload(image_file):
    s3_path = "user_photos/" + image_file
    try:
        s3_client.head_object(Bucket=BUCKET_NAME, Key=s3_path)
        print(f"✅ Verified upload: s3://{BUCKET_NAME}/{s3_path}")
        return True
    except:
        print(f"❌ Upload failed verification: {image_file}")
        return False

def upload_photo_s3_async(image_file,user_id,camera_id):
    thread = threading.Thread(target=lambda: upload_photo_s3(image_file,user_id,camera_id) and verify_s3_upload(image_file))
    thread.start()