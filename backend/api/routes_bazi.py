"""八字计算 API"""
from fastapi import APIRouter
from backend.models.schemas import BaziRequest, BaziResponse
from backend.core.bazi_calculator import BaziCalculator

router = APIRouter(prefix="/api/bazi", tags=["bazi"])


@router.post("/calculate", response_model=BaziResponse)
async def calculate_bazi(request: BaziRequest):
    calculator = BaziCalculator(request.year, request.month, request.day, request.hour)
    fortune = calculator.get_fortune_base()
    traits = calculator.get_personality_traits()

    return BaziResponse(
        bazi=fortune["八字"],
        wuxing=fortune["五行"],
        strongest=fortune["最强五行"],
        weakest=fortune["最弱五行"],
        zodiac=fortune["生肖"],
        constellation=fortune["星座"],
        personality_traits=traits,
    )
