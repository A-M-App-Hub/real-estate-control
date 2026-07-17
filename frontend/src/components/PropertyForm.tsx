/**
 * Formulário de cadastro de imóvel (AC-3.4)
 * Validação de campos obrigatórios e feedback visual
 */
import { useState, FormEvent } from 'react';
import { createProperty } from '../services/api';
import type { PropertyCreate } from '../types';

interface PropertyFormProps {
  onSuccess?: () => void;
}

export default function PropertyForm({ onSuccess }: PropertyFormProps) {
  const [formData, setFormData] = useState<PropertyCreate>({
    proprietario: '',
    endereco: '',
    tipo: 'Residencial',
    status: 'Disponível',
    valor_aluguel: 0,
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [submitting, setSubmitting] = useState(false);
  const [toast, setToast] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.proprietario.trim()) {
      newErrors.proprietario = 'Proprietário é obrigatório';
    }
    if (!formData.endereco.trim()) {
      newErrors.endereco = 'Endereço é obrigatório';
    }
    if (formData.valor_aluguel <= 0) {
      newErrors.valor_aluguel = 'Valor deve ser maior que zero';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    if (!validate()) {
      return;
    }

    try {
      setSubmitting(true);
      await createProperty(formData);
      
      // Sucesso
      setToast({ type: 'success', message: 'Imóvel cadastrado com sucesso!' });
      
      // Limpar formulário
      setFormData({
        proprietario: '',
        endereco: '',
        tipo: 'Residencial',
        status: 'Disponível',
        valor_aluguel: 0,
      });
      setErrors({});

      // Notificar componente pai
      if (onSuccess) {
        onSuccess();
      }

      // Remover toast após 3s
      setTimeout(() => setToast(null), 3000);
    } catch (err) {
      setToast({ 
        type: 'error', 
        message: err instanceof Error ? err.message : 'Erro ao cadastrar imóvel.' 
      });
      setTimeout(() => setToast(null), 3000);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="form-container">
      <h2>Cadastrar Novo Imóvel</h2>
      
      {toast && (
        <div className={`toast toast-${toast.type}`}>
          {toast.message}
        </div>
      )}

      <form onSubmit={handleSubmit} className="property-form">
        <div className="form-group">
          <label htmlFor="proprietario">Proprietário *</label>
          <input
            id="proprietario"
            type="text"
            value={formData.proprietario}
            onChange={(e) => setFormData({ ...formData, proprietario: e.target.value })}
            className={errors.proprietario ? 'error' : ''}
          />
          {errors.proprietario && <span className="error-message">{errors.proprietario}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="endereco">Endereço *</label>
          <input
            id="endereco"
            type="text"
            value={formData.endereco}
            onChange={(e) => setFormData({ ...formData, endereco: e.target.value })}
            className={errors.endereco ? 'error' : ''}
          />
          {errors.endereco && <span className="error-message">{errors.endereco}</span>}
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="tipo">Tipo *</label>
            <select
              id="tipo"
              value={formData.tipo}
              onChange={(e) => setFormData({ ...formData, tipo: e.target.value })}
            >
              <option value="Residencial">Residencial</option>
              <option value="Comercial">Comercial</option>
              <option value="Terreno">Terreno</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="status">Status Inicial *</label>
            <select
              id="status"
              value={formData.status}
              onChange={(e) => setFormData({ ...formData, status: e.target.value })}
            >
              <option value="Disponível">Disponível</option>
              <option value="Em Manutenção">Em Manutenção</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="valor_aluguel">Valor Sugerido de Aluguel (R$) *</label>
            <input
              id="valor_aluguel"
              type="number"
              step="0.01"
              min="0"
              value={formData.valor_aluguel}
              onChange={(e) => setFormData({ ...formData, valor_aluguel: parseFloat(e.target.value) || 0 })}
              className={errors.valor_aluguel ? 'error' : ''}
            />
            {errors.valor_aluguel && <span className="error-message">{errors.valor_aluguel}</span>}
          </div>
        </div>

        <button type="submit" className="btn-primary" disabled={submitting}>
          {submitting ? 'Cadastrando...' : 'Cadastrar'}
        </button>
      </form>
    </div>
  );
}
