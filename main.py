# main.py

from binance_client import inicializar_cliente_binance, obtener_datos_mercado
from indicadores import calcular_tendencia, calcular_resistencia
from config import PAR_TRADING, CAPITAL_INICIAL, MARGEN_COMPRA, MARGEN_VENTA, INTERVALO_ITERACION 
import json
from datetime import datetime
from alertas import enviar_alerta
from simulacion import backtest
import time  # Agregado al principio del archivo

ESTADO_FILE = "estado.json"

def cargar_estado():
    """Carga el estado desde un archivo JSON."""
    try:
        with open(ESTADO_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Archivo de estado no encontrado. Creando uno nuevo.")
        return {
            "capital_inicial": 100,
            "capital_final": 100,
            "ganancia_total": 0,
            "operaciones": 0,
            "precio_max_operado": 0,
            "precio_min_operado": 0,
            "comisiones": 0,
            "precio_max_crypto": 0,
            "precio_min_crypto": 0,
            "enviar_resumen": False
        }

def guardar_estado(estado):
    """Guarda el estado en un archivo JSON."""
    with open(ESTADO_FILE, 'w') as file:
        json.dump(estado, file, indent=4)

def enviar_resumen_diario():
    """Genera y envía un resumen diario por correo."""
    estado = cargar_estado()

    resumen = (
        f"Resumen diario del bot de trading ({datetime.now().strftime('%Y-%m-%d')}):\n\n"
        f"- Capital inicial: ${estado['capital_inicial']:.2f}\n"
        f"- Capital final: ${estado['capital_final']:.2f}\n"
        f"- Ganancia total: ${estado['ganancia_total']:.2f}\n"
        f"- Operaciones realizadas: {estado['operaciones']}\n"
        f"- Precio máximo operado: ${estado['precio_max_operado']:.2f}\n"
        f"- Precio mínimo operado: ${estado['precio_min_operado']:.2f}\n"
        f"- Gasto en comisiones: ${estado['comisiones']:.2f}\n"
        f"- Precio máximo de la criptomoneda: ${estado['precio_max_crypto']:.2f}\n"
        f"- Precio mínimo de la criptomoneda: ${estado['precio_min_crypto']:.2f}\n"
    )

    try:
        enviar_alerta("Resumen diario del bot de trading", resumen)
        print("Resumen diario enviado correctamente.")
        estado["enviar_resumen"] = False  # Desactivamos el envío para la siguiente ejecución
        guardar_estado(estado)
    except Exception as e:
        print(f"Error al enviar el resumen diario: {e}")

def manejar_error(mensaje):
    """Maneja errores críticos enviando alertas y registrando el error."""
    print(mensaje)
    try:
        enviar_alerta("Error crítico en el bot", mensaje)
    except Exception as e:
        print(f"Error al enviar la alerta: {e}")

def comprar(cliente, par_trading, cantidad):
    """
    Realiza una orden de compra de mercado.
    """
    try:
        orden = cliente.create_market_buy_order(par_trading, cantidad)
        print(f"Compra ejecutada: {orden}")
        return orden
    except Exception as e:
        manejar_error(f"Error al realizar compra: {e}")
        return None

def vender(cliente, par_trading, cantidad):
    """
    Realiza una orden de venta de mercado.
    """
    try:
        orden = cliente.create_market_sell_order(par_trading, cantidad)
        print(f"Venta ejecutada: {orden}")
        return orden
    except Exception as e:
        manejar_error(f"Error al realizar venta: {e}")
        return None

def main():
    try:
        # Cargar el estado
        estado = cargar_estado()

        # Verificar si se debe enviar el resumen
        if estado["enviar_resumen"]:
            enviar_resumen_diario()

        cliente = inicializar_cliente_binance()

        while True:
            try:
                # Obtener datos de mercado
                velas = obtener_datos_mercado(cliente, PAR_TRADING, limite=50)
                if not velas:
                    mensaje_error = "No se pudieron obtener datos de mercado."
                    print(mensaje_error)
                    enviar_alerta("Error en datos de mercado", mensaje_error)
                    time.sleep(INTERVALO_ITERACION)
                    continue

                # Calcular indicadores
                tendencia = calcular_tendencia(velas)
                resistencia = calcular_resistencia(velas)

                print(f"Tendencia actual (SMA): {tendencia}")
                print(f"Resistencia actual: {resistencia}")

                # Obtener el precio actual del mercado
                ticker = cliente.fetch_ticker(PAR_TRADING)
                precio_actual = ticker['last']
                print(f"Precio actual: {precio_actual}")

                # Actualizar precios máximos y mínimos de la criptomoneda
                estado["precio_max_crypto"] = max(estado["precio_max_crypto"], precio_actual)
                estado["precio_min_crypto"] = min(estado["precio_min_crypto"], precio_actual)

                # Condición de compra
                if precio_actual <= tendencia * (1 - MARGEN_COMPRA) and estado["capital_final"] > 0:
                    cantidad = estado["capital_final"] / precio_actual
                    orden = comprar(cliente, PAR_TRADING, cantidad)
                    if orden:
                        estado["capital_final"] = 0  # Todo el capital fue usado para comprar
                        estado["operaciones"] += 1
                        estado["precio_max_operado"] = max(estado["precio_max_operado"], precio_actual)
                        estado["precio_min_operado"] = min(estado["precio_min_operado"], precio_actual)

                # Condición de venta
                elif precio_actual >= tendencia * (1 + MARGEN_VENTA) and estado["capital_final"] == 0:
                    cantidad = orden["filled"]  # Cantidad comprada
                    orden = vender(cliente, PAR_TRADING, cantidad)
                    if orden:
                        ganancia = cantidad * precio_actual - orden["cost"]
                        estado["capital_final"] = cantidad * precio_actual
                        estado["ganancia_total"] += ganancia
                        estado["operaciones"] += 1

                # Guardar estado actualizado
                guardar_estado(estado)

                # Pausar antes de la siguiente iteración
                time.sleep(INTERVALO_ITERACION)

            except Exception as iter_error:
                print(f"Error en iteración: {iter_error}")
                enviar_alerta("Error en iteración del bot", str(iter_error))
                time.sleep(INTERVALO_ITERACION)

    except KeyboardInterrupt:
        print("Bot detenido por el usuario.")
        enviar_alerta("Bot detenido", "El bot fue detenido manualmente por el usuario.")
    except Exception as e:
        mensaje_error = f"Error general en el bot: {e}"
        print(mensaje_error)
        enviar_alerta("Error crítico en el bot", mensaje_error)

if __name__ == "__main__":
    main()
