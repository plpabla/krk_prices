from fastapi import APIRouter

from schemas.estimate import EstimateInput, EstimateOutput
from model import model

router = APIRouter(prefix="")


@router.post("/estimate")
async def get_estimate(data: EstimateInput) -> EstimateOutput:
    print(data)
    estimate_price = int(model.predict(data) / 1000) * 1000
    print(estimate_price)
    estimate = EstimateOutput.model_validate({"price": estimate_price})
    return estimate
