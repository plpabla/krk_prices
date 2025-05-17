from fastapi import APIRouter, UploadFile, File
import base64

from schemas.photo_feedback import PhotoFeedback
from model.GPT import analyze_apartment_photos

router = APIRouter(prefix="")


async def send_file_to_model(file: UploadFile) -> PhotoFeedback:
    photo = await file.read()
    photo_base64 = base64.b64encode(photo).decode("utf-8")
    resp = {
        "luxury_level": 0,
    }
    try:
        resp = analyze_apartment_photos([photo_base64])
    except Exception:
        # we'll return default response
        pass

    return PhotoFeedback(luxury_level=resp["luxury_level"])  # Example response


@router.post("/upload")
async def upload_photo(file: UploadFile = File(...)) -> PhotoFeedback:
    resp = await send_file_to_model(file)
    return resp
