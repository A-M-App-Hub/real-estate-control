/**
 * Serviços de API - funções para consumir endpoints do backend
 */
import { apiFetch } from '../lib/api';
import type { Metrics, MonthlyStats, PropertiesListResponse, PropertyCreate, Property } from '../types';

export async function getMetrics(): Promise<Metrics> {
  const response = await apiFetch('/metrics');
  if (!response.ok) {
    throw new Error('Erro ao carregar métricas');
  }
  return response.json();
}

export async function getMonthlyStats(): Promise<MonthlyStats> {
  const response = await apiFetch('/contracts/monthly-stats');
  if (!response.ok) {
    throw new Error('Erro ao carregar estatísticas mensais');
  }
  return response.json();
}

export async function getProperties(page: number = 1, limit: number = 10): Promise<PropertiesListResponse> {
  const response = await apiFetch(`/properties?page=${page}&limit=${limit}`);
  if (!response.ok) {
    throw new Error('Erro ao carregar imóveis');
  }
  return response.json();
}

export async function createProperty(data: PropertyCreate): Promise<Property> {
  const response = await apiFetch('/properties', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    throw new Error('Erro ao cadastrar imóvel');
  }
  return response.json();
}
