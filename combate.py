#aquí se trabaja la lógica del combate 

from defensa import Base , Torre 
torres_en_juego = [] #guarda cada torre puesta en el mapa junto con su fila y columna 
#se creó esta nueva clase ya que hacia falta para que las unidades tengan algo contra que chocar al moverse

from collections import deque

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

def obstaculo_mas_cercano(tablero, fila, columna):
    # Revisa las 4 celdas vecinas y devuelve la que tenga un obstáculo
    # destructible (muro o torre), junto con su posición. Si ninguna
    # vecina tiene nada que atacar, devuelve None.
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for delta_fila, delta_columna in movimientos:
        fila_vecina = fila + delta_fila
        columna_vecina = columna + delta_columna

        if not tablero.celda_valida(fila_vecina, columna_vecina):
            continue

        obstaculo = hay_obstaculo(tablero, fila_vecina, columna_vecina)
        if obstaculo is not None:
            return fila_vecina, columna_vecina, obstaculo

    return None

from collections import deque

def encontrar_siguiente_paso(tablero, fila_inicio, columna_inicio, fila_base, columna_base):
    # Primero revisa si hay una torre o muro adyacente para atacar directamente
    # Las unidades prefieren atacar obstáculos cercanos antes de moverse
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for df, dc in movimientos:
        fv, cv = fila_inicio + df, columna_inicio + dc
        if not tablero.celda_valida(fv, cv):
            continue
        obj = tablero.obtener(fv, cv)
        if isinstance(obj, (Torre, Muro)):
            return None  # hay torre/muro adyacente, que ataque en vez de moverse

    # Si no hay torres/muros adyacentes, BFS hacia la base
    inicio = (fila_inicio, columna_inicio)
    destino = (fila_base, columna_base)

    if inicio == destino:
        return None

    cola = deque([inicio])
    visitadas = {inicio: None}

    encontrado = False
    while cola:
        actual = cola.popleft()
        if actual == destino:
            encontrado = True
            break
        fa, ca = actual
        for df, dc in movimientos:
            vecina = (fa + df, ca + dc)
            fv, cv = vecina
            if vecina in visitadas:
                continue
            if not tablero.celda_valida(fv, cv):
                continue
            obj = tablero.obtener(fv, cv)
            if obj is not None and vecina != destino:
                continue
            visitadas[vecina] = actual
            cola.append(vecina)

    if not encontrado:
        return None

    paso_actual = destino
    while visitadas[paso_actual] != inicio:
        paso_actual = visitadas[paso_actual]
    return paso_actual

def mover_unidades(tablero, unidades_en_juego, fila_base, columna_base):
    for ficha in unidades_en_juego:
        unidad = ficha["unidad"]

        if not unidad.viva:
            continue

        if unidad.velocidad_congelada:
            unidad.descongelar()
            continue

        fila_actual = ficha["fila"]
        columna_actual = ficha["columna"]

        for _ in range(unidad.velocidad):
            if not unidad.viva:
                break

            # Primero revisa si hay torre o muro adyacente para atacar
            ataco = False
            movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for df, dc in movimientos:
                fv, cv = fila_actual + df, columna_actual + dc
                if not tablero.celda_valida(fv, cv):
                    continue
                obj = tablero.obtener(fv, cv)
                if isinstance(obj, (Torre, Muro)):
                    obj.recibir_daño(unidad.daño)
                    if obj.esta_destruida():
                        tablero.quitar(fv, cv)
                    ataco = True
                    break  # ataca solo uno por paso

            if ataco:
                break  # si atacó, no se mueve este paso

            # Si no atacó, intenta moverse con BFS
            siguiente_paso = encontrar_siguiente_paso(
                tablero, fila_actual, columna_actual, fila_base, columna_base
            )

            if siguiente_paso is None:
                # Completamente bloqueada o ya en la base
                obstaculo_cercano = obstaculo_mas_cercano(tablero, fila_actual, columna_actual)
                if obstaculo_cercano is not None:
                    fila_obs, columna_obs, objeto_obs = obstaculo_cercano
                    objeto_obs.recibir_daño(unidad.daño)
                    if objeto_obs.esta_destruida():
                        tablero.quitar(fila_obs, columna_obs)
                break

            fila_destino, columna_destino = siguiente_paso
            tablero.quitar(fila_actual, columna_actual)
            tablero.colocar(fila_destino, columna_destino, unidad)
            fila_actual, columna_actual = fila_destino, columna_destino

        ficha["fila"] = fila_actual
        ficha["columna"] = columna_actual

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
    dinero_ganado_defensor = 0
    for ficha_torre in torres_en_juego:
        torre = ficha_torre["torre"]
        if torre.esta_destruida():
            continue

        en_rango = unidades_en_rango(
            ficha_torre["fila"], ficha_torre["columna"],
            torre.alcance, unidades_en_juego)
        if not en_rango:
            continue

        objetivo_ficha = ficha_mas_cercana(
            ficha_torre["fila"], ficha_torre["columna"], en_rango)
        objetivo = objetivo_ficha["unidad"]
        vida_antes = objetivo.vida_actual

        objetivo.recibir_daño(torre.daño)

        if objetivo.vida_actual < vida_antes:
            dinero_ganado_defensor += DINERO_POR_GOLPE  # +10 por golpe

        if torre.puede_activar_habilidad():
            if torre.tipo == "pesada":
                for ficha_en_rango in en_rango:
                    torre.activar_habilidad(ficha_en_rango["unidad"])
            else:
                torre.activar_habilidad(objetivo)

    return dinero_ganado_defensor


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
# Constantes de dinero
DINERO_POR_GOLPE = 10
DINERO_POR_DESTRUIR = "costo"  # se usa el costo real del objeto


def dinero_defensor_por_muertes(unidades_en_juego):
    # Solo cuenta el dinero, NO elimina las unidades muertas
    # Las unidades muertas se mantienen en la lista para persistir entre rondas
    # (el tablero ya las quitó visualmente cuando murieron)
    dinero_ganado = 0
    for ficha in unidades_en_juego:
        unidad = ficha["unidad"]
        if not unidad.viva:
            dinero_ganado += unidad.costo
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
            continue
        if torre.vida_actual < vida_anterior:
            dinero_ganado += DINERO_POR_GOLPE  # +10 por cada golpe
            if torre.esta_destruida():
                dinero_ganado += torre.costo  # +costo de la torre al destruirla
    return dinero_ganado


# Misma idea que con las torres, pero para la base central.
# vida_base_antes es la vida que tenía la base antes del turno.
def dinero_atacante_por_base(base, vida_base_antes):
    if base.vida_actual < vida_base_antes:
        return DINERO_POR_GOLPE  # +10 por golpear la base
    return 0

#turno completo.............
# Esta función ejecuta un turno completo, llamando todo lo de arriba
# en orden: primero disparan las torres, luego se mueven las unidades,
# luego activan su habilidad si les toca, y al final se reparte el
# dinero y se revisa si alguien ganó la ronda.
def ejecutar_turno(tablero, base, torres_en_juego, unidades_en_juego, dinero_atacante_actual, fila_base, columna_base):
    vida_base_antes = base.vida_actual
    vidas_torres_antes = {id(ft["torre"]): ft["torre"].vida_actual for ft in torres_en_juego}

    dinero_ganado_defensor = disparar_torres(torres_en_juego, unidades_en_juego)
    mover_unidades(tablero, unidades_en_juego, fila_base, columna_base)
    mensajes_habilidades = activar_habilidades_unidades(unidades_en_juego)

    dinero_ganado_defensor += dinero_defensor_por_muertes(unidades_en_juego)
    dinero_ganado_atacante  = dinero_atacante_por_torres(torres_en_juego, vidas_torres_antes)
    dinero_ganado_atacante += dinero_atacante_por_base(base, vida_base_antes)

    dinero_atacante_total = dinero_atacante_actual + dinero_ganado_atacante
    ganador_ronda = verificar_victoria_ronda(base, dinero_atacante_total, unidades_en_juego)

    return {
        "dinero_ganado_defensor": dinero_ganado_defensor,
        "dinero_ganado_atacante": dinero_ganado_atacante,
        "mensajes_habilidades": mensajes_habilidades,
        "ganador_ronda": ganador_ronda,
    }

