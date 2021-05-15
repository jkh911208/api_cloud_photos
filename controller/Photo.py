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

    async def get_photo_list(self, skip, owner_id):
        return await Photos.get_by_owner(owner_id, skip, 100)

    async def get_image(self, filename, owner_id):
        format = filename.split(".")[-1]
        file_path = f"{config.STORE_PATH}/{owner_id}/{filename}"
        img = open(file_path, mode="rb")
        return StreamingResponse(img, media_type=f"image/{format}")

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

        id = str(uuid4())

        # read image
        file_bytes = await file.read()
        img = Image.open(io.BytesIO(file_bytes))
        await file.close()

        # parse exif and size
        img_exif = img._getexif()
        exif = {}
        width, height = img.size
        if img_exif is not None:
            for key, val in img_exif.items():
                if key in ExifTags.TAGS:
                    exif[ExifTags.TAGS[key]] = val
            if "Orientation" in exif:
                if exif["Orientation"] > 4:
                    height, width = img.size

        # build db payload
        payload = {
            "id": id,
            "original_filename": file.filename,
            "original_datetime": exif["DateTime"] if "DateTime" in exif else None,
            "original_make": exif["Make"] if "Make" in exif else None,
            "original_model": exif["Model"] if "Model" in exif else None,
            "original_width": width,
            "original_height": height,
            "new_filename": f"{id}.{file_format}",
            "thumbnail": f"{id}-thumbnail.{file_format}",
            "resize": f"{id}-resize.{file_format}",
            "owner": owner_id,
            "status": 1
        }

        # parse GPS info into coordinate
        if "GPSInfo" in exif:
            payload["latitude"] = float((exif["GPSInfo"][2][0] + exif["GPSInfo"][2][1] /
                                        60 + exif["GPSInfo"][2][2] / 3600) * 1 if exif["GPSInfo"][1] == "N" else -1)
            payload["longitude"] = float((exif["GPSInfo"][4][0] + exif["GPSInfo"][4][1] /
                                         60 + exif["GPSInfo"][4][2] / 3600) * (1 if exif["GPSInfo"][3] == "E" else -1))

            # change datetime into UTC
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
        # write payload to DB
        await Photos.insert(**payload)

        # save file to disk
        complete_path = f"{config.STORE_PATH}/{owner_id}/"
        if not os.path.exists(complete_path):
            os.makedirs(complete_path)
        # save original file
        with open(f"{complete_path}{id}.{file_format}", 'wb+') as f:
            f.write(file_bytes)
            f.close()
        # save resized file
        img.thumbnail((2560, 2560), Image.LANCZOS)
        img.save(f"{complete_path}{id}-resize.{file_format}",
                 file_format, exif=img.info['exif'])
        # save thumbnail
        img.thumbnail((512, 512), Image.LANCZOS)
        img.save(f"{complete_path}{id}-thumbnail.{file_format}",
                 file_format, exif=img.info['exif'])

        return payload

    async def __process_video(self, file, owner_id):
        pass
