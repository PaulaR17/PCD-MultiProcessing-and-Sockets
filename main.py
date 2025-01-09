import multiprocessing as mp
import random
import time
import os

#EJERCICIO 1: Carrera de proceso
#notas:
"""
un PROCESO es almenos un programa cargado en memoria, con todos los recursos que
necesita para funcionar alojados en una zona de memoria propia, asignada SOLO para el
"""

def funcion_procesos():
    print(f"Estás en el proceso hijo {os.getpid()}")
    crear_archivo_corredor()
    avanzar()

def crear_archivo_corredor():
    print(f"Creando el archivo para el proceso {os.getpid()}")
    nombre_archivo=f"corredor_{os.getpid()}"
    archivo=open(nombre_archivo,"w") #w para escribir
    archivo.write("He iniciado el archivo")
    archivo.close()

def avanzar():
    distancia=0
    while distancia <100:#cuando un proceso llegue a 100 será cuando gane un corredor
        suma=random.randint(1,100)
        distancia+=suma
        print(f"Proceso {os.getpid()} avanzó {suma} metros. Total: {distancia} metros.")



if __name__ == "__main__":
    #cuando empecemos siempre estaremos en el proceso padre
    print("Estamos en el proceso padre")
    print(f"PID del proceso padre: {os.getpid()}")

    corredores=int(input("¿Cuantos corredores quieres?"))
    procesos = []

    for _ in range(corredores):
        process = mp.Process(target=funcion_procesos)
        process.start()
        print(f"ID del proceso hijo: {process.pid}")
        procesos.append(process)  #guardar el proceso en la lista

        # Esperar a que todos los procesos terminen
    for process in procesos:
        process.join()



