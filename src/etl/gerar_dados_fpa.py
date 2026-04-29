import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Garante que a pasta existe
os.makedirs('data/raw', exist_ok=True)

print("🚀 A iniciar a geração de dados de FP&A (Rede de Restaurantes)...")

# ---------------------------------------------------------
# 1. GERAR DIMENSÃO: PLANO DE CONTAS (Chart of Accounts)
# ---------------------------------------------------------
plano_contas = [
    {'id_conta': 100, 'categoria': 'Receitas', 'subcategoria': 'Vendas Comida'},
    {'id_conta': 101, 'categoria': 'Receitas', 'subcategoria': 'Vendas Bebida'},
    {'id_conta': 200, 'categoria': 'Custos Operacionais', 'subcategoria': 'CMV - Comida'},
    {'id_conta': 201, 'categoria': 'Custos Operacionais', 'subcategoria': 'CMV - Bebida'},
    {'id_conta': 300, 'categoria': 'Despesas com Pessoal', 'subcategoria': 'Salários'},
    {'id_conta': 301, 'categoria': 'Despesas com Pessoal', 'subcategoria': 'Horas Extras'},
    {'id_conta': 400, 'categoria': 'Despesas Gerais', 'subcategoria': 'Marketing e Publicidade'},
    {'id_conta': 401, 'categoria': 'Despesas Gerais', 'subcategoria': 'Renda e Serviços (Água/Luz)'}
]
df_plano_contas = pd.DataFrame(plano_contas)
df_plano_contas.to_csv('data/raw/dim_plano_contas.csv', index=False)
print("✅ dim_plano_contas.csv gerado com sucesso!")

# ---------------------------------------------------------
# 2. GERAR FACTO: ORÇAMENTO (Budget 2023 - Mensal)
# ---------------------------------------------------------
lojas = ['Loja_Centro', 'Loja_Shopping', 'Loja_Aeroporto']
meses_2023 = pd.date_range(start='2023-01-01', end='2023-12-01', freq='MS')

budget_data = []
for loja in lojas:
    for mes in meses_2023:
        for conta in plano_contas:
            # Gerar valores base lógicos para o orçamento
            base_val = random.randint(15000, 30000) if conta['categoria'] == 'Receitas' else random.randint(2000, 8000)
            budget_data.append({
                'mes_ano': mes.strftime('%Y-%m-%d'),
                'loja_id': loja,
                'id_conta': conta['id_conta'],
                'valor_orcado': base_val
            })

df_budget = pd.DataFrame(budget_data)
df_budget.to_csv('data/raw/fact_budget.csv', index=False)
print("✅ fact_budget.csv gerado com sucesso!")

# ---------------------------------------------------------
# 3. GERAR FACTO: REALIZADO (Actuals 2023 - Diário com "Sujeira")
# ---------------------------------------------------------
dias_2023 = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
actuals_data = []

for loja in lojas:
    for dia in dias_2023:
        for conta in plano_contas:
            # Simulamos 1 a 3 transações por dia por conta
            num_transacoes = random.randint(1, 3)
            for _ in range(num_transacoes):
                # O valor real varia em torno do planeado (com alguma aleatoriedade)
                valor_real = round(random.uniform(50, 1200), 2)
                
                # INJEÇÃO DE "CAOS" (Para o teu ETL resolver depois)
                # 5% de probabilidade de a descrição vir Nula
                descricao = f"Transação padrão - {conta['subcategoria']}" if random.random() > 0.05 else np.nan
                
                # 2% de probabilidade de vir um valor negativo errado nas receitas
                if conta['categoria'] == 'Receitas' and random.random() < 0.02:
                    valor_real = valor_real * -1

                actuals_data.append({
                    'data_transacao': dia.strftime('%Y-%m-%d %H:%M:%S'),
                    'loja_id': loja,
                    'id_conta': conta['id_conta'],
                    'valor_realizado': valor_real,
                    'descricao_sistema': descricao
                })

df_actuals = pd.DataFrame(actuals_data)
df_actuals.to_csv('data/raw/fact_actuals.csv', index=False)
print(f"✅ fact_actuals.csv gerado com sucesso! ({len(df_actuals)} registos)")
print("🎉 Sprint 1 - Dados base criados. Estamos prontos para a Engenharia de Dados!")