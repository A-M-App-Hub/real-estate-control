"""
Testes unitários para endpoint GET /api/v1/metrics
AC-2.1: Endpoint retorna receita, taxa de ocupação e inadimplência (dados mockados)
"""
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_get_metrics_returns_200():
    """Testa que endpoint /api/v1/metrics retorna status 200"""
    response = client.get("/api/v1/metrics")
    assert response.status_code == 200


def test_get_metrics_returns_valid_json():
    """Testa que endpoint retorna JSON válido com campos esperados"""
    response = client.get("/api/v1/metrics")
    data = response.json()
    
    assert "receita_alugueis" in data
    assert "taxa_ocupacao" in data
    assert "inadimplencia" in data


def test_get_metrics_returns_realistic_values():
    """Testa que valores retornados são realistas (não negativos, percentuais entre 0-100)"""
    response = client.get("/api/v1/metrics")
    data = response.json()
    
    # Receita deve ser número positivo
    assert isinstance(data["receita_alugueis"], (int, float))
    assert data["receita_alugueis"] >= 0
    
    # Taxa de ocupação deve ser percentual (0-100)
    assert isinstance(data["taxa_ocupacao"], (int, float))
    assert 0 <= data["taxa_ocupacao"] <= 100
    
    # Inadimplência deve ser percentual (0-100)
    assert isinstance(data["inadimplencia"], (int, float))
    assert 0 <= data["inadimplencia"] <= 100


def test_get_metrics_schema():
    """Testa que schema da resposta está correto (tipos de dados)"""
    response = client.get("/api/v1/metrics")
    data = response.json()
    
    # Validar tipos
    assert isinstance(data["receita_alugueis"], (int, float))
    assert isinstance(data["taxa_ocupacao"], (int, float))
    assert isinstance(data["inadimplencia"], (int, float))
