#Este módulo es para la gestión de todo lo realcionado con los usuarios: registro, permitiri entrada al juego
# y guardar las victorias que se van acumulando en el JSON. 

import json
import os

ARCHIVO_USUARIOS = "usuarios.json" #nombre del archivo para no tener que escribirlo constantemente. 

def cargar_usuarios(): # la función se abrir el JSON y sacar todos los usuarios existentes. Devuelve un diccionario vacío si el archivo no existe para evitar que se caiga. 
    if not os.path.exists(ARCHIVO_USUARIOS):
        return {} # acá es donde se devuelve el grupo vacío 
    with open(ARCHIVO_USUARIOS, "r") as f:
        return json.load(f)

# toma el diccionario con los usuarios y lo escribe en el JSON
def guardar_usuarios(usuarios): 
    with open(ARCHIVO_USUARIOS, "w") as f:
        json.dump(usuarios, f, indent=4)

#Es para registrar nuevos usuarios.
def registrar(nombre, contrasena):
    usuarios = cargar_usuarios()
    if nombre in usuarios:
        return False, "El usuario ya existe." #revisa que no haya otro con el mismo nombre
    usuarios[nombre] = {
        "contrasena": contrasena, #si está libre se crean los datos en limpio 
        "victorias_defensor": 0,
        "victorias_atacante": 0
    }
    guardar_usuarios(usuarios)
    return True, "Usuario registrado con éxito."

#verifica que el usuario pueda entrar al juego revisando si el nombre y la contraseña son válidos. 
def iniciar_sesion(nombre, contrasena):
    usuarios = cargar_usuarios()
    if nombre not in usuarios:
        return False, "Usuario no encontrado."
    if usuarios[nombre]["contrasena"] != contrasena: #verificación de la contraseña 
        return False, "Contraseña incorrecta."
    return True, usuarios[nombre]

#le suma 1 al contador de victorias del jugador dependiendo de con cual tol ganó. 
def actualizar_victoria(nombre, rol): 
    usuarios = cargar_usuarios()
    if nombre in usuarios: #se verifica que el usuario exista antes de sumar algo 
        if rol == "defensor":
            usuarios[nombre]["victorias_defensor"] += 1
        elif rol == "atacante":
            usuarios[nombre]["victorias_atacante"] += 1
        guardar_usuarios(usuarios)