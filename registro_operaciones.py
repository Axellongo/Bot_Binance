import csv

ARCHIVO_REGISTRO = "operaciones.csv"

def inicializar_registro():
    """
    Crea el archivo de registro si no existe.
    """
    with open(ARCHIVO_REGISTRO, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Fecha", "Tipo", "Par", "Cantidad", "Precio", "Comisión"])

def registrar_operacion(tipo, par, cantidad, precio, comision):
    """
    Registra una operación en el archivo CSV.
    """
    with open(ARCHIVO_REGISTRO, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().isoformat(), tipo, par, cantidad, precio, comision])
