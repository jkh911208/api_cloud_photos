import io
import os
from datetime import datetime
from uuid import uuid4

import config
import pytz
from fastapi.responses import StreamingResponse
from PIL import ExifTags, Image
from schema.Photos import Photos
from timezonefinder import TimezoneFinder


class Photo(object):
    def __init__(self):
        pass

    async def get_resized_image(self, id, owner_id):
        img = await Photos.get_by_id(id)
        print(img)
        if owner_id != img["owner"]:
            raise ValueError("Not authenticated")

        complete_path = f"{config.STORE_PATH}/{owner_id}/"
        filename_split = img["new_filename"].split(".")
        resize_filename = f"{filename_split[0]}-resize.{filename_split[1]}"
        img = open(f"{complete_path}{resize_filename}", mode="rb")
        return StreamingResponse(img, media_type=f"image/{filename_split[1]}")

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
        if img_exif is not None:
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
            "new_filename": f"{id}.{file_format}",
            "owner": owner_id,
            "status": 1
        }

        if "GPSInfo" in exif:
            payload["latitude"] = float((exif["GPSInfo"][2][0] + exif["GPSInfo"][2][1] /
                                        60 + exif["GPSInfo"][2][2] / 3600) * 1 if exif["GPSInfo"][1] == "N" else -1)
            payload["longitude"] = float((exif["GPSInfo"][4][0] + exif["GPSInfo"][4][1] /
                                         60 + exif["GPSInfo"][4][2] / 3600) * (1 if exif["GPSInfo"][3] == "E" else -1))

            if payload["original_datetime"] is not None:
                tf = TimezoneFinder()
                timezone_str = tf.certain_timezone_at(
                    lat=payload["latitude"], lng=payload["longitude"])
                local = pytz.timezone(timezone_str)
                naive = datetime.strptime(
                    payload["original_datetime"], "%Y:%m:%d %H:%M:%S")
                local_dt = local.localize(naive, is_dst=None)
                utc_dt = local_dt.astimezone(pytz.utc)
                payload["original_datetime"] = datetime.strptime(
                    utc_dt.strftime("%Y:%m:%d %H:%M:%S"), "%Y:%m:%d %H:%M:%S")
        else:
            if payload["original_datetime"] is None:
                payload["original_datetime"] = datetime.utcnow()
            else:
                payload["original_datetime"] = datetime.strptime(
                    payload["original_datetime"], "%Y:%m:%d %H:%M:%S")

        complete_path = f"{config.STORE_PATH}/{owner_id}/"
        if not os.path.exists(complete_path):
            os.makedirs(complete_path)

        with open(f"{complete_path}{id}.{file_format}", 'wb+') as f:
            f.write(file_bytes)
            f.close()
        img.thumbnail((2560, 2560), Image.LANCZOS)
        img.save(f"{complete_path}{id}-resize.{file_format}", file_format)
        img.thumbnail((512, 512), Image.LANCZOS)
        img.save(f"{complete_path}{id}-thumbnail.{file_format}", file_format)
        print(payload)
        await file.close()
        await Photos.insert(**payload)
        return payload

    async def __process_video(self, file, owner_id):
        pass
