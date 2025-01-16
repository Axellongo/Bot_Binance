# config.py

from dotenv import load_dotenv
import os

load_dotenv()

MODO_SIMULACION = True  # True para simulación, False para operaciones reales

EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")


# Pares de trading
#PAR_TRADING = "XRP/USDT"
PAR_TRADING = "VANA/USDT"

# Configuración del bot
CAPITAL_INICIAL = 100  # Capital inicial en USD
LIMITE_PERDIDAS = 5  # Porcentaje máximo de pérdidas diarias
TIEMPO_TENDENCIA = 15  # Minutos para calcular la tendencia
MARGEN_COMPRA = 0.009  # 0.9% por debajo de la tendencia
MARGEN_VENTA = 0.009  # 0.9% por encima de la tendencia

# Configuración de correo
EMAIL_SENDER = "botbinanceal@gmail.com"  # Cambiar por el correo emisor
EMAIL_RECIPIENT = "longobucco.axel@gmail.com"  # Correo donde se recibirán las alertas


# Configuración de resumen diario
RESUMEN_DIARIO = {
    "capital_inicial": True,
    "capital_final": True,
    "ganancia": True,
    "cantidad_operaciones": True,
    "precio_maximo_operado": True,
    "precio_minimo_operado": True,
    "gasto_comisiones": True,
    "precio_maximo_dia": True,
    "precio_minimo_dia": True,
}



# Otros
LOGS_ACTIVOS = True  # Guardar logs de operaciones


# Intervalo en segundos entre iteraciones del bot
INTERVALO_ITERACION = 15  # 15 segundos por defecto