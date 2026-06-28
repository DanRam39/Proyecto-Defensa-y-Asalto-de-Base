import tkinter as tk
from pathlib import Path
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
    def __init__(self, canvas, tablero, tema_nombre):
        self.canvas = canvas
        self.tablero = tablero
        self.tema_nombre = tema_nombre
        self.tema = TEMAS[tema_nombre]  # diccionario de colores de la facción elegida
        self.rectangulos = {}  # guarda el id del rectángulo dibujado en cada (fila, columna)
        self.imagenes_cache = {}
        self.imagenes_en_celdas = {}
        self.directorio_imagenes = Path(__file__).resolve().parent / "imagenes"
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

    def _carpeta_tema(self):
        mapeo = {
            "Medieval": "MEDIEVAL",
            "Futurista": "Futurista",
            "Naturaleza": "Naturaleza",
            "Acuático": "Naturaleza",
        }
        carpeta = mapeo.get(self.tema_nombre, "MEDIEVAL")
        return self.directorio_imagenes / carpeta

    def nombre_archivo_de(self, objeto):
        tipo_objeto = type(objeto).__name__.lower()
        letra_faccion = self.tema_nombre[0].upper() if self.tema_nombre in {"Medieval", "Futurista", "Naturaleza"} else "N"

        if tipo_objeto == "torre":
            return f"torre{letra_faccion}.png"
        elif tipo_objeto == "base":
            return f"base{letra_faccion}.png"
        elif tipo_objeto == "muro":
            return f"muro{letra_faccion}.png"
        elif tipo_objeto in ("soldado", "tanque", "rapida"):
            return f"{tipo_objeto}.png"
        return None

    def ruta_imagen_de(self, objeto):
        tipo_objeto = type(objeto).__name__.lower()
        if tipo_objeto in ("soldado", "tanque", "rapida"):
            return self.directorio_imagenes / "unidades" / self.nombre_archivo_de(objeto)
        if tipo_objeto in ("torre", "base", "muro"):
            return self._carpeta_tema() / self.nombre_archivo_de(objeto)
        return None

    def cargar_imagen(self, ruta_imagen):
        key = str(ruta_imagen)
        if key in self.imagenes_cache:
            return self.imagenes_cache[key]

        try:
            imagen = tk.PhotoImage(file=str(ruta_imagen))
            ancho_actual = imagen.width()
            alto_actual = imagen.height()
            factor_x = ancho_actual // TAMANO_CELDA
            factor_y = alto_actual // TAMANO_CELDA
            factor = max(int(factor_x // 1.4), int(factor_y // 1.4), 1)
            imagen = imagen.subsample(factor, factor)
        except Exception:
            return None

        self.imagenes_cache[key] = imagen
        return imagen

    def actualizar_celda(self, fila, columna):
        objeto = self.tablero.obtener(fila, columna)
        rect_id = self.rectangulos[(fila, columna)]

        if (fila, columna) in self.imagenes_en_celdas:
            self.canvas.delete(self.imagenes_en_celdas[(fila, columna)])
            del self.imagenes_en_celdas[(fila, columna)]

        if objeto is None:
            self.canvas.itemconfig(rect_id, fill=self.tema["fondo"])
            return

        tipo_objeto = type(objeto).__name__.lower()
        if tipo_objeto == "torre":
            color = self.tema["torre"]
        elif tipo_objeto == "base":
            color = self.tema["base"]
        elif tipo_objeto == "muro":
            color = self.tema["muro"]
        else:
            color = self.tema["unidad"]

        ruta_imagen = self.ruta_imagen_de(objeto)
        imagen = self.cargar_imagen(ruta_imagen) if ruta_imagen else None

        if imagen is not None:
            x = columna * TAMANO_CELDA + TAMANO_CELDA // 2
            y = fila * TAMANO_CELDA + TAMANO_CELDA // 2
            imagen_id = self.canvas.create_image(x, y, image=imagen)
            self.imagenes_en_celdas[(fila, columna)] = imagen_id
        else:
            self.canvas.itemconfig(rect_id, fill=color)

    def refrescar_todo(self):
        for fila in range(FILAS):
            for columna in range(COLUMNAS):
                self.actualizar_celda(fila, columna)