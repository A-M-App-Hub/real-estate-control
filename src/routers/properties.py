"""
Router para endpoints de imóveis
"""
from fastapi import APIRouter, Query, status
from src.schemas.properties import Property, PropertyCreate, PropertiesListResponse
from src.services.properties_service import get_properties, create_property

router = APIRouter(prefix="/api/v1/properties", tags=["properties"])


@router.get("", response_model=PropertiesListResponse)
def list_properties(
    page: int = Query(1, ge=1, description="Número da página"),
    limit: int = Query(10, ge=1, le=100, description="Limite de itens por página")
) -> PropertiesListResponse:
    """
    Lista imóveis cadastrados com paginação
    
    AC-2.3: Listagem com paginação (query params page e limit)
    RN05: Ordenados por data de cadastro (mais recentes primeiro)
    """
    return get_properties(page=page, limit=limit)


@router.post("", response_model=Property, status_code=status.HTTP_201_CREATED)
def create_new_property(property_data: PropertyCreate) -> Property:
    """
    Cadastra novo imóvel
    
    AC-2.4: Cadastro com validação de campos obrigatórios
    RN04: Campos obrigatórios validados pelo Pydantic
    """
    return create_property(property_data)
