from fastapi import APIRouter, UploadFile, File, Form
import base64

from schemas.photo_feedback import PhotoFeedback
from model.GPT import analyze_apartment_photos
import asyncio

router = APIRouter(prefix="")


async def send_files_to_model(
    file: list[UploadFile], form_data: str = ""
) -> PhotoFeedback:
    async def read_file(f):
        return await f.read()

    photos = await asyncio.gather(*(read_file(f) for f in file))

    photos_base64 = [base64.b64encode(photo).decode("utf-8") for photo in photos]
    resp = {
        "attractiveness_level": 0,
    }
    try:
        resp = analyze_apartment_photos(photos_base64, form_data)
        print(">>>", resp)
    except Exception:
        # we'll return default response
        pass

    return PhotoFeedback(
        attractiveness_level=resp["attractiveness_level"],
        pros=resp["pros"],
        to_fix=resp["to_fix"],
        description=resp["description"],
    )


@router.post("/upload")
async def upload_photo(
    files: list[UploadFile] = File(default=None),
    parameters: str = Form(""),
) -> PhotoFeedback:
    files = files or []
    resp = await send_files_to_model(files, parameters)
    return resp
