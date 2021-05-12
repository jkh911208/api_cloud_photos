import io
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
        supported_format = {"jpeg", "jpg"}
        file_format = file.content_type.split("/")[1]
        if file_format.lower() not in supported_format:
            raise ValueError(f"Image format of {file_format} is not supported")


        # read image
        file_bytes = await file.read()
        img = Image.open(io.BytesIO(file_bytes))
        img_exif = img._getexif()

        exif = {}
        for key, val in img_exif.items():
            if key in ExifTags.TAGS:
                exif[ExifTags.TAGS[key]] = val
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

        if "GPSInfo" in exif:
            payload["latitude"] = float((exif["GPSInfo"][2][0] + exif["GPSInfo"][2][1] / 60 + exif["GPSInfo"][2][2] / 3600) * 1 if exif["GPSInfo"][1] == "N" else -1)
            payload["longitude"] = float((exif["GPSInfo"][4][0] + exif["GPSInfo"][4][1] / 60 + exif["GPSInfo"][4][2] / 3600) * (1 if exif["GPSInfo"][3] == "E" else -1))

        print(payload)
        with open(f"{id}.{file_format}",'wb+') as f:
            f.write(file_bytes)
            f.close()
        img.thumbnail((2560,2560), Image.LANCZOS)
        img.save(f"{id}-resize.{file_format}", file_format)
        img.thumbnail((512,512), Image.LANCZOS)
        img.save(f"{id}-thumbnail.{file_format}", file_format)

        return payload

    async def __process_video(self, file, owner_id):
        pass

