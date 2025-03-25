import os
import base64
from io import BytesIO
import boto3

s3 = boto3.client("s3")
# FILE_SYSTEM, AWS_S3, DB
QR_STORE_TYPE=os.getenv("QR_STORAGE_TYPE")
s3_bucket_name = os.getenv("S3_BUCKET_NAME")
s3_qr_folder = os.getenv("S3_QR_FOLDER")
QR_FILESYSTEM_PATH= os.getenv("FILE_SYSTEM_PATH")
class file_system:
    def store_qr(self,qr,gameId):

        try:
            os.makedirs(QR_FILESYSTEM_PATH,exist_ok=True)
            qr_path = os.path.join(QR_FILESYSTEM_PATH,f"{gameId}.png")
            # Save QR Code as file
            qr.save(qr_path)
            return {
                "targetStore":"FS",
                "imageUrl":qr_path
            }
        except Exception as ex:
            print(f"error saving to file system {ex}")
            return {"error":"Unable to save to file system"}

class db_store:
    def store_qr(self,qr,gameId):

        try:
            buffer = BytesIO()
            qr.save(buffer,format="PNG")
            base64Image= base64.b64encode(buffer.getvalue()).decode("utf-8")
            return {
                "targetStore":"DB",
                "imageUrl":base64Image
            }

        except Exception as ex:
            print(f"Error occurred saving qr to database {ex}")
            return {"error":"Unable to save to database"}
class aws_s3:
    def store_qr(self,qr,gameId):

        try:
            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            buffer.seek(0)

            s3.upload_fileobj(buffer, s3_bucket_name, f"{s3_qr_folder}/{gameId}.png")
            s3_storage_url = f"https://{s3_bucket_name}.s3.amazonaws.com/{s3_qr_folder}/{gameId}.png"
            return {
                "targetStore":"DB",
                "imageUrl":s3_storage_url
                }
        except Exception as ex:
            print(f"Error occurred while saving to s3")
store_options={
    "FS":file_system(),
    "DB":db_store(),
    "AWS_S3":aws_s3()
}
def store_qr_image(qr,gameId,store_type="DB"):
    qr_process = store_options.get(store_type)
    return qr_process.store_qr(qr,gameId)