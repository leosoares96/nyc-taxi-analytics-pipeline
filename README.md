# 🚕 NYC Taxi Analytics Pipeline

Projeto de análise exploratória e visualização de dados de corridas de táxi em Nova York, utilizando o dataset público do Kaggle:

📦 https://www.kaggle.com/datasets/elemento/nyc-yellow-taxi-trip-data

O projeto realiza processamento de dados, agregações e construção de um dashboard interativo em Streamlit para análise de padrões de mobilidade urbana.

---

# 📊 Objetivo do Projeto

O objetivo é transformar dados brutos de corridas de táxi em insights acionáveis, permitindo:

- Análise de demanda ao longo do tempo
- Identificação de padrões por dia e semana
- Avaliação de comportamento por passageiros
- Distribuição de pagamentos
- Rotas mais frequentes

---

# 🧠 Problema de Negócio

Como entender o comportamento das corridas de táxi em NYC para responder perguntas como:

- Quando a demanda é maior?
- Existe sazonalidade diária ou semanal?
- Quais padrões de pagamento predominam?
- Quais rotas são mais frequentes?
- Como os dados se comportam por segmento?

---

# 🏗️ Arquitetura do Projeto

```
nyc-taxi-analytics-pipeline/
│
├── app/ # Dashboard Streamlit
│ └── app.py
│
├── data/
│ ├── raw/ # Dados originais do Kaggle
│ └── processed/ # Dados tratados e agregados
│
├── src/ # Scripts de processamento
│
├── main.py # Pipeline principal
├── requirements.txt # Dependências
└── .gitignore
```

---

# ⚙️ Pipeline de Dados

O fluxo do projeto segue as etapas:

### 1. Ingestão

- Download dos dados do Kaggle
- Armazenamento em `data/raw`

### 2. Processamento

- Limpeza de dados
- Conversão de tipos (datas, valores numéricos)
- Tratamento de inconsistências

### 3. Agregações (features analíticas)

Geração de datasets derivados:

- `by_passenger` → análise por número de passageiros
- `by_day` → tendência diária
- `by_week` → agregação semanal
- `by_shift_payment` → análise por forma de pagamento e turno
- `by_route_top100` → top 100 rotas mais frequentes

---

# 📈 Dashboard (Streamlit)

O dashboard interativo permite:

### 📊 KPIs

- Total de corridas/valor
- Média por métrica
- Máximo e mínimo

### 📅 Análise temporal

- Tendência diária
- Crescimento ou queda ao longo do tempo

### 📦 Distribuição

- Segmentação por categoria
- Concentração de volume

### 🧠 Insights automáticos

- Detecção de variabilidade
- Assimetria de distribuição
- Padrões relevantes dos dados

# 🖥️ Interface do Dashboard

O dashboard foi desenvolvido em Streamlit com foco em:

- UX simples e intuitiva
- Layout moderno estilo BI
- Cards de indicadores (KPIs)
- Gráficos automáticos
- Seleção dinâmica de datasets

---

# 🚀 Como Executar o Projeto

## 1. Instalar dependências

```bash
pip install -r requirements.txt
```

## 2. Executar o pipeline (opcional)

```bash
python main.py
```

## 3. Rodar o dashboard

```bash
streamlit run app/app.py
```

---

# 🧪 Tecnologias Utilizadas

- Python
- Pandas
- Streamlit
- Parquet (PyArrow)
- Análise exploratória de dados (EDA)

---

# 📁 Estrutura dos Dados

- **by_passenger**: agregação por número de passageiros
- **by_day**: métricas diárias
- **by_week**: métricas semanais
- **by_shift_payment**: análise por turno e forma de pagamento
- **by_route_top100**: rotas mais frequentes

---

# 📌 Fonte

https://www.kaggle.com/datasets/elemento/nyc-yellow-taxi-trip-data

---

# 👨‍💻 Autor

Projeto desenvolvido para fins de estudo em análise de dados, engenharia de dados e visualização interativa.

@lesoares96
