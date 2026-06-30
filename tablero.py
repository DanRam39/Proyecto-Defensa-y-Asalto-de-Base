import tkinter as tk
from pathlib import Path
from temas import TEMAS

FILAS = 10
COLUMNAS = 16
TAMANO_CELDA = 40  # píxeles por celda, ajustable

# Columna donde empieza la "zona prohibida" para el atacante, contada
# desde la derecha: con 16 columnas (índices 0-15), la 4ta columna
# contando desde el borde derecho es el índice 12. El atacante solo
# puede colocar unidades en las columnas 13, 14 y 15 (la lógica real
# de esa restricción vive en ventanas.py, en _click_ataque); esta
# columna 12 se pinta de gris fijo, en los tres temas, únicamente para
# marcar visualmente dónde está ese límite.
COLUMNA_LIMITE_ATAQUE = COLUMNAS - 4
COLOR_FRANJA_LIMITE = "#555555"


class Tablero:
    def __init__(self):
        self.celdas = [[None for _ in range(COLUMNAS)] for _ in range(FILAS)]

    def colocar(self, fila, columna, objeto):
        if not self.celda_valida(fila, columna):
            return False
        if self.celdas[fila][columna] is not None:
            return False
        self.celdas[fila][columna] = objeto
        return True

    def quitar(self, fila, columna):
        if self.celda_valida(fila, columna):
            self.celdas[fila][columna] = None

    def obtener(self, fila, columna):
        if self.celda_valida(fila, columna):
            return self.celdas[fila][columna]
        return None

    def celda_valida(self, fila, columna):
        return 0 <= fila < FILAS and 0 <= columna < COLUMNAS

    def colocar_base(self, base):
        fila_central = FILAS // 2
        self.colocar(fila_central, 0, base)
        return fila_central, 0


class TableroVisual:
    # Esta clase se encarga SOLO de dibujar el Tablero en pantalla.
    # Recibe un Tablero y un Canvas donde dibujar.
    #
    # Antes solo pintaba un cuadrado de color por cada cosa (torre, base,
    # muro, unidad). Ahora primero intenta dibujar una imagen .png; si
    # no la encuentra por algún motivo, cae de vuelta al color plano de
    # siempre, así el juego nunca se rompe por una imagen faltante.
    def __init__(self, canvas, tablero, faccion_estructuras, faccion_unidades):
        self.canvas = canvas
        self.tablero = tablero
        # El defensor y el atacante pueden tener facciones DISTINTAS. Las
        # estructuras (torres, muros, base) se dibujan con la facción del
        # defensor y las unidades atacantes con la facción del atacante.
        # Por eso se guardan dos facciones por separado, en vez de un único
        # tema compartido por todo el tablero como antes.
        self.faccion_estructuras = faccion_estructuras  # defensor: torre/muro/base
        self.faccion_unidades = faccion_unidades        # atacante: unidades
        self.tema_estructuras = TEMAS[faccion_estructuras]  # colores del defensor
        self.tema_unidades = TEMAS[faccion_unidades]        # colores del atacante
        self.rectangulos = {}  # guarda el id del rectángulo dibujado en cada (fila, columna)
        self.imagenes_cache = {}       # evita volver a leer del disco la misma imagen muchas veces
        self.imagenes_en_celdas = {}   # guarda el id de la imagen dibujada en cada (fila, columna)
        self.directorio_imagenes = Path(__file__).resolve().parent / "imagenes"
        self.dibujar_cuadricula()

    def dibujar_cuadricula(self):
        # Dibuja el fondo de cada celda. Todas usan el color de fondo
        # del tema, salvo la columna límite del atacante (ver
        # COLUMNA_LIMITE_ATAQUE), que siempre se pinta gris fijo, sin
        # importar el tema elegido, para marcar claramente desde dónde
        # ya no se pueden colocar más unidades.
        for fila in range(FILAS):
            for columna in range(COLUMNAS):
                x1 = columna * TAMANO_CELDA
                y1 = fila * TAMANO_CELDA
                x2 = x1 + TAMANO_CELDA
                y2 = y1 + TAMANO_CELDA
                color_fondo = (COLOR_FRANJA_LIMITE
                                if columna == COLUMNA_LIMITE_ATAQUE
                                else self.tema_estructuras["fondo"])
                rect_id = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color_fondo,
                    outline="gray"
                )
                self.rectangulos[(fila, columna)] = rect_id

    def _letra_de(self, faccion):
        # Letra que se usa al final del nombre de archivo de cada
        # estructura, por ejemplo "torreM.png" para Medieval. No se usa
        # simplemente la primera letra del nombre de la facción porque no
        # siempre coincide con la letra real del archivo (por eso esta
        # tabla explícita). Recibe la facción como parámetro porque ahora
        # estructuras y unidades pueden usar facciones diferentes.
        letras = {
            "Medieval":  "M",
            "Futurista": "F",
            "Naturaleza":  "N",
        }
        return letras.get(faccion, "M")

    def nombre_archivo_de(self, objeto):
        # Decide qué nombre de archivo .png le corresponde a este
        # objeto según su tipo de clase y, si es una estructura
        # (torre/base/muro), según el tema visual actual.
        tipo_objeto = type(objeto).__name__.lower()

        if tipo_objeto == "torre":
            # Cada tipo de torre (básica/pesada/mágica) tiene su propia
            # imagen distinta dentro de la facción del DEFENSOR. La básica
            # usa el archivo base (torreM.png); la pesada el de sufijo "3"
            # (torreM3.png) y la mágica el de sufijo "2" (torreM2.png).
            letra = self._letra_de(self.faccion_estructuras)
            if objeto.tipo == "pesada":
                return f"torre{letra}3.png"
            elif objeto.tipo == "magica":
                return f"torre{letra}2.png"
            else:  # "basica"
                return f"torre{letra}.png"
        elif tipo_objeto == "base":
            return f"base{self._letra_de(self.faccion_estructuras)}.png"
        elif tipo_objeto == "muro":
            return f"muro{self._letra_de(self.faccion_estructuras)}.png"
        elif tipo_objeto in ("soldado", "tanque", "rapida"):
            # Las unidades SÍ cambian de imagen según la facción del
            # ATACANTE. Los archivos Medieval son los originales, sin
            # sufijo (soldado.png); Futurista y Naturaleza usan el sufijo
            # de su letra (soldadoF.png, soldadoN.png).
            letra = self._letra_de(self.faccion_unidades)
            if letra == "M":
                return f"{tipo_objeto}.png"
            return f"{tipo_objeto}{letra}.png"
        return None

    def ruta_imagen_de(self, objeto):
        # Todas las imágenes (estructuras y unidades) viven juntas en
        # una sola carpeta imagenes/, sin subcarpetas. Los nombres de
        # archivo ya son únicos entre sí (torreM.png, baseF.png,
        # soldado.png, etc.), así que alcanza con esta única carpeta.
        nombre_archivo = self.nombre_archivo_de(objeto)
        if nombre_archivo is None:
            return None
        return self.directorio_imagenes / nombre_archivo

    def cargar_imagen(self, ruta_imagen):
        # Carga un archivo .png del disco y lo reduce de tamaño para
        # que entre en una celda del tablero. Las imágenes ya cargadas
        # se guardan en self.imagenes_cache para no leer el mismo
        # archivo del disco una y otra vez cada vez que se repinta el
        # tablero (eso sería lento y innecesario).
        clave = str(ruta_imagen)
        if clave in self.imagenes_cache:
            return self.imagenes_cache[clave]

        try:
            imagen = tk.PhotoImage(file=str(ruta_imagen))
            ancho_actual = imagen.width()
            alto_actual = imagen.height()
            # .subsample(n) reduce la imagen n veces. Se calcula n a
            # partir de qué tan grande es la imagen original comparada
            # con el tamaño de una celda, para que termine entrando.
            factor_x = ancho_actual // TAMANO_CELDA
            factor_y = alto_actual // TAMANO_CELDA
            factor = max(int(factor_x // 1.4), int(factor_y // 1.4), 1)
            imagen = imagen.subsample(factor, factor)
        except Exception:
            # Si el archivo no existe o está corrupto, no se rompe el
            # juego: simplemente no hay imagen para mostrar, y
            # actualizar_celda() va a caer al color plano de respaldo.
            return None

        self.imagenes_cache[clave] = imagen
        return imagen

    def actualizar_celda(self, fila, columna):
        # Vuelve a pintar una celda según lo que haya ahí en este momento.
        # Se llama cada vez que algo cambia: se coloca, se mueve o muere algo.
        objeto = self.tablero.obtener(fila, columna)
        rect_id = self.rectangulos[(fila, columna)]

        # Si esta celda ya tenía una imagen dibujada de antes, hay que
        # borrarla primero. Sin esto, las imágenes viejas se quedarían
        # apiladas unas sobre otras en el canvas para siempre.
        if (fila, columna) in self.imagenes_en_celdas:
            self.canvas.delete(self.imagenes_en_celdas[(fila, columna)])
            del self.imagenes_en_celdas[(fila, columna)]

        if objeto is None:
            color_fondo = (COLOR_FRANJA_LIMITE
                            if columna == COLUMNA_LIMITE_ATAQUE
                            else self.tema_estructuras["fondo"])
            self.canvas.itemconfig(rect_id, fill=color_fondo)
            return

        # Usamos el nombre de la clase para saber qué color tocarle.
        # Esto asume que las clases se llaman Torre, Unidad, Base, Muro.
        tipo_objeto = type(objeto).__name__.lower()
        if tipo_objeto == "torre":
            color = self.tema_estructuras["torre"]
        elif tipo_objeto == "base":
            color = self.tema_estructuras["base"]
        elif tipo_objeto == "muro":
            color = self.tema_estructuras["muro"]
        else:
            color = self.tema_unidades["unidad"]  # cualquier subclase de Unidad

        ruta_imagen = self.ruta_imagen_de(objeto)
        imagen = self.cargar_imagen(ruta_imagen) if ruta_imagen else None

        if imagen is not None:
            # Hay imagen disponible: se dibuja centrada en la celda,
            # encima del rectángulo (que queda invisible debajo).
            x = columna * TAMANO_CELDA + TAMANO_CELDA // 2
            y = fila * TAMANO_CELDA + TAMANO_CELDA // 2
            imagen_id = self.canvas.create_image(x, y, image=imagen)
            self.imagenes_en_celdas[(fila, columna)] = imagen_id
        else:
            # No hay imagen (todavía no se agregó el archivo, o no se
            # encontró): se usa el color plano de siempre, como respaldo.
            self.canvas.itemconfig(rect_id, fill=color)

    def refrescar_todo(self):
        # Repinta el tablero completo, útil después de varios cambios a la vez
        for fila in range(FILAS):
            for columna in range(COLUMNAS):
                self.actualizar_celda(fila, columna)