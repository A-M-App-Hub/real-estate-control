"""
Serviço para dados de contratos
MVP: dados mockados em memória
"""
from datetime import datetime, timedelta
from src.schemas.contracts import MonthlyStatsResponse


def get_monthly_stats() -> MonthlyStatsResponse:
    """
    Retorna estatísticas mensais de novos contratos (últimos 12 meses)
    
    Dados mockados para MVP - gráfico de barras
    """
    # Gerar últimos 12 meses (de hoje para trás)
    months = []
    quantities = []
    
    # Mapeamento de meses em português
    month_names = {
        1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
        7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez"
    }
    
    current_date = datetime.now()
    
    # Gerar últimos 12 meses
    for i in range(11, -1, -1):
        month_date = current_date - timedelta(days=30 * i)
        month_str = f"{month_names[month_date.month]}/{str(month_date.year)[2:]}"
        months.append(month_str)
    
    # Dados mockados realistas (variação entre 5-15 contratos/mês)
    quantities = [8, 12, 10, 7, 15, 9, 11, 13, 8, 14, 10, 12]
    
    return MonthlyStatsResponse(
        months=months,
        quantities=quantities
    )
