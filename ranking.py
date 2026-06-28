import json
import os

ARCHIVO_USUARIOS = "usuarios.json"

def cargar_usuarios():
    if not os.path.exists(ARCHIVO_USUARIOS):
        return {}
    with open(ARCHIVO_USUARIOS, "r") as f:
        return json.load(f)

def guardar_usuarios(usuarios):
    with open(ARCHIVO_USUARIOS, "w") as f:
        json.dump(usuarios, f, indent=4)

def guardar_puntaje(nombre, puntos):
    # El ranking debe mostrar la mejor puntuación de una partida ganada,
    # no la suma de todas las partidas jugadas. Antes esto sumaba
    # "puntos" al valor guardado cada vez, así que alguien que ganara
    # muchas partidas chicas terminaba más arriba en el ranking que
    # alguien que ganó pocas partidas pero mucho mejores. Ahora se
    # guarda solo si "puntos" es mayor al récord que ya tenía.
    usuarios = cargar_usuarios()
    if nombre in usuarios:
        mejor_puntaje_anterior = usuarios[nombre].get("puntaje", 0)
        usuarios[nombre]["puntaje"] = max(mejor_puntaje_anterior, puntos)
        guardar_usuarios(usuarios)

def top_defensores():
    usuarios = cargar_usuarios()
    ordenados = sorted(
        usuarios.items(),
        key=lambda x: x[1].get("victorias_defensor", 0),
        reverse=True
    )
    return ordenados

def top_atacantes():
    usuarios = cargar_usuarios()
    ordenados = sorted(
        usuarios.items(),
        key=lambda x: x[1].get("victorias_atacante", 0),
        reverse=True
    )
    return ordenados