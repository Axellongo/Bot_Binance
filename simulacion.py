# simulacion.py

from indicadores import calcular_tendencia, calcular_resistencia
from config import PAR_TRADING, CAPITAL_INICIAL, MARGEN_COMPRA, MARGEN_VENTA

def backtest(data, capital_inicial=CAPITAL_INICIAL):
    """
    Ejecuta una simulación de backtesting con datos históricos.

    Args:
        data (list): Lista de velas históricas en formato [timestamp, open, high, low, close, volume].
        capital_inicial (float): Capital inicial para la simulación.

    Returns:
        dict: Resultados del backtesting, incluyendo métricas clave.
    """
    capital = capital_inicial
    capital_usado = 0
    cantidad_operaciones = 0
    ganancia_total = 0
    precio_max_operado = 0
    precio_min_operado = float('inf')

    operaciones = []  # Para almacenar operaciones (compra/venta)
    
    for i in range(50, len(data)):  # Comenzamos después de tener suficientes datos para calcular SMA
        velas = data[i-50:i]  # Últimas 50 velas para indicadores
        tendencia = calcular_tendencia(velas)
        resistencia = calcular_resistencia(velas)
        precio_actual = data[i][4]  # Precio de cierre actual

        # Simular compra
        if precio_actual <= tendencia * (1 - MARGEN_COMPRA) and capital > 0:
            cantidad = capital / precio_actual
            capital_usado = capital
            capital = 0  # Todo el capital fue usado para comprar
            cantidad_operaciones += 1
            precio_max_operado = max(precio_max_operado, precio_actual)
            precio_min_operado = min(precio_min_operado, precio_actual)
            operaciones.append(("Compra", data[i][0], precio_actual))
            print(f"Compra simulada a {precio_actual} en {data[i][0]}")

        # Simular venta
        elif precio_actual >= resistencia * (1 + MARGEN_VENTA) and capital_usado > 0:
            ganancia = cantidad * precio_actual - capital_usado
            capital = cantidad * precio_actual
            capital_usado = 0  # Todo fue vendido
            ganancia_total += ganancia
            cantidad_operaciones += 1
            precio_max_operado = max(precio_max_operado, precio_actual)
            precio_min_operado = min(precio_min_operado, precio_actual)
            operaciones.append(("Venta", data[i][0], precio_actual))
            print(f"Venta simulada a {precio_actual} en {data[i][0]}")

    return {
        "capital_final": capital,
        "ganancia_total": ganancia_total,
        "cantidad_operaciones": cantidad_operaciones,
        "precio_max_operado": precio_max_operado,
        "precio_min_operado": precio_min_operado,
        "operaciones": operaciones
    }
