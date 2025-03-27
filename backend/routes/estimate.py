from fastapi import APIRouter

from schemas.estimate import EstimateInput, EstimateOutput

router = APIRouter(prefix="")


@router.post("/estimate")
async def get_estimate(data: EstimateInput) -> EstimateOutput:
    print(data)
    estimate = EstimateOutput.model_validate({"price": 123_456})
    return estimate
