import os


# esta funcion va a crear un carpeta para almacenar nuesra base de datos en caso de que no exista, con fines de que quede todo mas ordenado.
def crear_carpeta(ruta, nombre):
    
    ruta_completa = os.path.join(ruta, nombre)
    if not os.path.exists(ruta_completa):
        os.makedirs(ruta_completa)
        return True, f"Se ha creado la carpeta {nombre} en {ruta}."
    else:
        return False, f"La carpeta {nombre} ya existe en {ruta}."