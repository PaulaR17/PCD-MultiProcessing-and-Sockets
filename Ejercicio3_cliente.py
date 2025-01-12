import socket
import threading
import random
import time

"""
EJERCICIO 3: Clientes del restaurante
- Cada cliente abre una conexión con el servidor para solicitar una mesa.
- Esperan a ser asignados a una mesa si el restaurante está lleno.
- Liberan la mesa una vez terminan de comer y cierran la conexión.
"""

def cliente_simulado(id_cliente):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket de los clientes
    cliente.connect(("localhost", 12345))
    print(f"Cliente {id_cliente} conectado al restaurante.")

    asignado = False
    while not asignado: #esperamos a que se le asigne una mesa
        mensaje = cliente.recv(1024).decode("utf-8")
        print(f"Cliente {id_cliente}: {mensaje}")
        if "Mesa asignada" in mensaje:
            asignado = True
        time.sleep(1)
#simulacion general del tiempo comiendo...
    tiempo_comiendo = random.randint(2, 5)
    print(f"Cliente {id_cliente} comiendo durante {tiempo_comiendo} segundos.")
    time.sleep(tiempo_comiendo)
    cliente.sendall("He terminado de comer.".encode("utf-8"))
    mensaje = cliente.recv(1024).decode("utf-8")
    print(f"Cliente {id_cliente}: {mensaje}")
    cliente.close()
    print(f"Cliente {id_cliente} desconectado.")

numero_clientes = random.randint(5, 10)#num random de clientes
hilos_clientes = []

for i in range(1, numero_clientes + 1):
    hilo = threading.Thread(target=cliente_simulado, args=(i,))
    hilos_clientes.append(hilo)
    hilo.start()

for hilo in hilos_clientes:
    hilo.join()

print("Todos los clientes han sido atendidos.")
