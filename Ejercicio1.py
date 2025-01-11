import multiprocessing as mp
import random
import time
import os

"""
EJERCICIO 1:Carrera de procesos
- Cada corredor tendra un archivo donde escribirá la distancia avanzada (si hay un LEIDO dentro). Mientras escribe habrá un archivo llamado igual pero en el inicio ESCRIBIENDO_
- Cuando el proceso padre revise el archivo pondrá un LEIDO (leera si no hay un archivo ESCRIBIENDO_)
- Cuando un proceso llega a 100 crea un archivo llamado ganador
- Si el proceso padre detecta el archivo ganador termina la carrera y anuncia al ganador
"""
mutex = mp.Lock()

def funcion_procesos():
    print(f"Estás en el proceso hijo {os.getpid()}")
    crear_archivo_corredor()
    avanzar()

def crear_archivo_corredor(): #creamos un archivo para cada proceso
    nombre_archivo = f"corredor_{os.getpid()}"
    mutex.acquire() #asi nos aseguramos de que ninguno mas pueda acceder al archivo
    archivo = open(nombre_archivo, "w")
    archivo.write("LEIDO")
    archivo.close()
    mutex.release()

def avanzar():
    distancia = 0
    nombre_archivo = f"corredor_{os.getpid()}"
    while distancia < 100: #cuando un corredor llegue a lo 100 m gana la carrera
        if not os.path.exists("ganador"):
            suma = random.randint(1, 10)
            distancia += suma
            print(f"Proceso {os.getpid()} Total: {distancia} metros.")
            while os.path.exists("ESCRIBIENDO_" + nombre_archivo): #si no se esta escribiendo en el archivo
                time.sleep(0.1)
            mutex.acquire()
            archivo = open(nombre_archivo, "r")
            contenido = archivo.read().strip()
            archivo.close()
            if contenido == "LEIDO": #comprobamos si el proceso padre ha escrito en el archivo
                temp_archivo = open("ESCRIBIENDO_" + nombre_archivo, "w")
                temp_archivo.close()
                archivo = open(nombre_archivo, "w")
                archivo.write(str(distancia))
                archivo.close()
                os.remove("ESCRIBIENDO_" + nombre_archivo)
            else:
                time.sleep(0.1)
            mutex.release()

    if distancia >= 100 and not os.path.exists("ganador"):
        mutex.acquire()
        archivo_ganador = open("ganador", "w")
        archivo_ganador.write(str(os.getpid()))  # escribimos el PID del proceso ganador
        archivo_ganador.close()  # cerramos el archivo
        mutex.release()
        print(f"Proceso {os.getpid()} ha ganado la carrera!!!!!")

def padre():
    while not os.path.exists("ganador"):
        time.sleep(0.1)
    mutex.acquire()
    mutex.acquire()
    archivo_ganador = open("ganador", "r")
    ganador_pid = archivo_ganador.read().strip()  # leemos el contenido
    archivo_ganador.close()  # cerramos el archivo
    mutex.release()

    print(f"LA CARRERA HA TERMINADO! Ha ganado el proceso {ganador_pid}")

if __name__ == "__main__":
    print("Estamos en el proceso padre")
    print(f"PID del proceso padre: {os.getpid()}")

    corredores = int(input("¿Cuántos corredores quieres? "))
    procesos = []

    for i in range(corredores): #creamos los procesos como los hilos y hacemos que vayan a la funcion de procesos
        process = mp.Process(target=funcion_procesos)
        process.start()
        print(f"ID del proceso hijo: {process.pid}")
        procesos.append(process)

    padre()

    for process in procesos:
        process.join()
