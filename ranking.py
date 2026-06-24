#Acá se muestra el top 5 de jugadores según victorias ya sea como defensor y atacante.
import json
import os

ARCHIVO_USUARIOS = "usuarios.json"

# Carga los usuarios desde el archivo JSON
def cargar_usuarios():
    if not os.path.exists(ARCHIVO_USUARIOS): #si el archivo no existe devuelve lista vacía 
        return {}
    with open(ARCHIVO_USUARIOS, "r") as f: # cuando se abre el archivo saca los datos de los jugadores y los deja listos para utilizarlos.
        return json.load(f)
#busca los usuarios 
def top_defensores():
    usuarios = cargar_usuarios()
    ordenados = sorted( # se acomodan de mayor a menor tomando en cuenta solo la cantidad de victorias 
        usuarios.items(),
        key=lambda x: x[1]["victorias_defensor"], #busca el dato victorias
        reverse=True
    )
    return ordenados[:5] #la lista se corta para dejar solamente los 5 mejores puntajes
