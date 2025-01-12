import socket
import threading
import random
import time

"""
EJERCICIO 3: Restaurante con Sockets TCP
- El restaurante tiene un número limitado de mesas disponibles.
- Los clientes llegan y solicitan sentarse en una mesa, esperando si no hay mesas disponibles.
- Cuando terminan de comer, notifican al camarero para liberar la mesa y cierran la conexión.
- El restaurante cierra cuando todos los clientes han cerrado las conexiones.
- Usamos sendall con un mensaje codeado a UTF-8 para ir informando de lo que va pasando con cada cliente.
"""
mesas_disponibles = 5
mesas_ocupadas = 0
mutex = threading.Lock()
clientes_activos = 0
servidor_activo = True

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #iniciamos el servidor
servidor.bind(("localhost", 12345))
servidor.listen(5)#esto hace que puedan estar hasta 5 conexiones en espera
print("Servidor escuchando en localhost:12345")

def manejar_cliente(conexion, direccion):
    global mesas_ocupadas, clientes_activos
    mutex.acquire()
    clientes_activos += 1 #cuando se conecta un cliente +1 de clientes activos
    mutex.release()

    print(f"Cliente conectado: {direccion}")

    sentado = False #si el cliente no esta sentado lo intentamos setnar
    while not sentado:
        mutex.acquire()
        if mesas_ocupadas < mesas_disponibles: #revisar si hay una mesa en la que el cliente se pueda sentar
            mesas_ocupadas += 1
            sentado = True
            mensaje = f"Mesa asignada a {direccion}"
            conexion.sendall(mensaje.encode("utf-8")) #mostrar que se sentó
        else:
            mensaje = "Restaurante lleno."
            conexion.sendall(mensaje.encode("utf-8"))
        mutex.release()
        time.sleep(1)

    tiempo_comida = random.randint(2, 5)
    print(f"{direccion}: Comiendo durante {tiempo_comida} segundos.")
    time.sleep(tiempo_comida) #simulamos el  tiempo en el que el cliente está comiendo
    mutex.acquire()
    mesas_ocupadas -= 1 #liberamos la mesa
    mensaje = f"{direccion}: Mesa liberada."
    conexion.sendall(mensaje.encode("utf-8"))
    mutex.release()

    print(f"{direccion} ha liberado su mesa.")
    confirmacion = conexion.recv(1024).decode("utf-8") #confirmamos que se haya desconectado, daba problemas si no
    if confirmacion == "Desconectar":
        print(f"{direccion} desconectado.")

    conexion.close() #cuando lo confirmamos cerramos conexiin
    mutex.acquire()
    clientes_activos -= 1
    mutex.release()

def iniciar_servidor():
    global servidor_activo
    while servidor_activo: #mientras que le servidor este activo
        mutex.acquire()
        if not servidor_activo:
            mutex.release()
            break
        mutex.release()
        conexion, direccion = servidor.accept()
        hilo_cliente = threading.Thread(target=manejar_cliente, args=(conexion, direccion))
        hilo_cliente.start()

hilo_servidor = threading.Thread(target=iniciar_servidor) #hilo para el servidor
hilo_servidor.start()

detener_servidor = False#asi mantenemos el serivdor indefinidamente
while not detener_servidor:
    mutex.acquire()
    if clientes_activos == 0 and not servidor_activo:
        detener_servidor = True
        mutex.release()
    else:
        mutex.release()
        time.sleep(1)

servidor_activo = False
hilo_servidor.join() #tiene que terminar el hilo antes de cerrar el socket
servidor.close()
print("Servidor cerrado correctamente.")
