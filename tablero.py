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
    # Recibe un Tablero y un Canvas donde dibujar.
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