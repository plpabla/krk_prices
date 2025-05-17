from fastapi import APIRouter, UploadFile, File
from schemas.photo_feedback import PhotoFeedback

router = APIRouter(prefix="")


async def send_file_to_model(file: UploadFile) -> PhotoFeedback:
    # TODO: Implement me
    """
    Simulate sending a file to a model and getting a response.
    In a real-world scenario, this would involve sending the file to a machine learning model
    and receiving the prediction.
    """
    # Simulate processing the file and returning a response
    # In reality, you would send the file to your model here
    return PhotoFeedback(luxury_level=5)  # Example response


@router.post("/upload")
async def upload_photo(file: UploadFile = File(...)) -> PhotoFeedback:
    resp = await send_file_to_model(file)
    return resp
