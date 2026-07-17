/**
 * Dashboard de Gestão Imobiliária - Componente Principal
 * AC-3.5: Header/Topbar com logo e título
 */
import { useState } from 'react';
import MetricsCards from './components/MetricsCards';
import ContractsChart from './components/ContractsChart';
import PropertiesTable from './components/PropertiesTable';
import PropertyForm from './components/PropertyForm';
import './App.css';

export default function App() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handlePropertyCreated = () => {
    // Trigger para recarregar tabela após cadastro
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <div className="logo">A&M</div>
          <h1>Dashboard de Gestão Imobiliária</h1>
          <div className="user-info">
            <span>👤 Usuário</span>
          </div>
        </div>
      </header>

      <main className="main-content">
        <section className="metrics-section">
          <MetricsCards />
        </section>

        <section className="chart-section">
          <ContractsChart />
        </section>

        <section className="form-section">
          <PropertyForm onSuccess={handlePropertyCreated} />
        </section>

        <section className="table-section">
          <PropertiesTable refresh={refreshTrigger} />
        </section>
      </main>
    </div>
  );
}
