import streamlit as st
import pandas as pd
import os

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="NYC Taxi Analytics",
    layout="wide"
)

# =========================
# ESTILO
# =========================
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}

.kpi {
    background-color: #1c1f26;
    padding: 18px;
    border-radius: 12px;
    text-align: center;
}

.kpi-title {
    font-size: 13px;
    color: #aaa;
}

.kpi-value {
    font-size: 26px;
    font-weight: bold;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("🚕 Painel Inteligente de Corridas de Táxi - NYC")

st.markdown("""
Análise completa de mobilidade urbana em Nova York com visão operacional, tática e estratégica.
Inclui tendências, sazonalidade, comportamento de passageiros e eficiência de rotas.
""")

# =========================
# DADOS
# =========================
BASE_PATH = r".\data\processed"

FILES = {
    "por_passageiro": "by_passenger.parquet",
    "por_dia": "by_day.parquet",
    "por_semana": "by_week.parquet",
    "por_mes": "by_month.parquet",
    "por_turno_pagamento": "by_shift_payment.parquet",
    "por_hora": "by_hour.parquet",
    "top_rotas": "by_route_top100.parquet",
}

@st.cache_data
def load_data(file):
    return pd.read_parquet(os.path.join(BASE_PATH, file))

data = {k: load_data(v) for k, v in FILES.items()}

# =========================
# SIDEBAR
# =========================
st.sidebar.header("📌 Filtros de Análise")

dataset = st.sidebar.selectbox(
    "Selecione a visão analítica",
    list(data.keys()),
    index=list(data.keys()).index("por_dia")
)

df = data[dataset]

# =========================
# DETECÇÃO AUTOMÁTICA
# =========================
num_cols = df.select_dtypes(include="number").columns.tolist()
cat_cols = df.select_dtypes(include="object").columns.tolist()

if not num_cols:
    st.warning("Nenhuma métrica numérica encontrada.")
    st.stop()

metric = num_cols[0]

# =========================
# KPI BASELINE (INTELIGENTE)
# =========================
st.subheader("📊 Indicadores Principais")

col1, col2, col3, col4 = st.columns(4)

total = df[metric].sum()
media = df[metric].mean()
maximo = df[metric].max()
minimo = df[metric].min()

baseline = df[metric].mean()

col1.markdown(f"""
<div class="kpi">
<div class="kpi-title">Volume Total</div>
<div class="kpi-value">{total:,.0f}</div>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class="kpi">
<div class="kpi-title">Média Geral</div>
<div class="kpi-value">{media:,.2f}</div>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div class="kpi">
<div class="kpi-title">Maior Pico</div>
<div class="kpi-value">{maximo:,.0f}</div>
</div>
""", unsafe_allow_html=True)

col4.markdown(f"""
<div class="kpi">
<div class="kpi-title">Menor Valor</div>
<div class="kpi-value">{minimo:,.0f}</div>
</div>
""", unsafe_allow_html=True)

# =========================
# VISÃO TEMPORAL INTELIGENTE
# =========================
st.subheader("📈 Tendência e Sazonalidade")

def get_date_column(df):
    candidatos = [c for c in df.columns if any(x in c.lower() for x in ["day", "date", "mes", "week"])]
    return candidatos[0] if candidatos else None

if "dia" in df.columns or "day" in df.columns:

    date_col = get_date_column(df)

    if date_col is None:
        st.info("📊 Este dataset não possui dimensão temporal para análise de tendência.")
    else:
        try:
            df_temp = df[[date_col, metric]].copy()

            df_temp = df_temp.dropna()

            df_temp[date_col] = pd.to_datetime(df_temp[date_col], errors="coerce")

            df_temp = df_temp.dropna().sort_values(date_col).set_index(date_col)

            if df_temp.empty:
                st.warning("Sem dados suficientes para análise temporal.")
            else:
                st.line_chart(df_temp[metric])
                # crescimento
                if len(df_temp) > 1:
                    inicio = df_temp[metric].iloc[0]
                    fim = df_temp[metric].iloc[-1]

                    if inicio != 0:
                        variacao = ((fim - inicio) / inicio) * 100

                        if variacao > 0:
                            st.success(f"📈 Crescimento de {variacao:.2f}% no período")
                        else:
                            st.error(f"📉 Queda de {abs(variacao):.2f}% no período")
        except Exception as e:
            st.error(f"Erro ao processar série temporal: {e}")



# =========================
# VISÃO HORÁRIA (NOVO VALOR)
# =========================
if dataset == "por_hora":
    st.subheader("⏰ Padrão de Demanda por Hora")

    st.bar_chart(df.set_index("hora")[metric])

    pico = df.loc[df[metric].idxmax(), "hora"]
    st.info(f"🔥 Pico de demanda ocorre às {pico}h")

# =========================
# VISÃO MENSAL (NOVO)
# =========================
if dataset == "por_mes":
    st.subheader("📅 Tendência Mensal (Visão Estratégica)")

    st.line_chart(df.set_index("mes")[metric])

# =========================
# DISTRIBUIÇÃO
# =========================
st.subheader("📊 Distribuição")

if cat_cols:
    cat = cat_cols[0]

    dist = df.groupby(cat)[metric].sum().sort_values(ascending=False).head(10)

    st.bar_chart(dist)

    top = dist.index[0]
    pct = (dist.iloc[0] / dist.sum()) * 100

    st.info(f"📌 {top} concentra {pct:.1f}% do total analisado")

# =========================
# INSIGHTS (MELHORADOS)
# =========================
st.subheader("🧠 Insights Automáticos")

insights = []

if df[metric].std() > df[metric].mean():
    insights.append("⚠️ Alta volatilidade indica comportamento inconsistente da demanda.")

if df[metric].skew() > 1:
    insights.append("📊 Distribuição assimétrica sugere forte concentração em poucos eventos.")

if df[metric].max() > df[metric].mean() * 3:
    insights.append("🚨 Existem picos extremos que podem indicar eventos ou outliers.")

if not insights:
    insights.append("✅ O comportamento dos dados é relativamente estável.")

for i in insights:
    st.write(i)

# =========================
# DADOS BRUTOS
# =========================
st.subheader("🔍 Exploração dos Dados")
st.dataframe(df.head(100))

# =========================
# ANÁLISE PERSONALIZADA
# =========================
st.subheader("⚙️ Análise Personalizada")

x = st.selectbox("📍 Variável X", df.columns)

y_options = [c for c in num_cols if c != x]

if not y_options:
    st.warning("Sem variáveis numéricas para comparação.")
    st.stop()

y = st.selectbox("📊 Métrica Y", y_options)

if x == y:
    st.warning("X e Y precisam ser diferentes.")
    st.stop()

plot_df = df[[x, y]].dropna()
plot_df[x] = plot_df[x].astype(str)

st.bar_chart(plot_df.set_index(x)[y])