#aquí se trabaja la lógica del combate 

from defensa import Base , Torre 
torres_en_juego = [] #guarda cada torre puesta en el mapa junto con su fila y columna 
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

#estas son para revisar si alguien ganó la ronda
def gano_atacante(base):
    return base.esta_destruida() #returna true si la base si fue destruida


def gano_defensor(base, dinero_atacante, unidades_en_juego):
    if base.esta_destruida():
        return False #si la base está destruida el defensor no puede ser el ganador

    unidades_vivas = [f for f in unidades_en_juego if f["unidad"].viva] #filtra la lista para ver las unidades q siguen vivas
    sin_unidades = len(unidades_vivas) == 0 #cuando el atacante ya no tiene nada en el mapa
    sin_dinero = dinero_atacante <= 0 #cuando ya no tiene plata para generar más unidades

    return sin_unidades and sin_dinero #el defensor gana si ambas se cumplen simultaneamente

#en esta se unen las funciones anteriores para no llamarlas por separado
def verificar_victoria_ronda(base, dinero_atacante, unidades_en_juego):
    if gano_atacante(base):
        return "atacante"
    if gano_defensor(base, dinero_atacante, unidades_en_juego):
        return "defensor"
    return None

#DISPARO DE TORRES........................................

def unidades_en_rango(fila_torre, columna_torre, alcance, unidades_en_juego):
    en_rango = []
    for ficha in unidades_en_juego:
        unidad = ficha["unidad"]
        if not unidad.viva:
            continue  # si ya murió la ignora y pasa a la siguiente 
        distancia = abs(fila_torre - ficha["fila"]) + abs(columna_torre - ficha["columna"]) #calcula cuantas casillas de distancia hay entre la torre y la unidad
        if distancia <= alcance: #si la unidad está dentro del alcance la guarda enb la lista
            en_rango.append(ficha)
    return en_rango


# De todas las unidades que están en rango, esta función elige la que
# está más cerca de la torre, para saber a cuál le va a disparar.
def ficha_mas_cercana(fila_torre, columna_torre, fichas):
    mas_cercana = None #esta es para guardar le mejor opcion encontrada
    distancia_minima = None
    for ficha in fichas: # calcula de nuevo la distancia en casillas para esta unidad especifica
        distancia = abs(fila_torre - ficha["fila"]) + abs(columna_torre - ficha["columna"])
        if distancia_minima is None or distancia < distancia_minima: # si es la primera unidad que revisa o es la nueva más cercana actualiza el record de distancia
            distancia_minima = distancia
            mas_cercana = ficha
    return mas_cercana


# Esta es la función principal de esta parte. Se llama una vez cada turno
# y hace que cada torre que esté viva ataque a la unidad enemiga más
# cercana que tenga dentro de su alcance. Si a la torre le toca activar
# su habilidad este turno, también la activa.
def disparar_torres(torres_en_juego, unidades_en_juego):
    for ficha_torre in torres_en_juego:
        torre = ficha_torre["torre"]

        if torre.esta_destruida():
            continue  # una torre destruida no puede disparar

        en_rango = unidades_en_rango(
            ficha_torre["fila"], ficha_torre["columna"], torre.alcance, unidades_en_juego
        )

        if not en_rango:
            continue  # no hay nadie cerca, no hace nada este turno

        objetivo_ficha = ficha_mas_cercana(ficha_torre["fila"], ficha_torre["columna"], en_rango)
        objetivo = objetivo_ficha["unidad"]

        objetivo.recibir_daño(torre.daño)  # el disparo normal de cada turno

        if torre.puede_activar_habilidad():
            if torre.tipo == "pesada":
                # La torre pesada con su habilidad le pega a todos los
                # que estén en rango, no solo al más cercano
                for ficha_en_rango in en_rango:
                    torre.activar_habilidad(ficha_en_rango["unidad"])
            else:
                # La básica (dispara dos veces) y la mágica (congela)
                # solo afectan a la unidad más cercana
                torre.activar_habilidad(objetivo)


# Esta parte hace que las unidades activen su habilidad especial.
# Unidad ya tiene un método que cuenta los turnos y la activa sola
# cada 3 turnos (intentar_habilidad), pero nadie lo estaba llamando
# todavía. Por eso, aunque el código de las habilidades ya existía,
# nunca se estaban usando en el juego.
def activar_habilidades_unidades(unidades_en_juego):
    mensajes = []  # guarda lo que diga cada habilidad que se activó
    for ficha in unidades_en_juego:  # revisa una por una todas las unidades en la partida
        unidad = ficha["unidad"]  # saca la unidad de su ficha para trabajar con ella
        if not unidad.viva:
            continue  # si ya murió, no intenta nada
        resultado = unidad.intentar_habilidad()  # la unidad decide sola si le toca usar su habilidad este turno
        if resultado is not None:  # si se activó algo, la unidad devuelve un mensaje; si no, devuelve None
            mensajes.append(resultado)
    return mensajes  # al final devuelve todos los mensajes para mostrarlos en pantalla

#Ganancia de dinero por daños.............................
DINERO_POR_DAÑAR_TORRE_O_BASE = 5
DINERO_EXTRA_POR_DESTRUIR_TORRE = 20


# Esta función le da dinero al defensor por cada unidad enemiga que
# haya muerto. La cantidad depende del tipo de unidad: le damos la
# mitad de lo que costaba comprarla. También se encarga de sacar de
# la lista a las unidades que ya murieron, para no cobrarlas dos veces
# en un turno futuro.
def dinero_defensor_por_muertes(unidades_en_juego):
    dinero_ganado = 0
    vivas = []
    for ficha in unidades_en_juego:
        unidad = ficha["unidad"]
        if unidad.viva:
            vivas.append(ficha)  # sigue viva, se queda en la lista
        else:
            dinero_ganado += unidad.costo // 2  # ya murió, se cobra y se deja afuera

    unidades_en_juego[:] = vivas  # la lista original se actualiza solo con las que quedaron vivas
    return dinero_ganado


# Esta función le da dinero al atacante por dañar o destruir torres.
# Para saber si una torre recibió daño este turno, comparamos su vida
# de antes contra su vida de ahora. Por eso necesita el diccionario
# vidas_antes, que hay que armar justo antes de mover unidades y
# disparar torres, guardando cuánta vida tenía cada una en ese momento.
def dinero_atacante_por_torres(torres_en_juego, vidas_antes):
    dinero_ganado = 0
    for ficha_torre in torres_en_juego:
        torre = ficha_torre["torre"]
        vida_anterior = vidas_antes.get(id(torre))
        if vida_anterior is None:
            continue  # si no se guardó su vida antes, no se cobra nada por seguridad

        if torre.vida_actual < vida_anterior:
            dinero_ganado += DINERO_POR_DAÑAR_TORRE_O_BASE  # le pegaron, gana dinero
            if torre.esta_destruida():
                dinero_ganado += DINERO_EXTRA_POR_DESTRUIR_TORRE  # además la destruyeron

    return dinero_ganado


# Misma idea que con las torres, pero para la base central.
# vida_base_antes es la vida que tenía la base antes del turno.
def dinero_atacante_por_base(base, vida_base_antes):
    if base.vida_actual < vida_base_antes:
        return DINERO_POR_DAÑAR_TORRE_O_BASE
    return 0

#turno completo.............
# Esta función ejecuta un turno completo, llamando todo lo de arriba
# en orden: primero disparan las torres, luego se mueven las unidades,
# luego activan su habilidad si les toca, y al final se reparte el
# dinero y se revisa si alguien ganó la ronda.
def ejecutar_turno(tablero, base, torres_en_juego, unidades_en_juego, dinero_atacante_actual):
    vida_base_antes = base.vida_actual
    vidas_torres_antes = {id(ft["torre"]): ft["torre"].vida_actual for ft in torres_en_juego}

    disparar_torres(torres_en_juego, unidades_en_juego)
    mover_unidades(tablero, unidades_en_juego)
    mensajes_habilidades = activar_habilidades_unidades(unidades_en_juego)

    dinero_ganado_defensor = dinero_defensor_por_muertes(unidades_en_juego)
    dinero_ganado_atacante = dinero_atacante_por_torres(torres_en_juego, vidas_torres_antes)
    dinero_ganado_atacante += dinero_atacante_por_base(base, vida_base_antes)

    # se suma lo que ya tenía el atacante con lo que ganó este turno,
    # para saber si ya le alcanza para seguir jugando
    dinero_atacante_total = dinero_atacante_actual + dinero_ganado_atacante
    ganador_ronda = verificar_victoria_ronda(base, dinero_atacante_total, unidades_en_juego)

    return {
        "dinero_ganado_defensor": dinero_ganado_defensor,
        "dinero_ganado_atacante": dinero_ganado_atacante,
        "mensajes_habilidades": mensajes_habilidades,
        "ganador_ronda": ganador_ronda,
    }