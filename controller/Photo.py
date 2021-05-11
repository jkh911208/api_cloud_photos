import cv2
import numpy


class Photo(object):
    def __init__(self):
        pass
    async def upload_media(self, file):
        print(file.content_type, type(file.content_type))
        # byte = async file.read()
        img = cv2.imdecode(numpy.fromstring(await file.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
        print(img.shape)

