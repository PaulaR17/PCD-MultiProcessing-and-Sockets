import random
import socket
import time
import threading

# Generación de la lista inicial de videojuegos
# Lista de géneros
generos = ["acción", "aventura", "rol", "deportes", "estrategia", "simulación", "romance", "carreras"]

# Tamaño aleatorio de la lista
tamaño_lista = random.randint(5, 15)

# Crear la lista de videojuegos
videojuegos = []
for _ in range(tamaño_lista):
    genero_aleatorio = random.choice(generos)
    videojuegos.append(genero_aleatorio)

print("Lista inicial de videojuegos:", videojuegos)

# Creación del servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.bind(("localhost", 12345))
print("Servidor escuchando en localhost:12345")

# Función para procesar las peticiones del cliente
def manejar_peticiones():
    while True:
        # Recibir la petición del cliente
        mensaje, direccion = servidor.recvfrom(1024)
        genero_solicitado = mensaje.decode("utf-8")
        print(f"Petición recibida de {direccion}: {genero_solicitado}")

        # Registrar el archivo del cliente
        archivo_servidor = f"{direccion[0]}_{direccion[1]}_envios.txt"
        archivo = open(archivo_servidor, "a")

        # Procesar la cola de videojuegos
        if len(videojuegos) > 0:
            videojuego = videojuegos[0]
            if videojuego == genero_solicitado:
                # Consumir el videojuego
                videojuegos.pop(0)
                respuesta = f"Éxito: {videojuego} consumido."
                archivo.write(f"{respuesta}\n")
            else:
                # Reinsertar el videojuego al final de la cola
                videojuegos.append(videojuegos.pop(0))
                respuesta = f"Error: {videojuego} no coincide con {genero_solicitado}."
                archivo.write(f"{respuesta}\n")
        else:
            respuesta = "Error: No hay videojuegos en la cola."
            archivo.write(f"{respuesta}\n")

        archivo.close()

        # Enviar respuesta al cliente
        servidor.sendto(respuesta.encode("utf-8"), direccion)

# Función para los clientes
def cliente(ip, puerto, peticiones):
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    archivo_cliente = f"{ip}_{puerto}_pedidos.txt"
    archivo = open(archivo_cliente, "w")

    for peticion in peticiones:
        # Registrar la petición
        archivo.write(f"Petición enviada: {peticion}\n")

        # Enviar la petición al servidor
        cliente_socket.sendto(peticion.encode("utf-8"), ("localhost", 12345))

        # Recibir la respuesta del servidor
        respuesta, _ = cliente_socket.recvfrom(1024)
        respuesta = respuesta.decode("utf-8")
        archivo.write(f"Respuesta recibida: {respuesta}\n")

    archivo.close()
    cliente_socket.close()

# Crear clientes con hilos
clientes = []
num_clientes = random.randint(2, 5)
for i in range(num_clientes):
    puerto_cliente = 5000 + i
    peticiones = [random.choice(generos) for _ in range(random.randint(1, 5))]
    hilo = threading.Thread(target=cliente, args=("localhost", puerto_cliente, peticiones))
    clientes.append(hilo)
    hilo.start()

# Iniciar el servidor en un hilo
servidor_hilo = threading.Thread(target=manejar_peticiones)
servidor_hilo.start()

# Esperar a que todos los clientes terminen
for hilo in clientes:
    hilo.join()

# El servidor sigue corriendo indefinidamente
print("Todos los clientes han terminado. El servidor sigue ejecutándose.")
"""
RESPUESTA A --> El servidor no terminará nunca su ejecución, porque estará esperando conexiones, pero cuando todos los clientes hayan terminado, lo consumido en cada archivo del servidor y cada archivo del cliente, debería coincidir. ¿Coincide siempre?
No tiene por que coincidir siempre, no hay una garantía de que esto pase. Esto es asi porque tenemos muchos factores que no podemos controlar como las condiciones de carrera, cuando volvemos a poner un elemnto en la cola, conexión...
"""