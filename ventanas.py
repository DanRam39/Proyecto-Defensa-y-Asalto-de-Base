import tkinter as tk
from tkinter import messagebox

from tablero import Tablero, TableroVisual, FILAS, COLUMNAS, TAMANO_CELDA
from defensa import Base, Torre
from combate import (Muro, disparar_torres, disparar_base, mover_unidades,
                     activar_habilidades_unidades, dinero_defensor_por_muertes,
                     dinero_atacante_por_torres, dinero_atacante_por_base)
from atacantes import Soldado, Tanque, Rapida
from usuarios import iniciar_sesion, registrar, actualizar_victoria
from ranking import top_defensores, top_atacantes, guardar_puntaje
from temas import TEMAS


class VentanaJuego:
    def __init__(self, ventana_principal):
        self.ventana = ventana_principal
        self.ventana.geometry("720x560")
        self.ventana.configure(bg="#1a1a2e")

        self.contenedor = tk.Frame(self.ventana, bg="#1a1a2e")
        self.contenedor.pack(fill="both", expand=True) 

        # Estado de sesión
        self.nombre_j1 = None
        self.nombre_j2 = None
        self.tema_nombre = "Medieval"
        self.nombre_defensor = None
        self.nombre_atacante = None

        # Estado de partida
        self.victorias_defensor = 0
        self.victorias_atacante = 0
        self.puntos_defensor = 0
        self.puntos_atacante = 0
        self.numero_ronda = 0
        self.dinero_defensor_ronda = 150
        self.dinero_atacante_ronda = 150

        # Estado de ronda
        self.tablero = None
        self.base_actual = None
        self.torres_en_juego = []
        self.muros_en_juego = []
        self.unidades_en_juego = []
        self.fila_base = 5
        self.columna_base = 0

        # Tick de combate automático
        self._tick_id = None

    # ───────────────────────────────────────────────────────
    #  UTILIDADES UI
    # ───────────────────────────────────────────────────────

    def limpiar(self):
        if self._tick_id:
            self.ventana.after_cancel(self._tick_id)
            self._tick_id = None
        for w in self.contenedor.winfo_children():
            w.destroy()

    def _titulo(self, parent, texto, size=22, color="#e94560"):
        tk.Label(parent, text=texto, font=("Georgia", size, "bold"),
                 bg=parent.cget("bg"), fg=color).pack(pady=(14, 6))

    def _label(self, parent, texto, size=11, color="#a8dadc"):
        tk.Label(parent, text=texto, font=("Arial", size),
                 bg=parent.cget("bg"), fg=color).pack()

    def _boton(self, parent, texto, comando, color="#e94560", fg="white", width=22):
        tk.Button(parent, text=texto, command=comando,
                  bg=color, fg=fg, font=("Arial", 12, "bold"),
                  relief="flat", cursor="hand2", width=width,
                  activebackground="#c73652", activeforeground="white",
                  pady=8).pack(pady=6)

    def _entry(self, parent, show=None):
        e = tk.Entry(parent, font=("Arial", 12), width=26,
                     bg="#0f3460", fg="white", insertbackground="white",
                     relief="flat", show=show)
        e.pack(pady=4)
        return e

    def _card(self, parent=None, bg="#16213e"):
        p = parent or self.contenedor
        f = tk.Frame(p, bg=bg)
        f.pack(pady=8)
        return f

    # ───────────────────────────────────────────────────────
    #  MENÚ PRINCIPAL
    # ───────────────────────────────────────────────────────

    def mostrar_menu_principal(self):
        self.limpiar()
        self.contenedor.configure(bg="#1a1a2e")

        tk.Label(self.contenedor,
                 text="⚔  Defensa y Asalto de Base  ⚔",
                 font=("Georgia", 26, "bold"),
                 bg="#1a1a2e", fg="#e94560").pack(pady=(60, 4))
        tk.Label(self.contenedor,
                 text="Estrategia por turnos · 2 jugadores",
                 font=("Arial", 11),
                 bg="#1a1a2e", fg="#a8dadc").pack(pady=(0, 40))

        card = self._card()
        self._boton(card, "⚔  Jugar",    self.ir_a_login_j1)
        self._boton(card, "🏆  Ranking",  self.mostrar_ranking,        color="#0f3460")
        self._boton(card, "✖  Salir",    self.ventana.quit,           color="#444")

    # ───────────────────────────────────────────────────────
    #  LOGIN / REGISTRO
    # ───────────────────────────────────────────────────────

    def _pantalla_login(self, titulo, callback_ok):
        self.limpiar()
        self.contenedor.configure(bg="#1a1a2e")
        self._titulo(self.contenedor, titulo, size=18)

        card = self._card()
        self._label(card, "Usuario")
        eu = self._entry(card)
        self._label(card, "Contraseña")
        ep = self._entry(card, show="*")

        msg = tk.StringVar()
        tk.Label(card, textvariable=msg, font=("Arial", 10),
                 bg="#16213e", fg="#e94560").pack(pady=2)

        def intentar_login():
            u = eu.get().strip()
            p = ep.get().strip()
            if not u or not p:
                msg.set("Completa usuario y contraseña.")
                return
            ok, datos = iniciar_sesion(u, p)
            if ok:
                callback_ok(u)
            else:
                msg.set("Usuario o contraseña incorrectos.\nSi no tienes cuenta, regístrate.")

        self._boton(card, "Iniciar sesión", intentar_login)
        self._boton(card, "Registrarse",
                    lambda: self._pantalla_registro(titulo, callback_ok),
                    color="#0f3460")
        self._boton(card, "← Volver al menú",
                    self.mostrar_menu_principal, color="#444")

    def _pantalla_registro(self, titulo_origen, callback_ok):
        self.limpiar()
        self.contenedor.configure(bg="#1a1a2e")
        self._titulo(self.contenedor, "Crear cuenta", size=18)

        card = self._card()
        self._label(card, "Nuevo usuario")
        eu = self._entry(card)
        self._label(card, "Contraseña")
        ep = self._entry(card, show="*")

        msg = tk.StringVar()
        tk.Label(card, textvariable=msg, font=("Arial", 10),
                 bg="#16213e", fg="#e94560").pack(pady=2)

        def intentar_registro():
            u = eu.get().strip()
            p = ep.get().strip()
            if not u or not p:
                msg.set("Completa todos los campos.")
                return
            ok, texto = registrar(u, p)
            if ok:
                messagebox.showinfo("Registro exitoso",
                                    f"Usuario '{u}' creado.\nAhora inicia sesión.")
                self._pantalla_login(titulo_origen, callback_ok)
            else:
                msg.set(texto)

        self._boton(card, "Registrarse", intentar_registro)
        self._boton(card, "← Volver",
                    lambda: self._pantalla_login(titulo_origen, callback_ok),
                    color="#444")

    def ir_a_login_j1(self):
        def ok_j1(nombre):
            self.nombre_j1 = nombre
            self.ir_a_login_j2()
        self._pantalla_login("Jugador 1 — Iniciar sesión", ok_j1)

    def ir_a_login_j2(self):
        def ok_j2(nombre):
            if nombre == self.nombre_j1:
                messagebox.showerror("Error",
                    "El Jugador 2 debe usar una cuenta diferente.")
                return
            self.nombre_j2 = nombre
            self.mostrar_seleccion_tema()
        self._pantalla_login("Jugador 2 — Iniciar sesión", ok_j2)

    # ───────────────────────────────────────────────────────
    #  SELECCIÓN DE TEMA
    # ───────────────────────────────────────────────────────

    def mostrar_seleccion_tema(self):
        self.limpiar()
        self.contenedor.configure(bg="#1a1a2e")
        self._titulo(self.contenedor, "Elige el tema de la partida", size=18)
        self._label(self.contenedor,
                    "Ambos jugadores jugarán con el mismo tema visual.",
                    color="#a8dadc")

        card = self._card()
        iconos = {"Medieval": "🏰", "Futurista": "🤖", "Acuático": "🌊"}
        for nombre, icono in iconos.items():
            n = nombre
            self._boton(card, f"{icono}  {nombre}",
                        lambda t=n: self._elegir_tema(t),
                        color="#0f3460")

    def _elegir_tema(self, tema):
        # Si el tema no existe en TEMAS (ej. Acuático no estaba), usar Medieval
        if tema not in TEMAS:
            tema = "Medieval"
        self.tema_nombre = tema
        self.mostrar_seleccion_defensor()

    # ───────────────────────────────────────────────────────
    #  SELECCIÓN DE ROL
    # ───────────────────────────────────────────────────────

    def mostrar_seleccion_defensor(self):
        self.limpiar()
        self.contenedor.configure(bg="#1a1a2e")
        self._titulo(self.contenedor, "¿Quién va a defender?", size=18)
        self._label(self.contenedor,
                    "El defensor construye torres y muros para proteger la base.",
                    color="#a8dadc")

        card = self._card()
        self._boton(card, f"🛡  {self.nombre_j1} defiende",
                    lambda: self._asignar_roles(self.nombre_j1, self.nombre_j2))
        self._boton(card, f"🛡  {self.nombre_j2} defiende",
                    lambda: self._asignar_roles(self.nombre_j2, self.nombre_j1),
                    color="#0f3460")

    def _asignar_roles(self, defensor, atacante):
        self.nombre_defensor = defensor
        self.nombre_atacante = atacante
        self.victorias_defensor = 0
        self.victorias_atacante = 0
        self.puntos_defensor = 0
        self.puntos_atacante = 0
        self.numero_ronda = 0
        self.dinero_defensor_ronda = 150
        self.dinero_atacante_ronda = 150
    # Inicializar tablero UNA sola vez aquí
        self.tablero = Tablero()
        self.torres_en_juego = []
        self.muros_en_juego = []
        self.unidades_en_juego = []
        self.iniciar_ronda()

    # ───────────────────────────────────────────────────────
    #  FLUJO DE RONDA
    # ───────────────────────────────────────────────────────

    def iniciar_ronda(self):
        self.numero_ronda += 1

        # Todas las torres reaparecen con vida completa en su posición
        # original al iniciar la ronda, incluso las que fueron destruidas
        # en la ronda anterior. Antes se eliminaban para siempre; ahora
        # se reconstruyen en el mismo lugar.
        torres_reconstruidas = []
        for ft in self.torres_en_juego:
            torre = ft["torre"]
            self.tablero.quitar(ft["fila"], ft["columna"])
            torre.vida_actual = torre.vida_maxima
            torre.turnos_restantes = torre.turnos_habilidad
            colocada = self.tablero.colocar(ft["fila"], ft["columna"], torre)
            if colocada:
                torres_reconstruidas.append(ft)
            # Si por alguna razón la celda ya no está libre (no debería
            # pasar, pero por seguridad), la torre se descarta en vez de
            # quedar fantasma sin estar en el tablero.
        self.torres_en_juego = torres_reconstruidas

        # Los muros reaparecen igual que las torres. Antes no tenían
        # ninguna lista propia (se colocaban en el tablero y se
        # olvidaban), así que cuando se destruían en combate se perdían
        # para siempre y nunca volvían a aparecer en rondas siguientes.
        muros_reconstruidos = []
        for fm in self.muros_en_juego:
            muro = fm["muro"]
            self.tablero.quitar(fm["fila"], fm["columna"])
            muro.vida_actual = muro.vida_maxima
            colocado = self.tablero.colocar(fm["fila"], fm["columna"], muro)
            if colocado:
                muros_reconstruidos.append(fm)
        self.muros_en_juego = muros_reconstruidos

        # Todas las unidades vuelven a origen con vida completa
        for ficha in self.unidades_en_juego:
            unidad = ficha["unidad"]
            self.tablero.quitar(ficha["fila"], ficha["columna"])
            unidad.vida_actual    = unidad.vida_maxima
            unidad.viva           = True
            unidad.velocidad_congelada = False
            unidad.cobrada        = False
            unidad.turnos_jugados = 0
            ficha["fila"]    = ficha["fila_origen"]
            ficha["columna"] = ficha["columna_origen"]
            self.tablero.colocar(ficha["fila_origen"], ficha["columna_origen"], unidad)

        # Nueva base: hay que quitar la base vieja del tablero ANTES de
        # colocar la nueva. Sin esto, Tablero.colocar() fallaba en
        # silencio porque la celda ya estaba ocupada por la base de la
        # ronda anterior: self.base_actual pasaba a apuntar a un objeto
        # nuevo con vida completa, pero el objeto que de verdad recibía
        # los ataques en el tablero seguía siendo el viejo, con la vida
        # (a veces muy baja) que le había quedado del combate anterior.
        # Por eso a veces parecía que la base "no recibía daño": el daño
        # sí se aplicaba, pero a un objeto que el marcador ya no miraba.
        if self.base_actual is not None:
            self.tablero.quitar(self.fila_base, self.columna_base)
        self.base_actual = Base(200)
        self.fila_base, self.columna_base = self.tablero.colocar_base(self.base_actual)

        self._mostrar_transicion(
            self.nombre_defensor, "Defensor 🛡",
            self.mostrar_construccion)



    def _mostrar_transicion(self, jugador, rol, callback):
        self.limpiar()
        self.contenedor.configure(bg="#1a1a2e")
        self._titulo(self.contenedor, f"Ronda {self.numero_ronda}", size=20)
        tk.Label(self.contenedor,
                 text=f"Turno de:\n{jugador}\n({rol})",
                 font=("Georgia", 16), bg="#1a1a2e", fg="white").pack(pady=20)
        self._label(self.contenedor,
                    "Pásale la computadora al jugador indicado,\nluego presiona Continuar.",
                    color="#a8dadc")
        self._boton(self.contenedor, "Continuar ▶", callback)

    # ───────────────────────────────────────────────────────
    #  FASE CONSTRUCCIÓN
    # ───────────────────────────────────────────────────────

    def mostrar_construccion(self):
        self.limpiar()
        self.contenedor.configure(bg="#1a1a2e")
        self.opcion_seleccionada = None

        top = tk.Frame(self.contenedor, bg="#1a1a2e")
        top.pack(fill="x", padx=10, pady=6)
        tk.Label(top,
                 text=f"🛡 {self.nombre_defensor}  |  Ronda {self.numero_ronda}",
                 font=("Arial", 12, "bold"), bg="#1a1a2e", fg="#a8dadc").pack(side="left")
        self.lbl_dinero_def = tk.Label(top,
                 text=f"💰 {self.dinero_defensor_ronda}",
                 font=("Arial", 13, "bold"), bg="#1a1a2e", fg="#f4d03f")
        self.lbl_dinero_def.pack(side="right")

        shop = tk.Frame(self.contenedor, bg="#16213e")
        shop.pack(fill="x", padx=10, pady=2)
        self.lbl_sel_def = tk.Label(shop, text="Selecciona qué colocar:",
                 font=("Arial", 10), bg="#16213e", fg="#a8dadc")
        self.lbl_sel_def.pack(side="left", padx=8)
        opciones = [("Torre Básica (60)", "torre_basica"),
                    ("Torre Pesada (120)", "torre_pesada"),
                    ("Torre Mágica (100)", "torre_magica"),
                    ("Muro (20)", "muro")]
        for texto, clave in opciones:
            tk.Button(shop, text=texto,
                      command=lambda k=clave: self._sel_def(k),
                      bg="#0f3460", fg="white", font=("Arial", 10),
                      relief="flat", cursor="hand2", padx=6, pady=4
                      ).pack(side="left", padx=3, pady=6)

        self.canvas = tk.Canvas(self.contenedor,
                                width=COLUMNAS * TAMANO_CELDA,
                                height=FILAS * TAMANO_CELDA,
                                bg="#1a1a2e", highlightthickness=0)
        self.canvas.pack(pady=4)
        self.visual = TableroVisual(self.canvas, self.tablero, self.tema_nombre)
        self.visual.refrescar_todo()  # ← muestra torres y muros de rondas anteriores
        self.canvas.bind("<Button-1>", self._click_construccion)

        info = tk.Frame(self.contenedor, bg="#16213e")
        info.pack()
        for txt in ["Torre Básica: Vida 100 · Daño 15 · Alcance 3",
                    "Torre Pesada: Vida 200 · Daño 25 · Alcance 2",
                    "Torre Mágica: Vida 80 · Daño 10 · Alcance 3 · Congela",
                    "Muro: Vida 50 · Bloquea el paso"]:
            tk.Label(info, text=txt, font=("Arial", 8),
                     bg="#16213e", fg="#a8dadc").pack(anchor="w", padx=8)

        self._boton(self.contenedor, "Listo ▶  Pasar al Atacante",
                    self._terminar_construccion, width=28)

    def _sel_def(self, clave):
        self.opcion_seleccionada = clave
        self.lbl_sel_def.config(
            text=f"Seleccionado: {clave.replace('_', ' ').title()}")

    def _click_construccion(self, evento):
        if not self.opcion_seleccionada:
            return
        col  = evento.x // TAMANO_CELDA
        fila = evento.y // TAMANO_CELDA
        costos = {"torre_basica": 60, "torre_pesada": 120,
                  "torre_magica": 100, "muro": 20}
        costo = costos[self.opcion_seleccionada]
        if self.dinero_defensor_ronda < costo:
            return
        if self.tablero.obtener(fila, col) is not None:
            return
        obj = self._crear_objeto(self.opcion_seleccionada)
        self.tablero.colocar(fila, col, obj)
        self.visual.actualizar_celda(fila, col)
        if self.opcion_seleccionada == "muro":
            self.muros_en_juego.append(
                {"fila": fila, "columna": col, "muro": obj})
        else:
            self.torres_en_juego.append(
                {"fila": fila, "columna": col, "torre": obj})
        self.dinero_defensor_ronda -= costo
        self.lbl_dinero_def.config(
            text=f"💰 {self.dinero_defensor_ronda}")

    def _crear_objeto(self, clave):
        if clave == "torre_basica":
            return Torre("Torre Básica", "basica", 60, 100, 15, 3, 3)
        elif clave == "torre_pesada":
            return Torre("Torre Pesada", "pesada", 120, 200, 25, 2, 4)
        elif clave == "torre_magica":
            return Torre("Torre Mágica", "magica", 100, 80, 10, 3, 2)
        elif clave == "muro":
            return Muro(50, 20)

    def _terminar_construccion(self):
        self._mostrar_transicion(
            self.nombre_atacante, "Atacante ⚔",
            self.mostrar_ataque)

    # ───────────────────────────────────────────────────────
    #  FASE ATAQUE
    # ───────────────────────────────────────────────────────

    def mostrar_ataque(self):
        self.limpiar()
        self.contenedor.configure(bg="#1a1a2e")
        self.opcion_seleccionada = None

        top = tk.Frame(self.contenedor, bg="#1a1a2e")
        top.pack(fill="x", padx=10, pady=6)
        tk.Label(top,
                 text=f"⚔ {self.nombre_atacante}  |  Ronda {self.numero_ronda}",
                 font=("Arial", 12, "bold"), bg="#1a1a2e", fg="#a8dadc").pack(side="left")
        self.lbl_dinero_atk = tk.Label(top,
                 text=f"💰 {self.dinero_atacante_ronda}",
                 font=("Arial", 13, "bold"), bg="#1a1a2e", fg="#f4d03f")
        self.lbl_dinero_atk.pack(side="right")

        shop = tk.Frame(self.contenedor, bg="#16213e")
        shop.pack(fill="x", padx=10, pady=2)
        self.lbl_sel_atk = tk.Label(shop, text="Selecciona unidad:",
                 font=("Arial", 10), bg="#16213e", fg="#a8dadc")
        self.lbl_sel_atk.pack(side="left", padx=8)
        for texto, clave in [("Soldado (50)", "soldado"),
                               ("Tanque (120)", "tanque"),
                               ("Unidad Rápida (70)", "rapida")]:
            tk.Button(shop, text=texto,
                      command=lambda k=clave: self._sel_atk(k),
                      bg="#0f3460", fg="white", font=("Arial", 10),
                      relief="flat", cursor="hand2", padx=6, pady=4
                      ).pack(side="left", padx=3, pady=6)

        self.canvas = tk.Canvas(self.contenedor,
                                width=COLUMNAS * TAMANO_CELDA,
                                height=FILAS * TAMANO_CELDA,
                                bg="#1a1a2e", highlightthickness=0)
        self.canvas.pack(pady=4)
        self.visual = TableroVisual(self.canvas, self.tablero, self.tema_nombre)
        self.visual.refrescar_todo()  # ← muestra todo lo que ya hay, incluyendo unidades anteriores
        self.canvas.bind("<Button-1>", self._click_ataque)

        info = tk.Frame(self.contenedor, bg="#16213e")
        info.pack()
        for txt in ["Soldado: Vida 80 · Daño 15 · Vel 1  |  Tanque: Vida 250 · Daño 30 · Vel 1",
                    "Unidad Rápida: Vida 60 · Daño 10 · Vel 2  |  Coloca en las 3 columnas de la derecha"]:
            tk.Label(info, text=txt, font=("Arial", 8),
                     bg="#16213e", fg="#a8dadc").pack(anchor="w", padx=8)

        self._boton(self.contenedor, "¡Listo! ▶  Iniciar combate",
                    self._terminar_ataque, width=28)

    def _sel_atk(self, clave):
        self.opcion_seleccionada = clave
        self.lbl_sel_atk.config(text=f"Seleccionada: {clave.title()}")

    def _click_ataque(self, evento):
        if not self.opcion_seleccionada:
            return
        col  = evento.x // TAMANO_CELDA
        fila = evento.y // TAMANO_CELDA
        if col < COLUMNAS - 3:
            return
        costos = {"soldado": 50, "tanque": 120, "rapida": 70}
        costo = costos[self.opcion_seleccionada]
        if self.dinero_atacante_ronda < costo:
            return
        if self.tablero.obtener(fila, col) is not None:
            return
        unidad = self._crear_unidad(self.opcion_seleccionada)
        self.tablero.colocar(fila, col, unidad)
        self.visual.actualizar_celda(fila, col)
        self.unidades_en_juego.append({
            "fila": fila,
            "columna": col,
            "fila_origen": fila,      # ← posición original guardada
            "columna_origen": col,    # ← posición original guardada
            "unidad": unidad
        })
        self.dinero_atacante_ronda -= costo
        self.lbl_dinero_atk.config(text=f"💰 {self.dinero_atacante_ronda}")

    def _crear_unidad(self, clave):
        if clave == "soldado":
            return Soldado()
        elif clave == "tanque":
            return Tanque()
        elif clave == "rapida":
            return Rapida()

    def _terminar_ataque(self):
        self.mostrar_combate()

    # ───────────────────────────────────────────────────────
    #  FASE COMBATE (automático por ticks)
    # ───────────────────────────────────────────────────────

    def mostrar_combate(self):
        self.limpiar()
        self.contenedor.configure(bg="#1a1a2e")

        top = tk.Frame(self.contenedor, bg="#1a1a2e")
        top.pack(fill="x", padx=10, pady=6)
        tk.Label(top, text=f"⚔  Combate — Ronda {self.numero_ronda}",
                 font=("Arial", 13, "bold"), bg="#1a1a2e", fg="#e94560").pack(side="left")
        self.lbl_vida_base = tk.Label(top,
                 text=f"🏰 Base: {self.base_actual.vida_actual}/{self.base_actual.vida_maxima}",
                 font=("Arial", 12, "bold"), bg="#1a1a2e", fg="#f4d03f")
        self.lbl_vida_base.pack(side="right")

        self.canvas = tk.Canvas(self.contenedor,
                                width=COLUMNAS * TAMANO_CELDA,
                                height=FILAS * TAMANO_CELDA,
                                bg="#1a1a2e", highlightthickness=0)
        self.canvas.pack(pady=4)
        self.visual = TableroVisual(self.canvas, self.tablero, self.tema_nombre)
        self.visual.refrescar_todo()

        self.log = tk.Text(self.contenedor, height=5, width=86,
                           bg="#0f3460", fg="#a8dadc",
                           font=("Courier", 9), relief="flat",
                           state="disabled")
        self.log.pack(pady=4)
        self._log("▶ Combate iniciado. Las tropas avanzan automáticamente...\n")

        self._pts_def_ronda = 0
        self._pts_atk_ronda = 0
        self._combate_terminado = False
        self._turnos_combate = 0  # salvaguarda: tope de turnos para evitar combates eternos

        self._tick_id = self.ventana.after(700, self._tick)

    def _log(self, texto):
        self.log.config(state="normal")
        self.log.insert("end", texto)
        self.log.see("end")
        self.log.config(state="disabled")

    def _tick(self):
        if self._combate_terminado:
            return

        gan_def = disparar_torres(self.tablero, self.torres_en_juego, self.unidades_en_juego)
        gan_def += disparar_base(self.tablero, self.base_actual, self.fila_base,
                                  self.columna_base, self.unidades_en_juego)
        gan_atk = mover_unidades(self.tablero, self.unidades_en_juego,
                                  self.fila_base, self.columna_base)
        msgs = activar_habilidades_unidades(self.unidades_en_juego)

        # Las torres destruidas se quedan en la lista (con vida_actual<=0):
        # disparar_torres ya las salta al disparar porque revisa
        # esta_destruida() antes de cada una. Se mantienen en la lista
        # a propósito para que iniciar_ronda() las pueda reconstruir con
        # vida completa al empezar la próxima ronda; si se filtraban y
        # eliminaban aquí, ya no había nada que reconstruir después.

        gan_def += dinero_defensor_por_muertes(self.unidades_en_juego)
        # El dinero del atacante por golpear base ya viene dentro de mover_unidades

        self._pts_def_ronda        += gan_def
        self._pts_atk_ronda        += gan_atk
        self.dinero_defensor_ronda += gan_def
        self.dinero_atacante_ronda += gan_atk

        self.visual.refrescar_todo()
        self.lbl_vida_base.config(
            text=f"🏰 Base: {self.base_actual.vida_actual}/{self.base_actual.vida_maxima}")

        for m in msgs:
            self._log(f"✦ {m}\n")
        if gan_def > 0:
            self._log(f"  Defensor +{gan_def} 💰\n")
        if gan_atk > 0:
            self._log(f"  Atacante +{gan_atk} 💰\n")

        self._turnos_combate += 1

        unidades_vivas = [f for f in self.unidades_en_juego if f["unidad"].viva]
        ganador = None
        if self.base_actual.esta_destruida():
            ganador = "atacante"
        elif len(unidades_vivas) == 0:
            ganador = "defensor"
        elif self._turnos_combate >= 200:
            # Salvaguarda: si el combate se extiende demasiado sin que
            # nadie gane (por ejemplo, unidades atascadas que ya no
            # pueden avanzar ni atacar), la ronda se cierra a favor del
            # defensor, ya que el atacante no logró destruir la base.
            ganador = "defensor"
            self._log("\n⏱  Tiempo límite de la ronda alcanzado.\n")

        if ganador:
            self._combate_terminado = True
            self._log(f"\n🏆  ¡{ganador.upper()} gana la ronda!\n")
            self.ventana.after(1200, lambda: self._fin_ronda(ganador))
        else:
            self._tick_id = self.ventana.after(700, self._tick)
    # ───────────────────────────────────────────────────────
    #  FIN DE RONDA / PARTIDA
    # ───────────────────────────────────────────────────────

    def _fin_ronda(self, ganador_ronda):
        if ganador_ronda == "defensor":
            self.victorias_defensor += 1
            self.puntos_defensor    += self._pts_def_ronda
        else:
            self.victorias_atacante += 1
            self.puntos_atacante    += self._pts_atk_ronda

        self._mostrar_resultado_ronda(ganador_ronda)

    def _mostrar_resultado_ronda(self, ganador_ronda):
        # Pantalla dedicada para que se pueda leer con calma quién ganó
        # la ronda. Antes esto solo se veía un instante en el log de
        # combate (que se borra al pasar de pantalla) y era imposible
        # de leer a tiempo.
        self.limpiar()
        self.contenedor.configure(bg="#1a1a2e")

        if ganador_ronda == "defensor":
            nombre_ganador = self.nombre_defensor
            color = "#a8dadc"
            icono = "🛡"
        else:
            nombre_ganador = self.nombre_atacante
            color = "#e94560"
            icono = "⚔"

        self._titulo(self.contenedor, f"Resultado de la Ronda {self.numero_ronda}", size=20)
        tk.Label(self.contenedor,
                 text=f"{icono}  ¡{nombre_ganador} gana la ronda!  {icono}",
                 font=("Georgia", 18, "bold"),
                 bg="#1a1a2e", fg=color).pack(pady=16)

        card = self._card()
        tk.Label(card,
                 text=(f"Marcador de la partida\n\n"
                       f"🛡 {self.nombre_defensor} (defensor): {self.victorias_defensor} rondas\n"
                       f"⚔ {self.nombre_atacante} (atacante): {self.victorias_atacante} rondas"),
                 font=("Arial", 12), bg=card.cget("bg"), fg="white",
                 justify="center").pack(pady=10)

        self._boton(self.contenedor, "Continuar ▶", self._continuar_tras_resultado, width=24)

    def _continuar_tras_resultado(self):
        if self.victorias_defensor >= 3 or self.victorias_atacante >= 3:
            self._fin_partida()
        else:
            # El dinero acumulado persiste entre rondas
            self.iniciar_ronda()

    def _fin_partida(self):
        if self.victorias_defensor >= 3:
            ganador     = self.nombre_defensor
            rol_ganador = "defensor"
            pts_ganador = self.puntos_defensor + 500
        else:
            ganador     = self.nombre_atacante
            rol_ganador = "atacante"
            pts_ganador = self.puntos_atacante + 500

        actualizar_victoria(ganador, rol_ganador)
        try:
            guardar_puntaje(ganador, pts_ganador)
        except Exception:
            pass

        self.limpiar()
        self.contenedor.configure(bg="#1a1a2e")
        self._titulo(self.contenedor, "¡Fin de la partida!", size=24)
        tk.Label(self.contenedor,
                 text=f"🏆  {ganador}  🏆",
                 font=("Georgia", 22, "bold"),
                 bg="#1a1a2e", fg="#f4d03f").pack(pady=10)
        tk.Label(self.contenedor,
                 text=(f"Defensor {self.nombre_defensor}: {self.victorias_defensor} rondas\n"
                       f"Atacante {self.nombre_atacante}: {self.victorias_atacante} rondas\n\n"
                       f"Puntos del ganador: {pts_ganador}"),
                 font=("Arial", 13), bg="#1a1a2e", fg="white").pack(pady=10)
        self._boton(self.contenedor, "🏠  Menú principal",
                    self.mostrar_menu_principal)
        self._boton(self.contenedor, "🏆  Ver ranking",
                    self.mostrar_ranking, color="#0f3460")

    # ───────────────────────────────────────────────────────
    #  RANKING
    # ───────────────────────────────────────────────────────

    def mostrar_ranking(self):
        self.limpiar()
        self.contenedor.configure(bg="#1a1a2e")
        self._titulo(self.contenedor, "🏆  Ranking de Jugadores", size=20)

        marco = tk.Frame(self.contenedor, bg="#16213e")
        marco.pack(pady=10, padx=20, fill="both", expand=True)

        # Defensores
        col_d = tk.Frame(marco, bg="#16213e")
        col_d.pack(side="left", padx=20, fill="both", expand=True)
        tk.Label(col_d, text="🛡 Mejores Defensores",
                 font=("Arial", 13, "bold"),
                 bg="#16213e", fg="#a8dadc").pack(pady=6)

        for i, (nombre, datos) in enumerate(top_defensores(), 1):
            vic = datos.get("victorias_defensor", 0)
            pts = datos.get("puntaje", 0)
            tk.Label(col_d,
                     text=f"{i}. {nombre}  —  {vic} vic  |  {pts} pts",
                     font=("Courier", 10),
                     bg="#16213e", fg="white").pack(anchor="w")

        # Separador
        tk.Frame(marco, bg="#e94560", width=2).pack(
            side="left", fill="y", pady=10)

        # Atacantes
        col_a = tk.Frame(marco, bg="#16213e")
        col_a.pack(side="left", padx=20, fill="both", expand=True)
        tk.Label(col_a, text="⚔ Mejores Atacantes",
                 font=("Arial", 13, "bold"),
                 bg="#16213e", fg="#a8dadc").pack(pady=6)

        for i, (nombre, datos) in enumerate(top_atacantes(), 1):
            vic = datos.get("victorias_atacante", 0)
            pts = datos.get("puntaje", 0)
            tk.Label(col_a,
                     text=f"{i}. {nombre}  —  {vic} vic  |  {pts} pts",
                     font=("Courier", 10),
                     bg="#16213e", fg="white").pack(anchor="w")

        self._boton(self.contenedor, "← Volver al menú",
                    self.mostrar_menu_principal, color="#444")