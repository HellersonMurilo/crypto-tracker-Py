import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import os
import glob

DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "historical")

# --- Leitura de todos os arquivos .parquet ---
all_files = glob.glob(os.path.join(DATA_DIR, "*.parquet"))

if not all_files:
    st.error(f"Nenhum arquivo .parquet encontrado em '{DATA_DIR}'. Execute o coletor primeiro.")
    st.stop()

dfs = []
for file in all_files:
    try:
        df_temp = pd.read_parquet(file)
        dfs.append(df_temp)
    except Exception as e:
        st.warning(f"Erro ao ler {file}: {e}")

if not dfs:
    st.error("Não foi possível carregar nenhum dado válido.")
    st.stop()

df = pd.concat(dfs, ignore_index=True)

# --- Conversão e ajustes ---
df["DateTime"] = pd.to_datetime(df["data_hora"])
df["Day"] = df["DateTime"].dt.to_period("D")
df["Month"] = df["DateTime"].dt.to_period("M")
df["Hour"] = df["DateTime"].dt.to_period("H")

# Renomear colunas para nomes mais amigáveis
df.rename(columns={
    "name": "Nome",
    "price_usd": "PrecoUSD",
    "price_brl": "PrecoBRL",
    "market_cap_usd": "MarketCapUSD",
    "percent_change_24h": "PercentVar24h"
}, inplace=True)

# --- Título ---
st.title("Dashboard de Crypto")

# --- Sidebar Filtros ---
st.sidebar.header("Filtros")
available_coins = ["Todas"] + sorted(df["Nome"].unique().tolist())
selected_coin = st.sidebar.selectbox("Selecione a Moeda:", available_coins)

# --- Período ---
min_date = df["DateTime"].min().date()
max_date = df["DateTime"].max().date()
selected_dates = st.sidebar.date_input(
    "Selecione o Período:",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

# --- Filtro aplicado ---
filtered_df = df[
    (df["DateTime"].dt.date >= selected_dates[0]) &
    (df["DateTime"].dt.date <= selected_dates[1])
]
if selected_coin != "Todas":
    filtered_df = filtered_df[filtered_df["Nome"] == selected_coin]

# --- Verificação de dados ---
if filtered_df.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")
    st.stop()

# --- Decidir granularidade: se há mais de 1 mês distinto, usar mês, senão dia ---
num_months_distintos = filtered_df["Month"].nunique()
if num_months_distintos > 1:
    agrupamento = "Month"
    label_x = "Mês"
    titulo_usd = "Evolução do Preço Médio USD Mensal"
    titulo_brl = "Evolução do Preço Médio BRL Mensal"
    # Para gráfico, transformar PeriodIndex para timestamps para melhor exibição
    def converter_periodo(index):
        return index.to_timestamp()
else:
    agrupamento = "Day"
    label_x = "Dia"
    titulo_usd = "Evolução do Preço Médio USD Diário"
    titulo_brl = "Evolução do Preço Médio BRL Diário"
    def converter_periodo(index):
        return index.to_timestamp()

# --- Gráfico 1 ---
st.subheader(titulo_usd)
fig1, ax1 = plt.subplots()
grouped_usd = filtered_df.groupby(agrupamento)["PrecoUSD"].mean()
grouped_usd.index = converter_periodo(grouped_usd.index)
grouped_usd.plot(kind="line", ax=ax1, marker='o')
ax1.set_xlabel(label_x)
ax1.set_ylabel("Preço Médio USD")
ax1.grid(True)
plt.xticks(rotation=45)
st.pyplot(fig1)
plt.close(fig1)

# --- Gráfico 2 ---
st.subheader(titulo_brl)
fig2, ax2 = plt.subplots()
grouped_brl = filtered_df.groupby(agrupamento)["PrecoBRL"].mean()
grouped_brl.index = converter_periodo(grouped_brl.index)
grouped_brl.plot(kind="line", ax=ax2, marker='o')
ax2.set_xlabel(label_x)
ax2.set_ylabel("Preço Médio BRL")
ax2.grid(True)
plt.xticks(rotation=45)
st.pyplot(fig2)
plt.close(fig2)

# --- Gráfico 3: Variação % 24h ---
st.subheader("Variação Percentual ao decorrer do Período")
fig3, ax3 = plt.subplots(figsize=(15, 6))
# Aqui usa DateTime direto, mas podemos agrupar por hora ou dia para legibilidade
var24h_grouped = filtered_df.groupby(filtered_df["DateTime"].dt.to_period("H"))["PercentVar24h"].mean()
var24h_grouped.index = var24h_grouped.index.to_timestamp()
var24h_grouped.plot(kind="bar", ax=ax3, rot=90)
ax3.set_xlabel("Data e Hora")
ax3.set_ylabel("Variação Percentual 24h")
st.pyplot(fig3)
plt.close(fig3)

# --- Gráfico 4: Participação no MarketCap ---
st.subheader("Participação das Moedas no MarketCap")
fig4, ax4 = plt.subplots()
marketcap_by_coin = filtered_df.groupby("Nome")["MarketCapUSD"].sum()
marketcap_by_coin.plot(kind="pie", ax=ax4, autopct='%1.1f%%', startangle=90)
ax4.set_ylabel('')
st.pyplot(fig4)
plt.close(fig4)
