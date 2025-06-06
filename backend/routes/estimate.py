from fastapi import APIRouter

from schemas.estimate import EstimateInput, EstimateOutput
from model import model
from fastapi import HTTPException

router = APIRouter(prefix="")


@router.post("/estimate")
async def get_estimate(data: EstimateInput) -> EstimateOutput:
    print(data)
    try:
        estimate_price = int(model.predict(data) / 1000) * 1000
    except Exception as e:
        print(f"Error during prediction: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    print(estimate_price)
    estimate = EstimateOutput.model_validate({"price": estimate_price})
    return estimate
