import multiprocessing as mp
import random
import time
import os

# Mutex para sincronización
mutex = mp.Lock()

def funcion_procesos():
    print(f"Estás en el proceso hijo {os.getpid()}")
    crear_archivo_corredor()
    avanzar()

def crear_archivo_corredor():
    nombre_archivo = f"corredor_{os.getpid()}"
    mutex.acquire()  # Bloqueo
    archivo = open(nombre_archivo, "w")
    archivo.write("LEIDO")  # Inicializamos con "LEIDO"
    archivo.close()
    mutex.release()  # Liberación del mutex

def avanzar():
    distancia = 0
    nombre_archivo = f"corredor_{os.getpid()}"

    while distancia < 100:
        if os.path.exists("terminado"):
            return

        suma = random.randint(1, 10)
        distancia += suma
        print(f"Proceso {os.getpid()} avanzó {suma} metros. Total: {distancia} metros.")

        while os.path.exists("ESCRIBIENDO_" + nombre_archivo):
            time.sleep(0.1)
        mutex.acquire()
        archivo = open(nombre_archivo, "r")
        contenido = archivo.read().strip()
        archivo.close()

        if contenido == "LEIDO":
            temp_archivo = open("ESCRIBIENDO_" + nombre_archivo, "w")
            temp_archivo.close()

            archivo = open(nombre_archivo, "w")
            archivo.write(str(distancia))
            archivo.close()

            os.remove("ESCRIBIENDO_" + nombre_archivo)
        else:
            time.sleep(0.1)
        mutex.release()

def padre():
    ganador = False
    ganador_pid = -1

    while not ganador:
        for proceso in procesos:
            pid = proceso.pid
            nombre_archivo = f"corredor_{pid}"

            if os.path.exists(nombre_archivo):
                while os.path.exists("ESCRIBIENDO_" + nombre_archivo):
                    time.sleep(0.1)

                mutex.acquire()
                archivo = open(nombre_archivo, "r")
                distancia = archivo.read().strip()
                archivo.close()

                if distancia != "LEIDO" and int(distancia) >= 100:
                    ganador = True
                    ganador_pid = pid
                    archivo_terminado = open("terminado", "w")
                    archivo_terminado.close()
                elif distancia == "LEIDO":
                    archivo = open(nombre_archivo, "w")
                    archivo.write("LEIDO")
                    archivo.close()
                mutex.release()

    print(f"LA CARRERA HA TERMINADO! Ha ganado el proceso {ganador_pid}")

if __name__ == "__main__":
    print("Estamos en el proceso padre")
    print(f"PID del proceso padre: {os.getpid()}")

    corredores = int(input("¿Cuántos corredores quieres? "))
    procesos = []

    for i in range(corredores):
        process = mp.Process(target=funcion_procesos)
        process.start()
        print(f"ID del proceso hijo: {process.pid}")
        procesos.append(process)

    padre()

    for process in procesos:
        process.join()
