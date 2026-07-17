"""
Schemas Pydantic para contratos
"""
from pydantic import BaseModel, Field


class MonthlyStatsResponse(BaseModel):
    """Schema para resposta do endpoint GET /api/v1/contracts/monthly-stats"""
    months: list[str] = Field(
        ...,
        description="Lista de meses no formato 'Xxx/YY' (ex: Jan/26, Fev/26)",
        min_length=12,
        max_length=12
    )
    quantities: list[int] = Field(
        ...,
        description="Lista de quantidades de novos contratos por mês",
        min_length=12,
        max_length=12
    )
