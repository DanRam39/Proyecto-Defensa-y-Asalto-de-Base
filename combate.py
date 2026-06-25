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
    
# Aqui se revisa una celda del tablero y dice si hay algo que bloquee el paso (muro, torre o base). Si está vacía, devuelve None.
def hay_obstaculo(tablero, fila, columna):
    objeto = tablero.obtener(fila, columna)
    if objeto is None:
        return None
    if isinstance(objeto, (Muro, Torre, Base)):
        return objeto
    return None


# Esta es la principal: mueve a todas las unidades un turno, 
def mover_unidades(tablero, unidades_en_juego):
    for ficha in unidades_en_juego: #es una lista donde cada elemento guarda la unidad
        unidad = ficha["unidad"]

        if not unidad.viva:
            continue  # si ya murió, no hace nada

        if unidad.velocidad_congelada:
            unidad.descongelar()  # pierde este turno pero queda libre para el siguiente
            continue

        fila_actual = ficha["fila"]
        columna_actual = ficha["columna"]
        fila_destino, columna_destino = unidad.mover(fila_actual, columna_actual)

        obstaculo = hay_obstaculo(tablero, fila_destino, columna_destino)

        if obstaculo is not None:
            # Hay algo en el camino, entonces ataca eso en vez de moverse
            obstaculo.recibir_daño(unidad.daño)
        elif tablero.celda_valida(fila_destino, columna_destino):
            # No hay nada en el camino, entonces avanza de verdad
            tablero.quitar(fila_actual, columna_actual)
            tablero.colocar(fila_destino, columna_destino, unidad)
            ficha["fila"] = fila_destino
            ficha["columna"] = columna_destino
        # si la celda destino se sale del tablero, simplemente no se mueve

