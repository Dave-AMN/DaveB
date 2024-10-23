import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import os

class S3PhotoManager:
    def __init__(self, bucket_name):
        self.s3_client = boto3.client('s3')
        self.bucket_name = bucket_name

    def upload_photo(self, folder, file_ID=None):
        if file_ID is None:
            file_ID = os.path.basename(folder)

        try:
            self.s3_client.upload_file(folder, self.bucket_name, file_ID)
            print(f"Uploaded {folder} to {self.bucket_name}/{file_ID}")
        except FileNotFoundError:
            print(f"The file was not found: {folder}")
        except NoCredentialsError:
            print("Credentials not available")
        except ClientError as e:
            print(f"Failed to upload file: {e}")

    def download_photo(self, file_ID, folder):
        try:
            self.s3_client.download_file(self.bucket_name, file_ID, folder)
            print(f"Downloaded {file_ID} to {folder}")
        except ClientError as e:
            print(f"Failed to download file: {e}")

    def list_photos(self):
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
            print("Photos in bucket:")
            for obj in response.get('Contents', []):
                print(f" - {obj['Key']}")
        except ClientError as e:
            print(f"Failed to list photos: {e}")

    def delete_photo(self, object_name):

        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_name)
            print(f"Deleted {object_name} from {self.bucket_name}")
        except ClientError as e:
            print(f"Failed to delete file: {e}")

# Example usage:
if __name__ == "__main__":
    bucket_name = 'davedive'  
    photo_manager = S3PhotoManager(bucket_name)

    # photo_manager.upload_photo('path/to/photo.jpg')

    # photo_manager.list_photos()

    photo_manager.download_photo('GPTempDownload.JPG', "davedive")

    # photo_manager.delete_photo('photo.jpg')
