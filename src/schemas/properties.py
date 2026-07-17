"""
Schemas Pydantic para imóveis
"""
from datetime import datetime
from pydantic import BaseModel, Field


class PropertyBase(BaseModel):
    """Campos base de um imóvel"""
    proprietario: str = Field(..., min_length=1, description="Nome do proprietário")
    endereco: str = Field(..., min_length=1, description="Endereço completo do imóvel")
    tipo: str = Field(..., description="Tipo do imóvel (Residencial, Comercial, Terreno)")
    status: str = Field(..., description="Status do imóvel (Disponível, Alugado, Em Manutenção)")
    valor_aluguel: float = Field(..., gt=0, description="Valor sugerido de aluguel em R$")


class PropertyCreate(PropertyBase):
    """Schema para criação de imóvel (POST request)"""
    pass


class Property(PropertyBase):
    """Schema completo de imóvel (com ID e data de cadastro)"""
    id: str = Field(..., description="ID único do imóvel")
    data_cadastro: datetime = Field(..., description="Data e hora de cadastro")

    class Config:
        from_attributes = True


class PropertiesListResponse(BaseModel):
    """Schema para resposta paginada de listagem de imóveis"""
    total: int = Field(..., ge=0, description="Total de imóveis cadastrados")
    page: int = Field(..., ge=1, description="Página atual")
    limit: int = Field(..., ge=1, description="Limite de itens por página")
    items: list[Property] = Field(..., description="Lista de imóveis")
