import streamlit as st
import pandas as pd
import os, sys
from sqlalchemy import create_engine
from dotenv import load_dotenv

# 1 Configuracao basica da pagina
st.set_page_config(page_title="FP&A Dashaboard", layout="wide", page_icon="📊")
st.title("FP&A Dashboard")
st.markdown("---")

# 2. Conexao segura com o DB
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

@st.cache_data(ttl=3600) #Mantem os dados em cache por 3600 s = 1h
def load_data_from_dw():
    engine = create_engine(DATABASE_URL)
    #Puxando as tabelas actuals, budget e contas
    df_actuals = pd.read_sql("SELECT * FROM fact_actuals", engine)
    df_budget = pd.read_sql("SELECT * FROM fact_budget", engine)
    df_contas = pd.read_sql("SELECT * FROM dim_plano_contas", engine)
    return df_actuals, df_budget, df_contas

try: 
    with st.spinner('A conectar aos DataWarehouse...'):
        df_actuals, df_budget, df_contas = load_data_from_dw()
    #3 - Join com dimensão
    df_actuals_completo = df_actuals.merge(df_contas, on='id_conta', how='left')

    #4 - calcula kpis 
    # #usei o .loc para filtrar e selecioanr coluna, e beleza visual do codigo
    receita_total = df_actuals_completo.loc[df_actuals_completo['categoria']== 'Receitas','valor_realizado'].sum()
    custo_total = df_actuals_completo.loc[df_actuals_completo['categoria'] != 'Custos','valor_realizado'].sum()
    lucro_operacional = receita_total - custo_total

    # 5 - Exibicao visual
    st.subheader("Indicadores Globais (YTD)")
    col1, col2, col3 = st.columns(3)

    col1.metric("Receita total (Realizado)", f"€ {receita_total:,.2f}")
    col2.metric("Custos Operacionais", f"€ {custo_total:,.2f}", delta="- (Atenção)", delta_color="inverse")
    col3.metric("Lucro Operacional", f"€ {lucro_operacional:,.2f}")

    st.markdown("---")

    #6 - Dados e filtros
    st.subheader("Extrato de transações e filtros")

    lojas = df_actuals_completo['loja_id'].unique()
    lojas_selecionada = st.selectbox("Selecione a loja para Análise", ["Todas"] + list(lojas))

    if lojas_selecionada != "Todas":
        # .loc para filtrar linha e coluna e beleza visual do codigo
        df_filtrado = df_actuals_completo.loc[df_actuals_completo['loja_id'] == lojas_selecionada]
    else:
        df_filtrado = df_actuals_completo

    st.dataframe(df_filtrado.sort_values(by='data_transacao', ascending=False).head(100), use_container_width=True)
except Exception as e:
    st.error(f"Erro crítico ao conectar o DB ou processar a visualização: {e}")
    st.exception(e)
