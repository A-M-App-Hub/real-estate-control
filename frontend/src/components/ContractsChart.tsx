/**
 * Gráfico de barras de novos contratos por mês (AC-3.2)
 * Usa Recharts para visualização
 */
import { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { getMonthlyStats } from '../services/api';
import type { MonthlyStats } from '../types';

export default function ContractsChart() {
  const [stats, setStats] = useState<MonthlyStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadStats = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getMonthlyStats();
      setStats(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro desconhecido');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStats();
  }, []);

  if (loading) {
    return (
      <div className="chart-container">
        <h2>Novos Contratos por Mês</h2>
        <div className="skeleton-chart">Carregando gráfico...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="chart-container">
        <h2>Novos Contratos por Mês</h2>
        <div className="error">
          <p>{error}</p>
          <button onClick={loadStats}>Tentar novamente</button>
        </div>
      </div>
    );
  }

  if (!stats) return null;

  // Transformar dados para formato do Recharts
  const chartData = stats.months.map((month, index) => ({
    month,
    quantity: stats.quantities[index],
  }));

  return (
    <div className="chart-container">
      <h2>Novos Contratos por Mês</h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="quantity" fill="#4CAF50" name="Contratos" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
