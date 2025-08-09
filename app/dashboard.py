import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Ensure the parquet file exists
try:
    df = pd.read_parquet("dados_crypto.parquet")
except FileNotFoundError:
    st.error("Arquivo 'dados_crypto.parquet' não encontrado. Certifique-se de que está no mesmo diretório.")
    st.stop()

# Convert columns to appropriate datetime types for analysis
df["DateTime"] = pd.to_datetime(df["DataHora"])
df["Day"] = df["DateTime"].dt.to_period("D")
df["Month"] = df["DateTime"].dt.to_period("M")
df["Hour"] = df["DateTime"].dt.to_period("H")

st.title("Dashboard de Crypto")

# --- Sidebar Filters ---
st.sidebar.header("Filtros")

# Currency filter
available_coins = ["Todas"] + sorted(df["Nome"].unique().tolist())
selected_coin = st.sidebar.selectbox("Selecione a Moeda:", available_coins)

# --- Centered Title for Selected Coin ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if selected_coin == "Todas":
        st.subheader("Todas as Moedas")
    else:
        st.subheader(f"Moeda: {selected_coin}")

# --- Date Range Filter with Calendar ---
min_date = df["DateTime"].min().date()
max_date = df["DateTime"].max().date()
selected_dates = st.sidebar.date_input(
    "Selecione o Período:",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

# --- Apply filters ---
filtered_df = df[
    (df["DateTime"].dt.date >= selected_dates[0]) & 
    (df["DateTime"].dt.date <= selected_dates[1])
]
if selected_coin != "Todas":
    filtered_df = filtered_df[filtered_df["Nome"] == selected_coin]

# --- Check if filtered data is empty ---
if filtered_df.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")
else:
    # Chart 1: Monthly Average USD Price Evolution
    st.subheader("Evolução do Preço Médio USD Mensal")
    fig1, ax1 = plt.subplots()
    filtered_df.groupby("Month")["PrecoUSD"].mean().plot(kind="line", ax=ax1)
    ax1.set_xlabel("Mês")
    ax1.set_ylabel("Preço Médio USD")
    st.pyplot(fig1)
    plt.close(fig1)

    # Chart 2: Monthly Average BRL Price Evolution
    st.subheader("Evolução do Preço Médio BRL Mensal")
    fig2, ax2 = plt.subplots()
    filtered_df.groupby("Month")["PrecoBRL"].mean().plot(kind="line", ax=ax2)
    ax2.set_xlabel("Mês")
    ax2.set_ylabel("Preço Médio BRL")
    st.pyplot(fig2)
    plt.close(fig2)

    # Chart 3: 24h Percentage Variation Over Time
    st.subheader("Variação Percentual ao decorrer do Período")
    fig3, ax3 = plt.subplots(figsize=(15, 6))
    filtered_df.groupby("DateTime")["PercentVar24h"].mean().plot(kind="bar", ax=ax3, rot=90)
    ax3.set_xlabel("Data e Hora")
    ax3.set_ylabel("Variação Percentual 24h")
    st.pyplot(fig3)
    plt.close(fig3)

    # Chart 4: MarketCap Share by Coin
    st.subheader("Participação das Moedas no MarketCap")
    fig4, ax4 = plt.subplots()
    marketcap_by_coin = filtered_df.groupby("Nome")["MarketCapUSD"].sum()
    marketcap_by_coin.plot(kind="pie", ax=ax4, autopct='%1.1f%%', startangle=90)
    ax4.set_ylabel('')
    st.pyplot(fig4)
    plt.close(fig4)
