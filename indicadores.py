# indicadores.py

def calcular_tendencia(velas):
    """
    Calcula la tendencia (media móvil simple) usando los precios de cierre.

    :param velas: Lista de velas ([timestamp, open, high, low, close]).
    :return: Promedio de los precios de cierre.
    """
    try:
        precios_cierre = [vela[4] for vela in velas]  # Precio de cierre
        return sum(precios_cierre) / len(precios_cierre)
    except Exception as e:
        print(f"Error al calcular tendencia: {e}")
        return None

def calcular_resistencia(velas):
    """
    Calcula el precio máximo (resistencia) en las últimas velas.

    :param velas: Lista de velas ([timestamp, open, high, low, close]).
    :return: Precio máximo.
    """
    try:
        precios_maximos = [vela[2] for vela in velas]  # Precio máximo (high)
        return max(precios_maximos)
    except Exception as e:
        print(f"Error al calcular resistencia: {e}")
        return None
