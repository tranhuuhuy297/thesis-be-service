import io
import requests
from PIL import Image
import uuid


def compress_image(image_src):
    try:
        res = requests.get(image_src)
        image = Image.open(io.BytesIO(res.content))

        image.save(str(uuid.uuid1()),
                   "JPEG",
                   optimize=True,
                   quality=10)
    except:
        return None

    return str(uuid.uuid1())
