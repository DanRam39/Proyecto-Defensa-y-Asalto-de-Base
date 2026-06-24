# Este módulo maneja el tablero del juego: la cuadrícula donde se coloca
# la base, las torres, los muros y las unidades atacantes.

import tkinter as tk

FILAS = 10
COLUMNAS = 16
TAMAÑO_CELDA = 40  # píxeles por celda

class Tablero:
    def __init__(self, ventana, tema):
        # tema viene de temas.py, según la facción elegida por el defensor
        self.tema = tema

        # Matriz lógica: guarda qué objeto hay en cada celda (None = vacía)
        # Se accede como self.celdas[fila][columna]
        self.celdas = [[None for _ in range(COLUMNAS)] for _ in range(FILAS)]

        # Posición fija de la base central: columna 0 (lado del defensor),
        # en la fila del medio del tablero
        self.fila_base = FILAS // 2
        self.col_base = 0

        # Canvas donde se dibuja todo visualmente
        ancho = COLUMNAS * TAMAÑO_CELDA
        alto = FILAS * TAMAÑO_CELDA
        self.canvas = tk.Canvas(ventana, width=ancho, height=alto, bg=tema["fondo"])
        self.canvas.pack()

        # Guardamos referencia a cada rectángulo dibujado, para poder
        # cambiarle el color después sin tener que redibujar todo el tablero
        self.rectangulos = [[None for _ in range(COLUMNAS)] for _ in range(FILAS)]

        self.dibujar_cuadricula()

    def dibujar_cuadricula(self):
        # Dibuja todas las celdas vacías como rectángulos con borde
        for fila in range(FILAS):
            for columna in range(COLUMNAS):
                x1 = columna * TAMAÑO_CELDA
                y1 = fila * TAMAÑO_CELDA
                x2 = x1 + TAMAÑO_CELDA
                y2 = y1 + TAMAÑO_CELDA

                rect = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=self.tema["fondo"],
                    outline="gray"
                )
                self.rectangulos[fila][columna] = rect

        # Una vez dibujada la cuadrícula vacía, dibujamos la base encima
        self.dibujar_base()

    def dibujar_base(self):
        # Pinta la celda de la base con su color de facción
        color = self.tema["base"]
        rect = self.rectangulos[self.fila_base][self.col_base]
        self.canvas.itemconfig(rect, fill=color)

    def colocar(self, fila, columna, objeto, color):
        # Coloca un objeto (Torre, Unidad, etc.) en la matriz lógica
        # y actualiza el color visual de esa celda
        self.celdas[fila][columna] = objeto
        rect = self.rectangulos[fila][columna]
        self.canvas.itemconfig(rect, fill=color)

    def quitar(self, fila, columna):
        # Libera una celda (cuando algo muere o se destruye)
        self.celdas[fila][columna] = None
        rect = self.rectangulos[fila][columna]
        self.canvas.itemconfig(rect, fill=self.tema["fondo"])

    def hay_algo_en(self, fila, columna):
        return self.celdas[fila][columna] is not None

    def obtener(self, fila, columna):
        return self.celdas[fila][columna]

    def celda_valida(self, fila, columna):
        # Revisa que la posición exista dentro del tablero
        return 0 <= fila < FILAS and 0 <= columna < COLUMNAS
    
# Este módulo maneja el tablero del juego: una cuadrícula de 16 columnas x 10 filas
# donde se colocan la base, las torres, los muros y las unidades atacantes.

FILAS = 10
COLUMNAS = 16

class Tablero:
    def __init__(self):
        # Creamos la matriz vacía: una lista de 10 filas, cada una con 16 columnas.
        # Cada celda empieza en None, es decir, "no hay nada ahí todavía".
        self.celdas = [[None for _ in range(COLUMNAS)] for _ in range(FILAS)]

    def colocar(self, fila, columna, objeto):
        # Coloca un objeto (Torre, Unidad, Base, etc.) en una celda específica.
        # Antes de colocar, revisamos que la posición exista dentro del tablero
        # y que la celda esté vacía, para no sobreescribir algo por error.
        if not self.celda_valida(fila, columna):
            return False
        if self.celdas[fila][columna] is not None:
            return False  # la celda ya está ocupada
        self.celdas[fila][columna] = objeto
        return True

    def quitar(self, fila, columna):
        # Se usa cuando algo muere o es destruido, para liberar la celda.
        if self.celda_valida(fila, columna):
            self.celdas[fila][columna] = None

    def obtener(self, fila, columna):
        # Devuelve qué hay en una celda (puede ser None si está vacía).
        if self.celda_valida(fila, columna):
            return self.celdas[fila][columna]
        return None

    def celda_valida(self, fila, columna):
        # Revisa que la fila y columna estén dentro de los límites del tablero.
        return 0 <= fila < FILAS and 0 <= columna < COLUMNAS

    def colocar_base(self, base):
        # La base central siempre va en la columna 0, en la fila de en medio.
        fila_central = FILAS // 2
        self.colocar(fila_central, 0, base)
        return fila_central, 0 
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
    # Esta clase se encarga SOLO de dibujar el Tablero en pantalla.
    # Recibe un Tablero (la lógica) y un Canvas donde dibujar.
    def __init__(self, canvas, tablero, tema_nombre):
        self.canvas = canvas
        self.tablero = tablero
        self.tema = TEMAS[tema_nombre]  # diccionario de colores de la facción elegida
        self.rectangulos = {}  # guarda el id del rectángulo dibujado en cada (fila, columna)
        self.dibujar_cuadricula()

    def dibujar_cuadricula(self):
        # Dibuja el fondo de cada celda, vacío por defecto
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

    def actualizar_celda(self, fila, columna):
        # Vuelve a pintar una celda según lo que haya ahí en este momento.
        # Se llama cada vez que algo cambia: se coloca, se mueve o muere algo.
        objeto = self.tablero.obtener(fila, columna)
        rect_id = self.rectangulos[(fila, columna)]

        if objeto is None:
            color = self.tema["fondo"]
        else:
            # Usamos el nombre de la clase para saber qué color tocarle.
            # Esto asume que las clases se llaman Torre, Unidad, Base, Muro.
            tipo_objeto = type(objeto).__name__.lower()
            if tipo_objeto == "torre":
                color = self.tema["torre"]
            elif tipo_objeto == "base":
                color = self.tema["base"]
            elif tipo_objeto == "muro":
                color = self.tema["muro"]
            else:
                color = self.tema["unidad"]  # cualquier subclase de Unidad

        self.canvas.itemconfig(rect_id, fill=color)

    def refrescar_todo(self):
        # Repinta el tablero completo, útil después de varios cambios a la vez
        for fila in range(FILAS):
            for columna in range(COLUMNAS):
                self.actualizar_celda(fila, columna)