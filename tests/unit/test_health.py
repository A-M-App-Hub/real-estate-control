"""
Testes unitários para endpoint GET /health
AC-2.5: Endpoint retorna status do backend
"""
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_health_returns_200():
    """Testa que endpoint /health retorna status 200"""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_valid_json():
    """Testa que endpoint retorna JSON válido com campos esperados"""
    response = client.get("/health")
    data = response.json()
    
    assert "status" in data
    assert "timestamp" in data


def test_health_status_is_ok():
    """Testa que status é 'ok'"""
    response = client.get("/health")
    data = response.json()
    
    assert data["status"] == "ok"


def test_health_timestamp_is_valid():
    """Testa que timestamp é uma string não vazia"""
    response = client.get("/health")
    data = response.json()
    
    assert isinstance(data["timestamp"], str)
    assert len(data["timestamp"]) > 0
