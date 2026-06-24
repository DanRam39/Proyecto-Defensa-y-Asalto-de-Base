# Este módulo contiene las clases relacionadas con el rol del defensor:
# la Base central que se debe proteger, y las Torres que la defienden.

class Base:
    def __init__(self, vida_maxima):
        self.vida_maxima = vida_maxima  # vida con la que arranca, sirve de referencia (ej. para barra de vida)
        self.vida_actual = vida_maxima  # vida que va bajando conforme recibe ataques

    def recibir_daño(self, cantidad):
        # Se llama cuando una unidad atacante le hace daño a la base
        self.vida_actual = max(0, self.vida_actual - cantidad)

    def esta_destruida(self):
        # El atacante gana la ronda cuando esto devuelve True
        return self.vida_actual <= 0


class Torre:
    # Clase única para representar cualquier torre defensiva.
    # En vez de crear una subclase por cada tipo de torre, usamos el atributo
    # "tipo" para diferenciar el comportamiento dentro de activar_habilidad().
    def __init__(self, nombre, tipo, costo, vida, daño, alcance, turnos_habilidad):
        self.nombre = nombre
        self.tipo = tipo  # "basica", "pesada" o "magica" — define qué habilidad usa
        self.costo = costo  # lo que cuesta comprarla, se resta del dinero del defensor
        self.vida_maxima = vida
        self.vida_actual = vida
        self.daño = daño  # daño que hace cada vez que ataca a una unidad
        self.alcance = alcance  # qué tan lejos puede atacar dentro del mapa
        self.turnos_habilidad = turnos_habilidad  # cada cuántos turnos se puede activar la habilidad
        self.turnos_restantes = turnos_habilidad  # contador que baja cada turno hasta llegar a 0

    def recibir_daño(self, cantidad):
        # Se llama cuando una unidad atacante le hace daño a esta torre
        self.vida_actual = max(0, self.vida_actual - cantidad)

    def esta_destruida(self):
        # El atacante gana dinero extra cuando destruye una torre (ver combate.py)
        return self.vida_actual <= 0

    def puede_activar_habilidad(self):
        # Este método se debe llamar UNA vez por turno desde combate.py.
        # Va bajando el contador y, cuando llega a 0, indica que ya toca
        # activar la habilidad y reinicia el contador para la próxima vez.
        self.turnos_restantes -= 1
        if self.turnos_restantes <= 0:
            self.turnos_restantes = self.turnos_habilidad  # se reinicia el ciclo
            return True
        return False

    def activar_habilidad(self, objetivo=None):
        # objetivo es la Unidad enemiga que recibe el efecto de la habilidad.
       
        if self.tipo == "basica":
            # Disparo doble: la torre básica golpea dos veces en el mismo turno
            if objetivo:
                objetivo.recibir_daño(self.daño)
                objetivo.recibir_daño(self.daño)

        elif self.tipo == "pesada":
            # Daño en área: 
            # El área real (afectar a varias unidades cercanas) se calcula en
            # combate.py, porque esta clase no tiene acceso al mapa ni a la
            # lista completa de unidades — solo sabe de un objetivo a la vez.
            if objetivo:
                objetivo.recibir_daño(self.daño * 1.5)

        elif self.tipo == "magica":
            # Congelar: marcamos a la unidad como congelada con un atributo nuevo.
            # combate.py debe revisar este atributo antes de mover la unidad,
            # y luego quitarle el efecto al pasar el turno.
            if objetivo:
                objetivo.velocidad_congelada = True