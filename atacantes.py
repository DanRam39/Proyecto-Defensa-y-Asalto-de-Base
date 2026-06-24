#Acá se trabaja la clase base unidad, así como también las clases dependientes: soldado, tanque, rápida. 

#aquí se guardan los datos básicos que tiene cada unidad 
class Unidad:
    def __init__(self, nombre, costo, vida, daño, velocidad):
        self.nombre = nombre
        self.costo = costo
        self.vida_maxima = vida
        self.vida_actual = vida
        self.daño = daño
        self.velocidad = velocidad
        self.turno_habilidad = 3  # la habilidad se activa cada 3 turnos
        self.turnos_jugados = 0
        self.viva = True

#tiene la función de restar vida y si llega a 0 se muere 
    def recibir_daño(self, cantidad):
        self.vida_actual = max(0, self.vida_actual - cantidad)
        if self.vida_actual <= 0:
            self.viva = False

#lo que hace es mover la unidad a la izquierda restando columnas según la velocidad. 
    def mover(self, fila, col):
        # Avanza hacia la base (hacia la izquierda en el mapa)
        return fila, col - self.velocidad

#habilidad especial 
    def activar_habilidad(self):
        pass  # cada subclase define la suya

#suma de turnos 
    def intentar_habilidad(self):
        self.turnos_jugados += 1 #suma un turno y al pasar 3 activa la habilidad especial 
        if self.turnos_jugados % self.turno_habilidad == 0:
            return self.activar_habilidad()
        return None


#creación del soldado con sus características
class Soldado(Unidad):
    def __init__(self):
        super().__init__(
            nombre="Soldado",
            costo=50,
            vida=80,
            daño=15,
            velocidad=1
        ) #este es el más corriente y barato

#pega el doble de daño por este turno
    def activar_habilidad(self):
        self.daño *= 2 
        return f"{self.nombre} activa Ataque Doble: daño duplicado este turno."


#creación del tanque 
class Tanque(Unidad):
    def __init__(self):
        super().__init__(
            nombre="Tanque",
            costo=120, 
            vida=250,
            daño=30,
            velocidad=1 #es nuy lento 
        ) 
        self.escudo_activo = False #arranca sin el escudo puesto

#su habilidad es prender el escudo  para no verse afectado por el ataque siguiente
    def activar_habilidad(self): 
        self.escudo_activo = True
        return f"{self.nombre} activa Escudo: ignorará el próximo ataque."

#se cambia la forma en que recibe el daño cuando el escudo está activo ignorando el golpe
    def recibir_daño(self, cantidad):
        if self.escudo_activo:
            self.escudo_activo = False
            return  # ignora el daño
        super().recibir_daño(cantidad)


#esta unidad es muy rápida pero tiene muy poca vida 
class Rapida(Unidad):
    def __init__(self):
        super().__init__(
            nombre="Unidad Rápida",
            costo=70,
            vida=60,
            daño=10,
            velocidad=2
        )
#su habilidad especial es meter turbo para correr 
    def activar_habilidad(self):
        self.velocidad += 2
        return f"{self.nombre} activa Turbo: velocidad aumentada este turno."