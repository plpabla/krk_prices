from fastapi import APIRouter, UploadFile, File

router = APIRouter(prefix="")


@router.post("/upload")
async def upload_photo(file: UploadFile = File(...)):
    # TODO: Implement me
    # For demo purposes, just return the filename
    return {"filename": file.filename}
