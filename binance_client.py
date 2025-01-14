# binance_client.py

import ccxt
from config import API_KEY, API_SECRET

def inicializar_cliente_binance():
    """
    Inicializa y devuelve un cliente de la API de Binance.
    """
    try:
        cliente = ccxt.binance({
            'apiKey': API_KEY,
            'secret': API_SECRET,
            'enableRateLimit': True,
        })
        print("Cliente de Binance inicializado correctamente.")
        return cliente
    except Exception as e:
        print(f"Error al inicializar el cliente de Binance: {e}")
        raise

# Función para obtener datos de mercado
def obtener_datos_mercado(cliente, par_trading, limite=100):
    """
    Obtiene datos históricos de velas para el par de trading especificado.

    :param cliente: Cliente de la API de Binance.
    :param par_trading: El par de trading (ej. BTC/USDT).
    :param limite: Número de velas a obtener.
    :return: Lista de velas (cada una incluye [timestamp, open, high, low, close]).
    """
    try:
        velas = cliente.fetch_ohlcv(par_trading, timeframe='15m', limit=limite)
        return velas
    except Exception as e:
        print(f"Error al obtener datos de mercado: {e}")
        return []
