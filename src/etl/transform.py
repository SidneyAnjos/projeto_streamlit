import pandas as pd
import numpy as np
import os, sys

os.makedirs('data/processed', exist_ok=True)

print("Iniciando a extração de dados da RAW para a memória...")

# 1 - Carregamento dos dados
try:
    df_contas = pd.read_csv('data/raw/dim_plano_contas.csv')
    df_budget = pd.read_csv('data/raw/fact_budget.csv')
    df_actuals = pd.read_csv('data/raw/fact_actuals.csv')
    print("Dados brutos carregados na memória com sucesso!")
except FileNotFoundError as e:
    print(f"Erro: procura de arquivos {e}") 
    exit()

# 2 - Transformação agora
print("Iniciando a transformação dos dados...")

# Regra A: Tratar valores nulos na descrição
# Cuidado para usar o nome exato da coluna para sobrescrevê-la
df_actuals['descricao_sistema'] = df_actuals['descricao_sistema'].fillna('Descrição Indisponível')

# Regra B: Corrigir os valores negativos nas Receitas
df_actuals = df_actuals.merge(df_contas[['id_conta', 'categoria']], on="id_conta", how='left')

# Atenção ao 'valor_realizado' todo minúsculo
mask_receitas_negativas = (df_actuals['categoria'] == 'Receitas') & (df_actuals['valor_realizado'] < 0)

# Aplicando o valor absoluto na coluna correta
df_actuals.loc[mask_receitas_negativas, 'valor_realizado'] = df_actuals.loc[mask_receitas_negativas, 'valor_realizado'].abs()

# Regra C: Removida a coluna 'categoria', pertence a dimensão não à tabela factos
df_actuals = df_actuals.drop(columns=['categoria'])

# Regra D: Conversão de Datas
df_actuals['data_transacao'] = pd.to_datetime(df_actuals['data_transacao'])
df_budget['mes_ano'] = pd.to_datetime(df_budget['mes_ano'])

# 3 - Carrega os dados (GUARDA NA CAMADA PROCESSED EM PARQUET)
df_contas.to_parquet('data/processed/dim_plano_contas.parquet', index=False)
df_budget.to_parquet('data/processed/fact_budget.parquet', index=False)
df_actuals.to_parquet('data/processed/fact_actuals.parquet', index=False)

print("Transformação feita. Arquivos guardados em 'data/processed/' no formato Parquet.")