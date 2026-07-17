/**
 * Tabela de imóveis com paginação (AC-3.3)
 */
import { useEffect, useState } from 'react';
import { getProperties } from '../services/api';
import type { PropertiesListResponse } from '../types';

interface PropertiesTableProps {
  refresh?: number; // Trigger para recarregar
}

export default function PropertiesTable({ refresh }: PropertiesTableProps) {
  const [data, setData] = useState<PropertiesListResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const limit = 10;

  const loadProperties = async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await getProperties(page, limit);
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erro desconhecido');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProperties();
  }, [page, refresh]);

  if (loading) {
    return (
      <div className="table-container">
        <h2>Imóveis Cadastrados</h2>
        <div className="skeleton-table">Carregando tabela...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="table-container">
        <h2>Imóveis Cadastrados</h2>
        <div className="error">
          <p>{error}</p>
          <button onClick={loadProperties}>Tentar novamente</button>
        </div>
      </div>
    );
  }

  if (!data || data.items.length === 0) {
    return (
      <div className="table-container">
        <h2>Imóveis Cadastrados</h2>
        <div className="empty-state">
          <p>Nenhum imóvel cadastrado.</p>
          <p>Cadastre o primeiro imóvel usando o formulário acima.</p>
        </div>
      </div>
    );
  }

  const totalPages = Math.ceil(data.total / limit);

  return (
    <div className="table-container">
      <h2>Imóveis Cadastrados ({data.total})</h2>
      <table className="properties-table">
        <thead>
          <tr>
            <th>Endereço/Código</th>
            <th>Tipo</th>
            <th>Status</th>
            <th>Valor Aluguel</th>
          </tr>
        </thead>
        <tbody>
          {data.items.map((property) => (
            <tr key={property.id}>
              <td>{property.endereco}</td>
              <td>
                <span className={`badge badge-${property.tipo.toLowerCase()}`}>
                  {property.tipo}
                </span>
              </td>
              <td>
                <span className={`badge badge-status-${property.status.toLowerCase().replace(' ', '-')}`}>
                  {property.status}
                </span>
              </td>
              <td>R$ {property.valor_aluguel.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {totalPages > 1 && (
        <div className="pagination">
          <button
            onClick={() => setPage(p => Math.max(1, p - 1))}
            disabled={page === 1}
          >
            ← Anterior
          </button>
          <span>Página {page} de {totalPages}</span>
          <button
            onClick={() => setPage(p => Math.min(totalPages, p + 1))}
            disabled={page === totalPages}
          >
            Próxima →
          </button>
        </div>
      )}
    </div>
  );
}
