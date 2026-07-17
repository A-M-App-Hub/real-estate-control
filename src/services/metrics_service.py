"""
Serviço para cálculo de métricas do dashboard
MVP: dados mockados em memória
"""
from src.schemas.metrics import MetricsResponse


def get_metrics() -> MetricsResponse:
    """
    Retorna métricas do dashboard (mockadas para MVP)
    
    RN01: Receita = soma de contratos ativos
    RN02: Taxa de Ocupação = (imóveis alugados / total) * 100
    RN03: Inadimplência = (contratos em atraso / total ativos) * 100
    """
    # Dados mockados realistas
    return MetricsResponse(
        receita_alugueis=125000.00,  # R$ 125k/mês
        taxa_ocupacao=85.5,           # 85.5% ocupação
        inadimplencia=3.2             # 3.2% inadimplência
    )
