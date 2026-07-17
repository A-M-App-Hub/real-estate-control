/**
 * Cards de métricas principais (AC-3.1)
 * - Receita de Aluguéis (R$)
 * - Taxa de Ocupação (%)
 * - Inadimplência (%)
 */
import { useEffect, useState } from 'react';
import { getMetrics } from '../services/api';
import type { Metrics } from '../types';

export default function MetricsCards() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadMetrics = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getMetrics();
      setMetrics(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro desconhecido');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMetrics();
  }, []);

  if (loading) {
    return (
      <div className="metrics-cards">
        <div className="card skeleton">Carregando...</div>
        <div className="card skeleton">Carregando...</div>
        <div className="card skeleton">Carregando...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="metrics-cards">
        <div className="card error">
          <p>Erro ao carregar métricas</p>
          <button onClick={loadMetrics}>Tentar novamente</button>
        </div>
      </div>
    );
  }

  if (!metrics) return null;

  return (
    <div className="metrics-cards">
      <div className="card card-receita">
        <div className="card-icon">💰</div>
        <div className="card-content">
          <h3>Receita de Aluguéis</h3>
          <p className="card-value">
            R$ {metrics.receita_alugueis.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
          </p>
        </div>
      </div>

      <div className="card card-ocupacao">
        <div className="card-icon">🏠</div>
        <div className="card-content">
          <h3>Taxa de Ocupação</h3>
          <p className="card-value">{metrics.taxa_ocupacao.toFixed(1)}%</p>
        </div>
      </div>

      <div className="card card-inadimplencia">
        <div className="card-icon">⚠️</div>
        <div className="card-content">
          <h3>Inadimplência</h3>
          <p className="card-value">{metrics.inadimplencia.toFixed(1)}%</p>
        </div>
      </div>
    </div>
  );
}
