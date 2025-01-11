import random
import socket
import time
import threading

"""
EJERCICIO 2: Productor-Consumidor con Sockets UDP
- Los productores generan aleatoriamente videojuegos con un género específico y los almacenan en una cola.
- Los consumidores envían peticiones UDP al servidor para consumir videojuegos que sean del generoque piden.
- Cada consumidor realiza un número aleatorio de peticiones y registra sus pedidos en un archivo.
- El servidor registra los consumos o errores en un archivo por cliente.
- El programa "termina" cuando los clientes han realizado todas las peticiones pero el servidor siempre quedara activo.
"""
generos = ["acción", "aventura", "rol", "deportes", "estrategia", "simulación", "romance", "carreras"] #generos de videojuegos que usaremos para crear una lista aleatoria
tamaño_lista = random.randint(5, 15)
videojuegos = []
for _ in range(tamaño_lista):
    videojuegos.append(random.choice(generos)) #generamos la lista con los generos
print("Lista de videojuegos disponibles en el servidor:", videojuegos)
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #creamos el servidor
servidor.bind(("localhost", 12345))#como pone en el temario lo ponemos escuchando en el puerto 12345
print("Servidor escuchando en localhost:12345")

def manejar_peticiones():
    while True:
        mensaje, direccion = servidor.recvfrom(1024)#recibimos el mensaje del cliente
        genero_solicitado = mensaje.decode("utf-8")
        print(f"Petición recibida de {direccion}: {genero_solicitado}")
        archivo_servidor = f"{direccion[0]}_{direccion[1]}_envios.txt"#crear o si ya esta abrir el archivo de envíos del cliente
        archivo = open(archivo_servidor, "a")
        if len(videojuegos) > 0:
            videojuego = videojuegos[0] #miramos el primer elemento
            if videojuego == genero_solicitado:
                videojuegos.pop(0)#si coincide con el elemento que ha solicitado el cliente lo  sacamos de la lista
                respuesta = f"Éxito: {videojuego} consumido."
                archivo.write(f"{respuesta}\n")
            else:#si el genero no coincide con el pedido lo volvemos a poner en la cola
                videojuegos.append(videojuegos.pop(0))
                respuesta = f"Error: {videojuego} no coincide con {genero_solicitado}."
                archivo.write(f"{respuesta}\n")
        else:
            respuesta = "Error: No hay videojuegos en la cola."
            archivo.write(f"{respuesta}\n")

        archivo.close()
        servidor.sendto(respuesta.encode("utf-8"), direccion) #mandamos la respuesta al cliente

def cliente(ip, puerto, peticiones):
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    archivo_cliente = f"{ip}_{puerto}_pedidos.txt"
    archivo = open(archivo_cliente, "w")

    for peticion in peticiones:
        archivo.write(f"Petición enviada: {peticion}\n") #ponemos la peticion en el archivo del cliente
        cliente_socket.sendto(peticion.encode("utf-8"), ("localhost", 12345)) #mandamos la peticion al servidor
        respuesta = cliente_socket.recv(1024).decode() #recibimos la respuesta del server
        archivo.write(f"Respuesta recibida: {respuesta}\n")

    archivo.close()
    cliente_socket.close()


clientes = []
num_clientes = random.randint(2, 5)  #creamos un num aleatorio de clientes
for i in range(num_clientes):
    puerto_cliente = random.randint(5000,6000)
    peticiones = [random.choice(generos) for _ in range(random.randint(5, 20))] #numero de peticiones que tendrá cada cliente
    hilo = threading.Thread(target=cliente, args=("localhost", puerto_cliente, peticiones))#creamos el hilo p
    clientes.append(hilo)
    hilo.start()

servidor_hilo = threading.Thread(target=manejar_peticiones) #iniciamos el server
servidor_hilo.start()

for hilo in clientes:
    hilo.join()

print("Todos los clientes han terminado. Pero el servidor sigue ejecutándose.")
