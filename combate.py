#aquí se trabaja la lógica del combate 

from defensa import Base , Torre 

#se creó esta nueva clase ya que hacia falta para que las unidades tengan algo contra que chocar al moverse
class Muro:
    def __init__(self, vida, costo):
        self.costo = costo
        self.vida_maxima = vida
        self.vida_actual = vida

    def recibir_daño(self, cantidad):
        self.vida_actual = max(0, self.vida_actual - cantidad)

    def esta_destruida(self):
        return self.vida_actual <= 0

