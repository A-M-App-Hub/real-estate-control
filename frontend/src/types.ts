/**
 * Tipos TypeScript para dados da aplicação
 */

export interface Metrics {
  receita_alugueis: number;
  taxa_ocupacao: number;
  inadimplencia: number;
}

export interface MonthlyStats {
  months: string[];
  quantities: number[];
}

export interface Property {
  id: string;
  proprietario: string;
  endereco: string;
  tipo: string;
  status: string;
  valor_aluguel: number;
  data_cadastro: string;
}

export interface PropertiesListResponse {
  total: number;
  page: number;
  limit: number;
  items: Property[];
}

export interface PropertyCreate {
  proprietario: string;
  endereco: string;
  tipo: string;
  status: string;
  valor_aluguel: number;
}
