import random

generos = ["acción", "aventura", "rol", "deportes", "estrategia", "simulación"]
tamaño_lista = random.randint(5, 15)
videojuegos = []

for _ in range(tamaño_lista):
    genero_aleatorio = random.choice(generos)
    videojuegos.append(genero_aleatorio)

print("Lista inicial de videojuegos:", videojuegos)
