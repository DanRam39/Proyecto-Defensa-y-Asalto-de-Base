import tkinter as tk
from ventanas import VentanaJuego
import sonidos

def iniciar_juego():
    sonidos.inicializar()
    ventana_principal = tk.Tk()
    ventana_principal.title("Defensa y Asalto de Base")
    ventana_principal.resizable(True, True)
    juego = VentanaJuego(ventana_principal)
    juego.mostrar_menu_principal()
    ventana_principal.mainloop()

if __name__ == "__main__":
    iniciar_juego()