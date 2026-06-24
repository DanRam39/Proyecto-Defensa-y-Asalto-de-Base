# main.py
# Archivo principal del proyecto. Desde aquí se arranca todo el juego.
# Las demás ventanas (login, selección de facción, tablero, ranking)
# se manejan en ventanas.py y se llaman desde acá.

import tkinter as tk

def iniciar_juego():
    ventana_principal = tk.Tk()
    ventana_principal.title("Defensa y Asalto de Base")

    # Por ahora mostramos un mensaje temporal mientras armamos las
    # pantallas reales en ventanas.py (login, selección de facción, etc.)
    etiqueta = tk.Label(
        ventana_principal,
        text="Defensa y Asalto de Base\n(en construcción)",
        font=("Arial", 16)
    )
    etiqueta.pack(padx=40, pady=40)

    ventana_principal.mainloop()


if __name__ == "__main__":
    iniciar_juego()