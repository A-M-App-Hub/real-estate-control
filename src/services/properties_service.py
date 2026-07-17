"""
Serviço para gestão de imóveis
MVP: persistência em memória (lista Python)
"""
from datetime import datetime, timezone
from uuid import uuid4
from src.schemas.properties import Property, PropertyCreate, PropertiesListResponse


# Armazenamento em memória (MVP)
_properties_db: list[Property] = []


def _generate_mock_properties():
    """Gera alguns imóveis mockados para demonstração"""
    mock_data = [
        {
            "id": str(uuid4()),
            "proprietario": "João Silva",
            "endereco": "Rua das Flores, 123 - Centro",
            "tipo": "Residencial",
            "status": "Alugado",
            "valor_aluguel": 2500.00,
            "data_cadastro": datetime(2024, 1, 15, 10, 30, tzinfo=timezone.utc)
        },
        {
            "id": str(uuid4()),
            "proprietario": "Maria Santos",
            "endereco": "Av. Principal, 456 - Sala 201",
            "tipo": "Comercial",
            "status": "Disponível",
            "valor_aluguel": 5000.00,
            "data_cadastro": datetime(2024, 2, 20, 14, 15, tzinfo=timezone.utc)
        },
        {
            "id": str(uuid4()),
            "proprietario": "Carlos Souza",
            "endereco": "Rua Nova, 789",
            "tipo": "Terreno",
            "status": "Disponível",
            "valor_aluguel": 1500.00,
            "data_cadastro": datetime(2024, 3, 10, 9, 0, tzinfo=timezone.utc)
        },
    ]
    
    for data in mock_data:
        _properties_db.append(Property(**data))


# Inicializar com dados mockados
_generate_mock_properties()


def get_properties(page: int = 1, limit: int = 10) -> PropertiesListResponse:
    """
    Retorna lista paginada de imóveis
    
    RN05: Ordenados por data de cadastro (mais recentes primeiro)
    """
    # Ordenar por data de cadastro (decrescente)
    sorted_properties = sorted(
        _properties_db,
        key=lambda p: p.data_cadastro,
        reverse=True
    )
    
    # Calcular paginação
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_items = sorted_properties[start_idx:end_idx]
    
    return PropertiesListResponse(
        total=len(_properties_db),
        page=page,
        limit=limit,
        items=paginated_items
    )


def create_property(property_data: PropertyCreate) -> Property:
    """
    Cria novo imóvel
    
    RN04: Valida campos obrigatórios (feito pelo Pydantic)
    """
    new_property = Property(
        id=str(uuid4()),
        **property_data.model_dump(),
        data_cadastro=datetime.now(timezone.utc)
    )
    
    _properties_db.append(new_property)
    
    return new_property
