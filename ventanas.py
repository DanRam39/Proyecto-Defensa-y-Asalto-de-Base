import tkinter as tk

from tablero import Tablero, TableroVisual, FILAS, COLUMNAS, TAMANO_CELDA
from defensa import Base, Torre
from combate import Muro

from atacantes import Soldado, Tanque, Rapida

from combate import ejecutar_turno

class VentanaJuego:
    def __init__(self, ventana_principal, tema_nombre):
        self.ventana = ventana_principal
        self.tema_nombre = tema_nombre

        # Frame contenedor: vamos a destruir y recrear lo que haya
        # adentro de este frame cada vez que cambiemos de pantalla,
        # en vez de manejar varias ventanas (Toplevel) sueltas.
        self.contenedor = tk.Frame(self.ventana)
        self.contenedor.pack(fill="both", expand=True)

    def limpiar_contenedor(self):
        # Borra todo lo que esté dibujado actualmente, para poder
        # dibujar la siguiente pantalla encima del mismo espacio.
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def mostrar_pantalla_transicion(self, nombre_jugador, rol, funcion_continuar):
        # rol = "Defensor" o "Atacante"
        # funcion_continuar = qué hacer cuando el jugador presiona "Continuar"
        self.limpiar_contenedor()

        mensaje = tk.Label(
            self.contenedor,
            text=f"Pásale el mouse a: {nombre_jugador}\nTurno del {rol}",
            font=("Arial", 18),
            pady=40
        )
        mensaje.pack()

        boton = tk.Button(
            self.contenedor,
            text="Continuar",
            font=("Arial", 14),
            command=funcion_continuar
        )
        boton.pack(pady=20)

    def mostrar_pantalla_construccion(self, dinero_defensor, base, torres_en_juego, funcion_continuar):
        self.limpiar_contenedor()

        self.dinero_defensor = dinero_defensor
        self.torres_en_juego = torres_en_juego
        self.opcion_seleccionada = None  # qué quiere comprar el jugador ahora mismo

        # --- Panel superior: dinero y opciones de compra ---
        panel_superior = tk.Frame(self.contenedor)
        panel_superior.pack(pady=10)

        self.etiqueta_dinero = tk.Label(
            panel_superior,
            text=f"Dinero del Defensor: {self.dinero_defensor}",
            font=("Arial", 14)
        )
        self.etiqueta_dinero.pack(side="top", pady=5)

        panel_botones = tk.Frame(panel_superior)
        panel_botones.pack()

        opciones = [
            ("Torre Básica (60)", "torre_basica", 60),
            ("Torre Pesada (120)", "torre_pesada", 120),
            ("Torre Mágica (100)", "torre_magica", 100),
            ("Muro (20)", "muro", 20),
        ]

        for texto, clave, costo in opciones:
            boton = tk.Button(
                panel_botones,
                text=texto,
                command=lambda c=clave: self.seleccionar_opcion(c)
            )
            boton.pack(side="left", padx=5)

        # --- El tablero ---
        ancho = COLUMNAS * TAMANO_CELDA
        alto = FILAS * TAMANO_CELDA
        self.canvas = tk.Canvas(self.contenedor, width=ancho, height=alto)
        self.canvas.pack(pady=10)

        self.visual = TableroVisual(self.canvas, self.tablero, self.tema_nombre)
        fila_base, col_base = self.tablero.colocar_base(base)
        self.visual.actualizar_celda(fila_base, col_base)

        self.canvas.bind("<Button-1>", self.click_en_tablero)

        # --- Botón continuar ---
        boton_listo = tk.Button(
            self.contenedor,
            text="Listo, pasar al Atacante",
            font=("Arial", 12),
            command=funcion_continuar
        )
        boton_listo.pack(pady=10)

    def seleccionar_opcion(self, clave):
        self.opcion_seleccionada = clave

    def click_en_tablero(self, evento):
        if self.opcion_seleccionada is None:
            return  # el jugador no eligió qué comprar todavía

        columna = evento.x // TAMANO_CELDA
        fila = evento.y // TAMANO_CELDA

        costos = {"torre_basica": 60, "torre_pesada": 120, "torre_magica": 100, "muro": 20}
        costo = costos[self.opcion_seleccionada]

        if self.dinero_defensor < costo:
            return  # no le alcanza, no hace nada

        if self.tablero.obtener(fila, columna) is not None:
            return  # la celda ya está ocupada

        nuevo_objeto = self.crear_objeto_comprado(self.opcion_seleccionada)
        self.tablero.colocar(fila, columna, nuevo_objeto)
        self.visual.actualizar_celda(fila, columna)

        if self.opcion_seleccionada != "muro":
            self.torres_en_juego.append({"fila": fila, "columna": columna, "torre": nuevo_objeto})

        self.dinero_defensor -= costo
        self.etiqueta_dinero.config(text=f"Dinero del Defensor: {self.dinero_defensor}")

    def crear_objeto_comprado(self, clave):
        if clave == "torre_basica":
            return Torre("Torre Básica", "basica", 60, 100, 15, 3, 3)
        elif clave == "torre_pesada":
            return Torre("Torre Pesada", "pesada", 120, 200, 25, 2, 4)
        elif clave == "torre_magica":
            return Torre("Torre Mágica", "magica", 100, 80, 10, 3, 2)
        elif clave == "muro":
            return Muro(50, 20)
    
    def mostrar_pantalla_ataque(self, dinero_atacante, unidades_en_juego, funcion_continuar):
        self.limpiar_contenedor()

        self.dinero_atacante = dinero_atacante
        self.unidades_en_juego = unidades_en_juego
        self.opcion_seleccionada = None

        # --- Panel superior: dinero y opciones de compra ---
        panel_superior = tk.Frame(self.contenedor)
        panel_superior.pack(pady=10)

        self.etiqueta_dinero = tk.Label(
            panel_superior,
            text=f"Dinero del Atacante: {self.dinero_atacante}",
            font=("Arial", 14)
        )
        self.etiqueta_dinero.pack(side="top", pady=5)

        panel_botones = tk.Frame(panel_superior)
        panel_botones.pack()

        opciones = [
            ("Soldado (50)", "soldado", 50),
            ("Tanque (120)", "tanque", 120),
            ("Unidad Rápida (70)", "rapida", 70),
        ]

        for texto, clave, costo in opciones:
            boton = tk.Button(
                panel_botones,
                text=texto,
                command=lambda c=clave: self.seleccionar_opcion(c)
            )
            boton.pack(side="left", padx=5)

        # --- El tablero (reutiliza el mismo Tablero/TableroVisual de la fase anterior) ---
        ancho = COLUMNAS * TAMANO_CELDA
        alto = FILAS * TAMANO_CELDA
        self.canvas = tk.Canvas(self.contenedor, width=ancho, height=alto)
        self.canvas.pack(pady=10)

        self.visual = TableroVisual(self.canvas, self.tablero, self.tema_nombre)
        self.visual.refrescar_todo()  # repinta todo lo que el defensor ya colocó

        self.canvas.bind("<Button-1>", self.click_en_tablero_ataque)

        # --- Botón continuar ---
        boton_listo = tk.Button(
            self.contenedor,
            text="Listo, iniciar combate",
            font=("Arial", 12),
            command=funcion_continuar
        )
        boton_listo.pack(pady=10)

    def click_en_tablero_ataque(self, evento):
        if self.opcion_seleccionada is None:
            return

        columna = evento.x // TAMANO_CELDA
        fila = evento.y // TAMANO_CELDA

        # El atacante solo puede colocar unidades en las últimas 2 columnas
        # del tablero (su zona de entrada), no en cualquier parte del mapa.
        if columna < COLUMNAS - 2:
            return

        costos = {"soldado": 50, "tanque": 120, "rapida": 70}
        costo = costos[self.opcion_seleccionada]

        if self.dinero_atacante < costo:
            return

        if self.tablero.obtener(fila, columna) is not None:
            return

        nueva_unidad = self.crear_unidad_comprada(self.opcion_seleccionada)
        self.tablero.colocar(fila, columna, nueva_unidad)
        self.visual.actualizar_celda(fila, columna)

        self.unidades_en_juego.append({"fila": fila, "columna": columna, "unidad": nueva_unidad})

        self.dinero_atacante -= costo
        self.etiqueta_dinero.config(text=f"Dinero del Atacante: {self.dinero_atacante}")

    def crear_unidad_comprada(self, clave):
        if clave == "soldado":
            return Soldado()
        elif clave == "tanque":
            return Tanque()
        elif clave == "rapida":
            return Rapida()
    
    def mostrar_pantalla_combate(self, base, dinero_atacante, funcion_terminar_ronda):
        self.limpiar_contenedor()

        self.base = base
        self.dinero_atacante_combate = dinero_atacante
        self.ganador_ronda = None
        self.funcion_terminar_ronda = funcion_terminar_ronda

        # --- El tablero ---
        ancho = COLUMNAS * TAMANO_CELDA
        alto = FILAS * TAMANO_CELDA
        self.canvas = tk.Canvas(self.contenedor, width=ancho, height=alto)
        self.canvas.pack(pady=10)

        self.visual = TableroVisual(self.canvas, self.tablero, self.tema_nombre)
        self.visual.refrescar_todo()

        # --- Panel de mensajes ---
        self.texto_mensajes = tk.Text(self.contenedor, height=6, width=60)
        self.texto_mensajes.pack(pady=10)
        self.texto_mensajes.insert("end", "Presiona 'Ejecutar turno' para iniciar el combate.\n")

        # --- Botón de turno ---
        self.boton_turno = tk.Button(
            self.contenedor,
            text="Ejecutar turno",
            font=("Arial", 12),
            command=self.ejecutar_un_turno
        )
        self.boton_turno.pack(pady=10)

    def ejecutar_un_turno(self):
        resultado = ejecutar_turno(
            self.tablero,
            self.base,
            self.torres_en_juego,
            self.unidades_en_juego,
            self.dinero_atacante_combate
        )

        # Mostramos en el panel de texto lo que pasó este turno
        self.texto_mensajes.insert("end", f"--- Turno ---\n")
        self.texto_mensajes.insert("end", f"Defensor gana: {resultado['dinero_ganado_defensor']} oro\n")
        self.texto_mensajes.insert("end", f"Atacante gana: {resultado['dinero_ganado_atacante']} oro\n")
        for mensaje in resultado["mensajes_habilidades"]:
            self.texto_mensajes.insert("end", f"{mensaje}\n")
        self.texto_mensajes.see("end")  # se desplaza automáticamente hacia abajo

        self.dinero_atacante_combate += resultado["dinero_ganado_atacante"]
        self.visual.refrescar_todo()

        if resultado["ganador_ronda"] is not None:
            self.ganador_ronda = resultado["ganador_ronda"]
            self.texto_mensajes.insert("end", f"\n¡{self.ganador_ronda.upper()} gana la ronda!\n")
            self.boton_turno.config(state="disabled")

            boton_continuar = tk.Button(
                self.contenedor,
                text="Continuar",
                font=("Arial", 12),
                command=lambda: self.funcion_terminar_ronda(
                    self.ganador_ronda,
                    resultado["dinero_ganado_defensor"],
                    self.dinero_atacante_combate
                )
            )
            boton_continuar.pack(pady=10)
    
    def iniciar_partida(self, nombre_defensor, nombre_atacante):
        # Se llama una sola vez, al principio de toda la partida.
        self.nombre_defensor = nombre_defensor
        self.nombre_atacante = nombre_atacante
        self.victorias_defensor = 0
        self.victorias_atacante = 0
        self.iniciar_ronda()

    def iniciar_ronda(self):
        # Se llama al principio de cada ronda nueva.
        # Reiniciamos el tablero y las listas, pero el marcador se mantiene.
        self.tablero = Tablero()
        self.torres_en_juego = []
        self.unidades_en_juego = []
        self.base_actual = Base(200)

        self.dinero_defensor_ronda = 150
        self.dinero_atacante_ronda = 150

        self.mostrar_pantalla_transicion(
            self.nombre_defensor,
            "Defensor",
            self.ir_a_construccion
        )

    def ir_a_construccion(self):
        self.mostrar_pantalla_construccion(
            self.dinero_defensor_ronda,
            self.base_actual,
            self.torres_en_juego,
            self.ir_a_transicion_atacante
        )

    def ir_a_transicion_atacante(self):
        # Guardamos el dinero que le quedó al defensor antes de cambiar de pantalla
        self.dinero_defensor_ronda = self.dinero_defensor
        self.mostrar_pantalla_transicion(
            self.nombre_atacante,
            "Atacante",
            self.ir_a_ataque
        )

    def ir_a_ataque(self):
        self.mostrar_pantalla_ataque(
            self.dinero_atacante_ronda,
            self.unidades_en_juego,
            self.ir_a_combate
        )

    def ir_a_combate(self):
        self.dinero_atacante_ronda = self.dinero_atacante
        self.mostrar_pantalla_combate(
            self.base_actual,
            self.dinero_atacante_ronda,
            self.terminar_ronda
        )

    def terminar_ronda(self, ganador_ronda, dinero_ganado_defensor, dinero_atacante_final):
        if ganador_ronda == "defensor":
            self.victorias_defensor += 1
        else:
            self.victorias_atacante += 1

        if self.victorias_defensor >= 3 or self.victorias_atacante >= 3:
            self.mostrar_pantalla_fin_partida()
        else:
            self.iniciar_ronda()

    def mostrar_pantalla_fin_partida(self):
        self.limpiar_contenedor()

        ganador = self.nombre_defensor if self.victorias_defensor >= 3 else self.nombre_atacante

        mensaje = tk.Label(
            self.contenedor,
            text=f"¡{ganador} gana la partida!\n\nDefensor: {self.victorias_defensor} rondas\nAtacante: {self.victorias_atacante} rondas",
            font=("Arial", 18),
            pady=40
        )
        mensaje.pack()