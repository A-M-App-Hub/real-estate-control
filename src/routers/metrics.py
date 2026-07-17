"""
Router para endpoints de métricas
"""
from fastapi import APIRouter
from src.schemas.metrics import MetricsResponse
from src.services.metrics_service import get_metrics

router = APIRouter(prefix="/api/v1", tags=["metrics"])


@router.get("/metrics", response_model=MetricsResponse)
def get_dashboard_metrics() -> MetricsResponse:
    """
    Retorna métricas principais do dashboard
    
    AC-2.1: Receita de aluguéis, taxa de ocupação e inadimplência
    """
    return get_metrics()
