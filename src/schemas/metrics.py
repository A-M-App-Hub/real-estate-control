"""
Schemas Pydantic para métricas do dashboard
"""
from pydantic import BaseModel, Field


class MetricsResponse(BaseModel):
    """Schema para resposta do endpoint GET /api/v1/metrics"""
    receita_alugueis: float = Field(
        ...,
        description="Receita total de aluguéis em R$ (RN01: soma de contratos ativos)",
        ge=0
    )
    taxa_ocupacao: float = Field(
        ...,
        description="Taxa de ocupação em % (RN02: imóveis alugados / total)",
        ge=0,
        le=100
    )
    inadimplencia: float = Field(
        ...,
        description="Taxa de inadimplência em % (RN03: contratos em atraso / total ativos)",
        ge=0,
        le=100
    )
