import requests
from PIL import Image
import io
import base64
import traceback

def get_image():
    url = "https://d2ktwrbyxtrufc.cloudfront.net/images/seed_image.png"
    response = requests.get(url)
    if response.status_code == 200:
        return base64.b64encode(response.content).decode('utf8')
    else:
        raise Exception(f"이미지 다운로드 실패: {response.status_code}")

print(get_image())


