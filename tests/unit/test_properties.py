"""
Testes unitários para endpoints de imóveis
AC-2.3: GET /api/v1/properties (listagem com paginação)
AC-2.4: POST /api/v1/properties (cadastro com validação)
"""
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


# ===== Testes GET /api/v1/properties (AC-2.3) =====

def test_get_properties_returns_200():
    """Testa que endpoint GET retorna status 200"""
    response = client.get("/api/v1/properties")
    assert response.status_code == 200


def test_get_properties_returns_paginated_response():
    """Testa que resposta contém campos de paginação"""
    response = client.get("/api/v1/properties")
    data = response.json()
    
    assert "total" in data
    assert "page" in data
    assert "limit" in data
    assert "items" in data


def test_get_properties_pagination_query_params():
    """Testa que paginação funciona com query params page e limit"""
    response = client.get("/api/v1/properties?page=1&limit=5")
    data = response.json()
    
    assert data["page"] == 1
    assert data["limit"] == 5
    assert len(data["items"]) <= 5


def test_get_properties_items_schema():
    """Testa que cada item tem campos esperados"""
    response = client.get("/api/v1/properties")
    data = response.json()
    
    if len(data["items"]) > 0:
        item = data["items"][0]
        assert "id" in item
        assert "proprietario" in item
        assert "endereco" in item
        assert "tipo" in item
        assert "status" in item
        assert "valor_aluguel" in item
        assert "data_cadastro" in item


def test_get_properties_ordered_by_date_desc():
    """Testa que imóveis são ordenados por data de cadastro (mais recentes primeiro)"""
    response = client.get("/api/v1/properties")
    data = response.json()
    
    if len(data["items"]) >= 2:
        # Primeiro item deve ter data >= segundo item (ordem decrescente)
        first_date = data["items"][0]["data_cadastro"]
        second_date = data["items"][1]["data_cadastro"]
        assert first_date >= second_date


# ===== Testes POST /api/v1/properties (AC-2.4) =====

def test_post_property_returns_201_on_success():
    """Testa que endpoint POST retorna 201 Created em caso de sucesso"""
    payload = {
        "proprietario": "João Silva",
        "endereco": "Rua Teste, 123",
        "tipo": "Residencial",
        "status": "Disponível",
        "valor_aluguel": 2500.00
    }
    response = client.post("/api/v1/properties", json=payload)
    assert response.status_code == 201


def test_post_property_returns_created_property():
    """Testa que resposta contém o imóvel criado com ID gerado"""
    payload = {
        "proprietario": "Maria Santos",
        "endereco": "Av. Principal, 456",
        "tipo": "Comercial",
        "status": "Disponível",
        "valor_aluguel": 5000.00
    }
    response = client.post("/api/v1/properties", json=payload)
    data = response.json()
    
    assert "id" in data
    assert data["proprietario"] == payload["proprietario"]
    assert data["endereco"] == payload["endereco"]
    assert data["tipo"] == payload["tipo"]
    assert data["status"] == payload["status"]
    assert data["valor_aluguel"] == payload["valor_aluguel"]
    assert "data_cadastro" in data


def test_post_property_validates_required_fields():
    """Testa que campos obrigatórios são validados (RN04)"""
    # Payload vazio
    response = client.post("/api/v1/properties", json={})
    assert response.status_code == 422  # Unprocessable Entity
    
    # Payload com campo faltando
    payload = {
        "proprietario": "João Silva",
        # falta endereco
        "tipo": "Residencial",
        "status": "Disponível",
        "valor_aluguel": 2500.00
    }
    response = client.post("/api/v1/properties", json=payload)
    assert response.status_code == 422


def test_post_property_validates_valor_aluguel_positive():
    """Testa que valor_aluguel deve ser positivo"""
    payload = {
        "proprietario": "João Silva",
        "endereco": "Rua Teste, 123",
        "tipo": "Residencial",
        "status": "Disponível",
        "valor_aluguel": -100.00  # valor negativo
    }
    response = client.post("/api/v1/properties", json=payload)
    assert response.status_code == 422


def test_post_property_persists_in_memory():
    """Testa que imóvel cadastrado aparece na listagem (persistência em memória)"""
    # Cadastrar novo imóvel
    payload = {
        "proprietario": "Carlos Souza",
        "endereco": "Rua Nova, 789",
        "tipo": "Terreno",
        "status": "Disponível",
        "valor_aluguel": 1500.00
    }
    post_response = client.post("/api/v1/properties", json=payload)
    assert post_response.status_code == 201
    created_id = post_response.json()["id"]
    
    # Verificar que aparece na listagem
    get_response = client.get("/api/v1/properties")
    data = get_response.json()
    
    # Procurar o imóvel criado na lista
    found = any(item["id"] == created_id for item in data["items"])
    assert found, f"Imóvel com ID {created_id} não encontrado na listagem"
