"""
Módulo de música de fondo del juego.

LA IDEA GENERAL
----------------
Cada pantalla del juego (menú, construcción, combate, etc.) tiene
asignada una música en el diccionario PISTAS, más abajo. Cuando
ventanas.py entra a una pantalla nueva, llama a reproducir("nombre_de_la_pantalla")
y este módulo se encarga de:

  1. Buscar qué archivo le toca a esa pantalla.
  2. Si ese archivo YA está sonando (porque la pantalla anterior usaba
     la misma música), no hacer nada: la canción sigue sin cortarse.
  3. Si es un archivo DISTINTO al que está sonando, cortar el actual y
     empezar el nuevo, siempre en loop (se repite sola sin que termine).

Así es como varias pantallas pueden "compartir" la misma canción sin
que se note un corte cada vez que cambiás de pantalla.

CÓMO AGREGAR UNA PISTA NUEVA (por ejemplo la música de combate)
------------------------------------------------------------------
1. Poné el archivo .mp3 dentro de la carpeta "musica/" de este proyecto.
2. Agregá una línea nueva al diccionario PISTAS de aquí abajo, con el
   nombre de pantalla que quieras y la ruta al archivo. Por ejemplo:

       "combate": "combate.mp3",

3. En ventanas.py, en el método de esa pantalla, agregá la línea:

       sonidos.reproducir("combate")

   (mirá cómo ya está hecho en mostrar_menu_principal, mostrar_construccion,
   etc. para copiar el mismo patrón)

Eso es todo — no hay que tocar el resto de este archivo.
"""

import os
import pygame

# Carpeta donde viven los archivos de música, relativa a este archivo.
# Usar una ruta relativa al propio sonidos.py (en vez de a la carpeta
# desde donde se ejecuta python) evita el clásico problema de "funciona
# en mi compu pero no en la del compañero" por estar parado en otra
# carpeta al ejecutar main.py.
CARPETA_MUSICA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "musica")

# Mapa de "nombre de pantalla" -> archivo de música.
# Varias pantallas pueden apuntar al MISMO archivo: eso es lo que hace
# que la música siga sonando sin cortarse al pasar de una a la otra.
PISTAS = {
    # Pantallas tranquilas: menú, login/registro y ranking comparten
    # la misma música de fondo.
    "menu":           "menu_y_ranking.mp3",
    "login":          "menu_y_ranking.mp3",
    "ranking":        "Hotline Bling - Drake low quality.mp3",

    # Pantallas de "preparar la ronda": selección de roles/facción,
    # transición entre rondas, construcción, ataque, resultado de la
    # ronda y fin de partida comparten otra música.
    "seleccion_roles":     "construccion_y_ataque.mp3",
    "transicion":          "construccion_y_ataque.mp3",
    "construccion":        "construccion_y_ataque.mp3",
    "ataque":              "construccion_y_ataque.mp3",
    "resultado_ronda":     "construccion_y_ataque.mp3",
    "fin_partida":         "construccion_y_ataque.mp3",

    # Combate: queda preparado para cuando agregues el archivo. Hasta
    # que ese archivo no exista en la carpeta musica/, esta línea no
    # hace nada raro: reproducir() simplemente nota que el archivo no
    # está y deja la música anterior sonando (ver más abajo).
    # "combate": "combate.mp3",
}

# Guarda qué pista está sonando ahora mismo, para no reiniciarla cada
# vez que se llama a reproducir() con el mismo nombre de pantalla.
_pista_actual = None
_audio_disponible = False


def inicializar():
    """Prende el motor de audio. Llamar UNA sola vez al arrancar el juego
    (ya está hecho en main.py). Si por algún motivo el audio no está
    disponible en esta computadora (sin tarjeta de sonido, drivers
    rotos, etc.), el juego sigue funcionando igual, simplemente sin
    música — nunca se cae por un problema de audio."""
    global _audio_disponible
    try:
        pygame.mixer.init()
        _audio_disponible = True
    except pygame.error:
        _audio_disponible = False


def reproducir(nombre_pantalla):
    """Pone la música que le corresponde a esta pantalla. Si la pantalla
    anterior ya estaba sonando la misma música, no la corta ni reinicia."""
    global _pista_actual

    if not _audio_disponible:
        return

    archivo = PISTAS.get(nombre_pantalla)
    if archivo is None:
        # Esta pantalla no tiene música asignada todavía (por ejemplo
        # "combate" hasta que agregues el archivo). Se deja sonando lo
        # que ya estaba, en vez de cortar la música a silencio.
        return

    if archivo == _pista_actual:
        # Es la misma pista que ya está sonando: no se toca nada, para
        # que no se note un corte/reinicio al cambiar de pantalla.
        return

    ruta_completa = os.path.join(CARPETA_MUSICA, archivo)
    if not os.path.exists(ruta_completa):
        # El archivo todavía no existe (por ejemplo, no descargaste
        # todavía la música de combate). Se avisa por consola para que
        # sea fácil notar el motivo, pero el juego sigue sin romperse.
        print(f"[sonidos] Aviso: no se encontró '{ruta_completa}', se deja la música actual.")
        return

    try:
        pygame.mixer.music.load(ruta_completa)
        pygame.mixer.music.play(loops=-1)  # loops=-1 = repetir para siempre
        _pista_actual = archivo
    except pygame.error as e:
        print(f"[sonidos] No se pudo reproducir '{ruta_completa}': {e}")


def detener():
    """Corta la música por completo (por ejemplo al cerrar el juego)."""
    global _pista_actual
    if _audio_disponible:
        pygame.mixer.music.stop()
    _pista_actual = None