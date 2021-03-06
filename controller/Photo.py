import glob
import io
import logging
import os
from datetime import datetime
from time import time
from uuid import uuid4

import config
import pytz
from fastapi.responses import StreamingResponse
from PIL import ExifTags, Image
from pyheif_pillow_opener import register_heif_opener
from schema.Photos import Photos
from timezonefinder import TimezoneFinder


class Photo(object):
    def __init__(self):
        pass

    async def delete_image_by_id(self, id, owner_id):
        logging.info(f"delete id {id} by {owner_id}")
        # delete from DB
        try:
            db_result = await Photos.delete(id)
            logging.info(db_result)
        except Exception:
            pass
        # delete from file system
        file_list = glob.glob(f"{config.STORE_PATH}/{owner_id}/{id}*")
        logging.info(file_list)

        for file_path in file_list:
            try:
                os.remove(file_path)
            except Exception:
                pass

    async def get_photo_list(self, created, owner_id):
        result = await Photos.get_by_owner(owner_id, created)
        result["has_next"] = False
        return result

    async def get_image(self, filename, owner_id):
        format = filename.split(".")[-1]
        file_path = f"{config.STORE_PATH}/{owner_id}/{filename}"
        img = open(file_path, mode="rb")
        return StreamingResponse(img, media_type=f"image/{format}")

    async def upload_media(self, file, owner_id, data):
        content_type = file.content_type
        if content_type.startswith("image/"):
            return await self.__process_image(file, owner_id, data)
        elif content_type.startswith("video/"):
            return await self.__process_video(file, owner_id, data)
        else:
            raise ValueError(f"Not supported type : {content_type}")

    async def __process_image(self, file, owner_id, data):
        logging.info(f"owner id : {owner_id}")
        register_heif_opener()
        supported_format = {"jpeg", "jpg", "heic"}
        file_format = file.content_type.split("/")[1]
        if file_format.lower() not in supported_format:
            raise ValueError(f"Image format of {file_format} is not supported")

        # check if your have same file
        redundant = await self.__check_redundant(owner_id, data["md5"])
        if redundant:
            await file.close()
            return redundant

        # generate uuid4 id
        id = str(uuid4())

        # read image
        file_bytes = await file.read()
        img = Image.open(io.BytesIO(file_bytes))
        await file.close()

        # build db payload
        payload = {
            "id": id,
            "created": int(time()*1000),
            "original_filename": file.filename,
            "original_datetime": data["creation_time"],
            "original_make": None,
            "original_model": None,
            "original_width": data["width"],
            "original_height": data["height"],
            "new_filename": f"{id}.{file_format}",
            "thumbnail": f"{id}-thumbnail.{file_format}",
            "resize": f"{id}-resize.{file_format}",
            "owner": owner_id,
            "status": 1,
            "latitude": None,
            "longitude": None,
            "md5": data["md5"],
            "original_filesize": data["size"],
            "duration": data["duration"]
        }

        if file_format.lower() == "heic":
            payload["thumbnail"] = f"{id}-thumbnail.jpeg"
            payload["resize"] = f"{id}-resize.jpeg"

        # write payload to DB
        await Photos.insert(**payload)

        # check if store path exist
        complete_path = f"{config.STORE_PATH}/{owner_id}/"
        if not os.path.exists(complete_path):
            os.makedirs(complete_path)

        # save original file
        with open(f"{complete_path}{id}.{file_format}", 'wb+') as f:
            f.write(file_bytes)
            f.close()

        if file_format.lower() == "heic":
            # save resized file
            img.thumbnail((2560, 2560), Image.LANCZOS)
            img.save(f"{complete_path}{id}-resize.jpeg", "jpeg")
            # save thumbnail
            img.thumbnail((512, 512), Image.LANCZOS)
            img.save(f"{complete_path}{id}-thumbnail.jpeg", "jpeg")
        else:
            exif_info = img.info['exif'] if "exif" in img.info else b''
            # save resized file
            img.thumbnail((2560, 2560), Image.LANCZOS)
            img.save(f"{complete_path}{id}-resize.{file_format}",
                     file_format, exif=exif_info)
            # save thumbnail
            img.thumbnail((512, 512), Image.LANCZOS)
            img.save(f"{complete_path}{id}-thumbnail.{file_format}",
                     file_format, exif=exif_info)

        return payload

    @staticmethod
    async def __check_redundant(owner_id, md5):
        return await Photos.check_redundant_file(owner_id, md5)

    @staticmethod
    async def __parse_exif_gps_info(exif):
        local_time = datetime.now()
        if "DateTime" in exif:
            local_time = datetime.strptime(
                exif["DateTime"], "%Y:%m:%d %H:%M:%S")

        # calculate gps coordinate
        latitude, longitude = None, None
        if "GPSInfo" in exif:
            if 1 in exif["GPSInfo"] and 2 in exif["GPSInfo"] and 3 in exif["GPSInfo"] and 4 in exif["GPSInfo"]:
                latitude = float((exif["GPSInfo"][2][0] + exif["GPSInfo"][2][1] /
                                  60 + exif["GPSInfo"][2][2] / 3600) * 1 if exif["GPSInfo"][1] == "N" else -1)
                longitude = float((exif["GPSInfo"][4][0] + exif["GPSInfo"][4][1] /
                                   60 + exif["GPSInfo"][4][2] / 3600) * (1 if exif["GPSInfo"][3] == "E" else -1))

        # calculate utc time based on gps info
        if latitude is not None:
            tf = TimezoneFinder()
            timezone_str = tf.certain_timezone_at(
                lat=latitude, lng=longitude)
            local = pytz.timezone(timezone_str)
            naive = local_time
            local_dt = local.localize(naive, is_dst=None)
            utc_dt = local_dt.astimezone(pytz.utc)
            local_time = datetime.strptime(
                utc_dt.strftime("%Y:%m:%d %H:%M:%S"), "%Y:%m:%d %H:%M:%S")
        return latitude, longitude, int((local_time-datetime(1970, 1, 1)).total_seconds() * 1000)

    @staticmethod
    async def __parse_exif(img):
        img_exif = img._getexif()
        exif = {}
        if img_exif is not None:
            for key, val in img_exif.items():
                if key in ExifTags.TAGS:
                    exif[ExifTags.TAGS[key]] = val
            return exif
        return None

    async def __process_video(self, file, owner_id, data):
        pass
