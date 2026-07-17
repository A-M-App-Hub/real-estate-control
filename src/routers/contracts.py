"""
Router para endpoints de contratos
"""
from fastapi import APIRouter
from src.schemas.contracts import MonthlyStatsResponse
from src.services.contracts_service import get_monthly_stats

router = APIRouter(prefix="/api/v1/contracts", tags=["contracts"])


@router.get("/monthly-stats", response_model=MonthlyStatsResponse)
def get_contracts_monthly_stats() -> MonthlyStatsResponse:
    """
    Retorna estatísticas mensais de novos contratos (últimos 12 meses)
    
    AC-2.2: Dados para gráfico de barras
    """
    return get_monthly_stats()
