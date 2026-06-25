# main.py
# Archivo principal del proyecto. Desde aquí se arranca todo el juego.

import tkinter as tk
from ventanas import VentanaJuego

def iniciar_juego():
    ventana_principal = tk.Tk()
    ventana_principal.title("Defensa y Asalto de Base")

    juego = VentanaJuego(ventana_principal, "Medieval")
    juego.iniciar_partida("Jugador 1 (Defensor)", "Jugador 2 (Atacante)")

    ventana_principal.mainloop()


if __name__ == "__main__":
    iniciar_juego()