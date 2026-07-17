"""
Testes unitários para endpoint GET /api/v1/contracts/monthly-stats
AC-2.2: Endpoint retorna dados para gráfico de barras (últimos 12 meses)
"""
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_get_contracts_monthly_stats_returns_200():
    """Testa que endpoint retorna status 200"""
    response = client.get("/api/v1/contracts/monthly-stats")
    assert response.status_code == 200


def test_get_contracts_monthly_stats_returns_valid_json():
    """Testa que endpoint retorna JSON válido com campos esperados"""
    response = client.get("/api/v1/contracts/monthly-stats")
    data = response.json()
    
    assert "months" in data
    assert "quantities" in data


def test_get_contracts_monthly_stats_returns_12_months():
    """Testa que retorna exatamente 12 meses de dados"""
    response = client.get("/api/v1/contracts/monthly-stats")
    data = response.json()
    
    assert len(data["months"]) == 12
    assert len(data["quantities"]) == 12


def test_get_contracts_monthly_stats_months_format():
    """Testa que meses estão no formato correto (ex: Jan/26, Fev/26)"""
    response = client.get("/api/v1/contracts/monthly-stats")
    data = response.json()
    
    # Validar que todos os meses são strings não vazias
    for month in data["months"]:
        assert isinstance(month, str)
        assert len(month) > 0
        # Formato esperado: "Xxx/YY" (3 letras + / + 2 dígitos)
        assert "/" in month


def test_get_contracts_monthly_stats_quantities_are_non_negative():
    """Testa que quantidades são números não negativos"""
    response = client.get("/api/v1/contracts/monthly-stats")
    data = response.json()
    
    for quantity in data["quantities"]:
        assert isinstance(quantity, int)
        assert quantity >= 0


def test_get_contracts_monthly_stats_schema():
    """Testa que schema da resposta está correto"""
    response = client.get("/api/v1/contracts/monthly-stats")
    data = response.json()
    
    # Validar tipos
    assert isinstance(data["months"], list)
    assert isinstance(data["quantities"], list)
    assert all(isinstance(m, str) for m in data["months"])
    assert all(isinstance(q, int) for q in data["quantities"])
