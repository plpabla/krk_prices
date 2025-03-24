from fastapi import APIRouter

router = APIRouter(prefix="/api")


@router.post("/estimate")
async def get_estimate():
    return {"Price": 400_000}
