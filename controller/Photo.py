import io
import shutil
from uuid import uuid4

from PIL import ExifTags, Image


class Photo(object):
    def __init__(self):
        pass
    async def upload_media(self, file, owner_id):
        content_type = file.content_type
        if content_type.startswith("image/"):
            return await self.__process_image(file, owner_id)
        elif content_type.startswith("video/"):
            return await self.__process_video(file, owner_id)
        else:
            raise ValueError(f"Not supported type : {content_type}")

    async def __process_image(self, file, owner_id):
        supported_format = {"jpeg", "jpg", "png"}
        file_format = file.content_type.split("/")[1]
        if file_format.lower() not in supported_format:
            raise ValueError(f"Image format of {file_format} is not supported")


        # read image
        file_bytes = await file.read()
        img = Image.open(io.BytesIO(file_bytes))
        img_exif = img.getexif()

        exif = {}
        for key, val in img_exif.items():
            if key in ExifTags.TAGS:
                exif[ExifTags.TAGS[key]] = val

        print(exif)

        width, height = img.size
        id = str(uuid4())
        payload = {
            "id": id,
            "original_filename": file.filename,
            "original_datetime": exif["DateTime"] if "DateTime" in exif else None,
            "original_make": exif["Make"] if "Make" in exif else None,
            "original_model": exif["Model"] if "Model" in exif else None,
            "original_width": width,
            "original_height": height,
            "new_filename": f"{id}.png",
            "thumbnail": f"{id}-thumbnail.png",
            "owner" : owner_id,
            "status": 1
        }
        from time import time
        init = time()
        with open(f"{id}.{file_format}",'wb+') as f:
            f.write(file_bytes)
            f.close()
        print("save original", time()-init)
        init = time()
        img.thumbnail((2560,2560), Image.LANCZOS)
        print("resize", time()-init)
        init = time()
        img.save(f"{id}-resize.{file_format}", file_format)
        print("save resize", time()-init)
        init = time()
        img.thumbnail((256,256), Image.LANCZOS)
        print("thumbnail", time()-init)
        init = time()
        img.save(f"{id}-thumbnail.{file_format}", file_format)
        print("save thumbnail", time()-init)

        return payload

    async def __process_video(self, file, owner_id):
        pass

