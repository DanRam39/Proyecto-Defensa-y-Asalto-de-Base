#Acá se trabajan las temáticas del juego 

#aquí se agregan los colores de cada facción 
TEMAS = {
    "Medieval": {
        "torre": "#8B4513",
        "muro": "#A0522D",
        "unidad": "#D2691E",
        "base": "#6B3410",
        "fondo": "#F5DEB3"
    },
    "Futurista": {
        "torre": "#00BFFF",
        "muro": "#1C1C2E",
        "unidad": "#7DF9FF",
        "base": "#0A0A1A",
        "fondo": "#E0F7FF"
    },
    "Naturaleza": {
        "torre": "#228B22",
        "muro": "#556B2F",
        "unidad": "#90EE90",
        "base": "#145214",
        "fondo": "#F0FFF0"
    }
}

# Esta funcion busca el tema que el usuario quiere 
def obtener_tema(nombre):
    return TEMAS.get(nombre, TEMAS["Medieval"]) #utiliza uno predeterminado en caso de que no se seleccione ninguno

# Retorna la lista de nombres de facciones disponibles
def listar_temas():
    return list(TEMAS.keys())

# Valida que el atacante y defensor no elijan lo mismo 
def validar_facciones(faccion_defensor, faccion_atacante):
    return faccion_defensor != faccion_atacante #verificación 