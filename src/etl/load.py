import pandas as pd
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# 1. Carregar variáveis de segurança do ficheiro .env
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    print("❌ Erro: Variável DATABASE_URL não encontrada no ficheiro .env")
    exit()

print("🚀 A iniciar a Carga (Load) para o PostgreSQL na nuvem (Supabase)...")

# 2. Criar o 'Motor' de conexão com o banco de dados
engine = create_engine(DATABASE_URL)

try:
    # 3. Ler os dados limpos da camada PROCESSED
    print("📥 A ler ficheiros Parquet da memória local...")
    df_contas = pd.read_parquet('data/processed/dim_plano_contas.parquet')
    df_budget = pd.read_parquet('data/processed/fact_budget.parquet')
    df_actuals = pd.read_parquet('data/processed/fact_actuals.parquet')

    # 4. Enviar para a Nuvem
    print("☁️ A enviar dados para a nuvem... (Isto pode demorar alguns segundos devido à rede)")
    
    # O if_exists='replace' garante que, se rodarmos o script 2 vezes, ele recria a tabela limpa
    df_contas.to_sql('dim_plano_contas', engine, if_exists='replace', index=False)
    print("✅ Tabela 'dim_plano_contas' carregada com sucesso!")

    df_budget.to_sql('fact_budget', engine, if_exists='replace', index=False)
    print("✅ Tabela 'fact_budget' carregada com sucesso!")

    df_actuals.to_sql('fact_actuals', engine, if_exists='replace', index=False)
    print("✅ Tabela 'fact_actuals' carregada com sucesso!")

    print("🎉 Sprint 3 Concluída! O teu Data Warehouse está vivo no Supabase!")

except Exception as e:
    print(f"❌ Erro durante o processo de carga: {e}")