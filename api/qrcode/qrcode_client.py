import qrcode
from io import BytesIO
import base64
import os
from api.qrcode.qr_image_store import store_qr_image

QR_BASE_URL = os.getenv("QR_CODE_BASE_URL")
def generate_qr_code(gameId:str):
    url = f"{QR_BASE_URL}?gameId={gameId}"
    # Create a QR code
    qr = qrcode.make(url)

    #  save Qr code in an in-memory byte
    generated_qr = store_qr_image(qr, gameId)
    generated_qr["gameUrl"]= url
    return generated_qr



