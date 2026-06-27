TEMAS = {
    "Medieval": {
        "torre": "#8B4513", "muro": "#A0522D",
        "unidad": "#D2691E", "base": "#6B3410", "fondo": "#F5DEB3"
    },
    "Futurista": {
        "torre": "#00BFFF", "muro": "#1C1C2E",
        "unidad": "#7DF9FF", "base": "#0A0A1A", "fondo": "#E0F7FF"
    },
    "Acuático": {
        "torre": "#1E90FF", "muro": "#4682B4",
        "unidad": "#87CEEB", "base": "#00008B", "fondo": "#E0F8FF"
    },
}

def obtener_tema(nombre):
    return TEMAS.get(nombre, TEMAS["Medieval"])

def listar_temas():
    return list(TEMAS.keys())

def validar_facciones(faccion_defensor, faccion_atacante):
    return faccion_defensor != faccion_atacante