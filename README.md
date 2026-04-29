content = """# 📊 FP&A Dashboard - Rede de Restaurantes

Este projeto é uma solução de Engenharia de Dados de ponta a ponta (End-to-End) para análise financeira (FP&A) de uma rede de restaurantes. Ele simula o fluxo completo desde a geração de dados brutos de um sistema ERP até a visualização analítica em um dashboard interativo na nuvem.

## 🚀 Link do Projeto
Acesse o dashboard online: [FP&A Dashboard](https://projetoapp-fk874pnux3jepaxjacgria.streamlit.app/)

---

## 🛠️ Stack Técnica

O projeto foi construído utilizando as ferramentas mais modernas do mercado de dados:

* **Linguagem:** Python 3.14 / 3.10
* **Manipulação de Dados:** Pandas & NumPy
* **Armazenamento de Alta Performance:** Apache Parquet (camada processed)
* **Banco de Dados (Data Warehouse):** PostgreSQL (alojado no **Supabase**)
* **ORM e Conectividade:** SQLAlchemy & Psycopg2
* **Interface e Visualização:** Streamlit
* **Segurança e Infraestrutura:** Dotenv (Gestão de segredos), WSL2 (Ambiente Linux), Git & GitHub
* **Deploy:** Streamlit Community Cloud

---

## 📐 Arquitetura e Pipeline (ETL)

O projeto segue a arquitetura clássica de pipelines de dados:

1.  **Extract (Geração & Extração):** * Um script customizado gera transações financeiras realistas em formato CSV.
    * Os dados são lidos da camada `data/raw`.
2.  **Transform (Transformação & Limpeza):** * Utilização de **Pandas** para limpeza (tratamento de valores nulos e correção de lógica de negócio).
    * Conversão para formato **Parquet**, reduzindo o tamanho dos arquivos e preservando a tipagem.
3.  **Load (Carga):** * Carga dos dados otimizada para o **Supabase** através de um **Connection Pooler (IPv4)** para garantir estabilidade em conexões via WSL2.
4.  **Analytics (Dashboard):**
    * Conexão direta ao Data Warehouse.
    * Uso de **Caching** (`@st.cache_data`) para performance.
    * Cálculo de KPIs financeiros (Receita, Custos, Lucro Operacional).

---

## 📂 Estrutura do Projeto

```text
projeto_streamlit/
├── app/
│   └── dashboard.py       # Aplicação Streamlit
├── data/
│   ├── raw/               # CSVs Brutos
│   └── processed/         # Arquivos Parquet Limpos
├── src/
│   ├── etl/
│   │   ├── transform.py   # Lógica de limpeza e transformação
│   │   └── load.py        # Script de carga para o Supabase
│   └── utils/
│       └── gerar_dados.py # Gerador de dados fictícios
├── .env                   # Variáveis de ambiente (Segredos)
├── .gitignore             # Proteção de arquivos sensíveis
├── README.md              # Documentação do projeto
└── requirements.txt       # Dependências do Python
```

🔒 Segurança
Este projeto aplica as melhores práticas de SecOps:

Gestão de Segredos: Credenciais de banco de dados nunca são expostas no código, sendo gerenciadas via variáveis de ambiente.

Row Level Security (RLS): Tabelas no Supabase com segurança em nível de linha ativada para impedir acessos não autorizados via API pública.

Connection Pooling: Uso de túnel seguro via porta 6543 para comunicação com o banco de dados.

👨‍💻 Autor
Projeto desenvolvido como parte do desafio técnico de Engenharia de Dados.
"""
