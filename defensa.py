class Base:
    def __init__(self, vida_maxima):
        self.vida_maxima = vida_maxima
        self.vida_actual = vida_maxima

    def recibir_daño(self, cantidad):
        # restamos el daño, pero no dejamos que la vida baje de 0
        self.vida_actual = max(0, self.vida_actual - cantidad)

    def esta_destruida(self):
        return self.vida_actual <= 0
    
class Torre:
    def __init__(self, nombre, tipo, costo, vida, daño, alcance, turnos_habilidad):
        self.nombre = nombre
        self.tipo = tipo  # "basica", "pesada" o "magica"
        self.costo = costo
        self.vida_maxima = vida
        self.vida_actual = vida
        self.daño = daño
        self.alcance = alcance
        self.turnos_habilidad = turnos_habilidad  # cada cuántos turnos se activa
        self.turnos_restantes = turnos_habilidad   # contador hasta la próxima activación

    def recibir_daño(self, cantidad):
        self.vida_actual = max(0, self.vida_actual - cantidad)

    def esta_destruida(self):
        return self.vida_actual <= 0
    
def puede_activar_habilidad(self):
        # bajamos el contador en 1 cada vez que se llama
        self.turnos_restantes -= 1
        if self.turnos_restantes <= 0:
            self.turnos_restantes = self.turnos_habilidad  # reiniciamos el contador
            return True
        return False

def puede_activar_habilidad(self):
        # bajamos el contador en 1 cada vez que se llama
        self.turnos_restantes -= 1
        if self.turnos_restantes <= 0:
            self.turnos_restantes = self.turnos_habilidad  # reiniciamos el contador
            return True
        return False

def activar_habilidad(self, objetivo=None):
    # objetivo es la unidad enemiga afectada, si aplica
    if self.tipo == "basica":
        # disparo doble: golpea dos veces
        if objetivo:
            objetivo.recibir_daño(self.daño)
            objetivo.recibir_daño(self.daño)

    elif self.tipo == "pesada":
        # daño en área: por ahora solo afecta al objetivo principal
            # (el área completa se maneja en combate.py, donde sí vemos el mapa)
        if objetivo:
            objetivo.recibir_daño(self.daño * 1.5)

    elif self.tipo == "magica":
        # congelar: reducimos la velocidad de la unidad a 0 por un turno
        if objetivo:
            objetivo.velocidad_congelada = True

class Base:
    def __init__(self, vida_maxima):
        self.vida_maxima = vida_maxima
        self.vida_actual = vida_maxima

    def recibir_daño(self, cantidad):
        # restamos el daño, pero no dejamos que la vida baje de 0
        self.vida_actual = max(0, self.vida_actual - cantidad)

    def esta_destruida(self):
        return self.vida_actual <= 0


class Torre:
    def __init__(self, nombre, tipo, costo, vida, daño, alcance, turnos_habilidad):
        self.nombre = nombre
        self.tipo = tipo  # "basica", "pesada" o "magica"
        self.costo = costo
        self.vida_maxima = vida
        self.vida_actual = vida
        self.daño = daño
        self.alcance = alcance
        self.turnos_habilidad = turnos_habilidad
        self.turnos_restantes = turnos_habilidad

    def recibir_daño(self, cantidad):
        self.vida_actual = max(0, self.vida_actual - cantidad)

    def esta_destruida(self):
        return self.vida_actual <= 0

    def puede_activar_habilidad(self):
        self.turnos_restantes -= 1
        if self.turnos_restantes <= 0:
            self.turnos_restantes = self.turnos_habilidad
            return True
        return False

    def activar_habilidad(self, objetivo=None):
        if self.tipo == "basica":
            # disparo doble: golpea dos veces
            if objetivo:
                objetivo.recibir_daño(self.daño)
                objetivo.recibir_daño(self.daño)

        elif self.tipo == "pesada":
            # daño en área (versión simple, el área real se calcula en combate.py)
            if objetivo:
                objetivo.recibir_daño(self.daño * 1.5)

        elif self.tipo == "magica":
            # congelar: la unidad no se mueve el siguiente turno
            if objetivo:
                objetivo.velocidad_congelada = True