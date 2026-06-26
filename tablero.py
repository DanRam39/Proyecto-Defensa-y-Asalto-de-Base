import tkinter as tk
from temas import TEMAS

FILAS = 10
COLUMNAS = 16
TAMANO_CELDA = 40  # píxeles por celda, ajustable


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
    # Esta clase dibuja el Tablero en pantalla. Ahora, además de pintar
    # colores, intenta usar una imagen para cada cosa (torre, unidad,
    # muro, base) según la facción. Si no encuentra la imagen, usa el
    # color como antes, para que el juego nunca se rompa por una imagen
    # faltante.
    def __init__(self, canvas, tablero, tema_nombre):
        self.canvas = canvas
        self.tablero = tablero
        self.tema_nombre = tema_nombre
        self.tema = TEMAS[tema_nombre]
        self.rectangulos = {}
        self.imagenes_cache = {}  # guarda las imágenes ya cargadas, para no cargarlas de nuevo cada vez
        self.imagenes_en_celdas = {}  # qué imagen está dibujada en cada celda ahora mismo
        self.dibujar_cuadricula()

    def dibujar_cuadricula(self):
        for fila in range(FILAS):
            for columna in range(COLUMNAS):
                x1 = columna * TAMANO_CELDA
                y1 = fila * TAMANO_CELDA
                x2 = x1 + TAMANO_CELDA
                y2 = y1 + TAMANO_CELDA
                rect_id = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=self.tema["fondo"],
                    outline="gray"
                )
                self.rectangulos[(fila, columna)] = rect_id

    def nombre_archivo_de(self, objeto):
        # Decide qué archivo de imagen le corresponde a un objeto del
        # tablero. Las imágenes de base/muro/torre llevan al final la
        # primera letra de la facción (M de Medieval, F de Futurista,
        # N de Naturaleza). Las unidades son compartidas entre todas
        # las facciones, así que van sin ninguna letra agregada.
        tipo_objeto = type(objeto).__name__.lower()
        letra_faccion = self.tema_nombre[0].upper()  # M, F o N

        if tipo_objeto == "torre":
            return f"torre{letra_faccion}.png"
        elif tipo_objeto == "base":
            return f"base{letra_faccion}.png"
        elif tipo_objeto == "muro":
            return f"muro{letra_faccion}.png"
        elif tipo_objeto in ("soldado", "tanque", "rapida"):
            return f"{tipo_objeto}.png"
        return None

    def cargar_imagen(self, nombre_archivo):
        # Carga una imagen desde la carpeta imagenes/. Si ya se cargó
        # antes, la reutiliza en vez de leerla de nuevo. Si el archivo
        # no existe, devuelve None (y se usa el color de respaldo).
        if nombre_archivo in self.imagenes_cache:
            return self.imagenes_cache[nombre_archivo]

        ruta = f"imagenes/{nombre_archivo}"
        try:
            imagen = tk.PhotoImage(file=ruta)
        except Exception:
            return None

        self.imagenes_cache[nombre_archivo] = imagen
        return imagen

    def actualizar_celda(self, fila, columna):
        objeto = self.tablero.obtener(fila, columna)
        rect_id = self.rectangulos[(fila, columna)]

        # si había una imagen dibujada antes en esta celda, se borra primero
        if (fila, columna) in self.imagenes_en_celdas:
            self.canvas.delete(self.imagenes_en_celdas[(fila, columna)])
            del self.imagenes_en_celdas[(fila, columna)]

        if objeto is None:
            self.canvas.itemconfig(rect_id, fill=self.tema["fondo"])
            return

        nombre_archivo = self.nombre_archivo_de(objeto)
        imagen = self.cargar_imagen(nombre_archivo) if nombre_archivo else None

        if imagen is not None:
            x = columna * TAMANO_CELDA + TAMANO_CELDA // 2
            y = fila * TAMANO_CELDA + TAMANO_CELDA // 2
            imagen_id = self.canvas.create_image(x, y, image=imagen)
            self.imagenes_en_celdas[(fila, columna)] = imagen_id
        else:
            # respaldo: si no hay imagen, se pinta el color como antes
            tipo_objeto = type(objeto).__name__.lower()
            if tipo_objeto == "torre":
                color = self.tema["torre"]
            elif tipo_objeto == "base":
                color = self.tema["base"]
            elif tipo_objeto == "muro":
                color = self.tema["muro"]
            else:
                color = self.tema["unidad"]
            self.canvas.itemconfig(rect_id, fill=color)

    def refrescar_todo(self):
        for fila in range(FILAS):
            for columna in range(COLUMNAS):
                self.actualizar_celda(fila, columna)
                