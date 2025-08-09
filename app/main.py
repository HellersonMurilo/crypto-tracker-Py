import requests
import time
import logging
from datetime import datetime
import os
import pandas as pd

API_URL = "https://api.coingecko.com/api/v3/coins/markets"

PARAMS = {
    "vs_currency": "usd",  # Pegamos USD, BRL será separado
    "ids": "bitcoin,ethereum,cardano,solana,dogecoin",
    "order": "market_cap_desc",
    "per_page": 100,
    "page": 1,
    "sparkline": "false",
    "price_change_percentage": "1h,24h,7d,30d"
}

INTERVAL = 60  # segundos entre requisições

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "historical")
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_crypto_data(vs_currency: str):
    params = PARAMS.copy()
    params["vs_currency"] = vs_currency
    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Erro ao acessar API para {vs_currency}: {e}")
        return None

def merge_data(usd_data, brl_data):
    brl_dict = {coin["id"]: coin for coin in brl_data}
    merged = []
    for coin_usd in usd_data:
        coin_brl = brl_dict.get(coin_usd["id"])
        if coin_brl:
            merged.append({
                "data_hora": datetime.now(),
                "id": coin_usd["id"],
                "name": coin_usd["name"],
                "symbol": coin_usd["symbol"],
                "price_usd": coin_usd["current_price"],
                "price_brl": coin_brl["current_price"],
                "market_cap_usd": coin_usd["market_cap"],
                "volume_24h_usd": coin_usd["total_volume"],
                "percent_change_1h": coin_usd.get("price_change_percentage_1h_in_currency"),
                "percent_change_24h": coin_usd.get("price_change_percentage_24h_in_currency"),
                "percent_change_7d": coin_usd.get("price_change_percentage_7d_in_currency"),
                "percent_change_30d": coin_usd.get("price_change_percentage_30d_in_currency"),
                "circulating_supply": coin_usd.get("circulating_supply"),
                "ath": coin_usd.get("ath"),
                "ath_date": coin_usd.get("ath_date")
            })
    return merged

def save_to_parquet(data, coin):
    filepath = os.path.join(DATA_DIR, f"{coin}.parquet")

    df_new = pd.DataFrame(data)
    if os.path.exists(filepath):
        df_existing = pd.read_parquet(filepath)
        df = pd.concat([df_existing, df_new], ignore_index=True)
        df.drop_duplicates(subset=["data_hora", "id"], inplace=True)
    else:
        df = df_new

    df.to_parquet(filepath)
    logging.info(f"Salvo {len(df_new)} registros para {coin} em {filepath}")

def main():
    while True:
        data_usd = fetch_crypto_data("usd")
        data_brl = fetch_crypto_data("brl")

        if data_usd and data_brl:
            merged_data = merge_data(data_usd, data_brl)
            # Agrupar por moeda e salvar individualmente
            coins = set([c["id"] for c in merged_data])
            for coin in coins:
                coin_data = [item for item in merged_data if item["id"] == coin]
                save_to_parquet(coin_data, coin)
        else:
            logging.warning("Não foi possível obter dados completos no momento.")

        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
