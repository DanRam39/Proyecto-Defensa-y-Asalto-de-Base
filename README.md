# Defensa y Asalto de Base

Juego de estrategia por turnos en Python con interfaz gráfica usando Tkinter. Dos jugadores se enfrentan en una partida asimétrica donde uno defiende una base y el otro ataca con unidades móviles.

## Descripción general

- El defensor construye torres y muros sobre el tablero.
- El atacante coloca unidades en las últimas columnas para avanzar hacia la base.
- Cada ronda tiene una fase de construcción, una fase de despliegue de unidades y una fase de combate.
- La partida termina cuando un jugador alcanza 3 victorias en rondas.

## Requisitos

- Python 3.8 o superior.
- Tkinter (normalmente incluido en Python estándar).

## Ejecución

1. Abre una terminal en la carpeta del proyecto.
2. Ejecuta:

```bash
python main.py
```

## Flujo de juego

1. Se inicia la aplicación y los jugadores inician sesión o se registran.
2. Se elige un tema visual: Medieval, Futurista o Acuático.
3. Se asignan los roles de defensor y atacante.
4. El defensor coloca torres y muros en el tablero.
5. El atacante coloca unidades en las columnas de entrada del lado derecho.
6. Al iniciar el combate, cada turno se ejecuta automáticamente:
   - las torres disparan a unidades en alcance,
   - la base dispara si hay unidades cerca,
   - las unidades atacantes se mueven o atacan según el camino disponible,
   - se activan habilidades especiales cada 3 turnos,
   - se calcula el dinero ganado por ambos bandos.
7. La ronda termina cuando la base es destruida o el atacante se queda sin dinero y sin unidades vivas.

## Unidades atacantes

### Soldado
- Costo: 50
- Vida: 80
- Daño: 15
- Velocidad: 1
- Habilidad: cada 3 turnos activa "Ataque Doble" y golpea el doble de daño una vez.

### Tanque
- Costo: 120
- Vida: 250
- Daño: 30
- Velocidad: 1
- Habilidad: cada 3 turnos activa "Escudo" y el siguiente ataque no le hace daño.

### Unidad Rápida
- Costo: 70
- Vida: 60
- Daño: 10
- Velocidad: 2
- Habilidad: cada 3 turnos activa "Turbo" y aumenta su velocidad en 2 puntos por ese turno.

## Defensas del defensor

### Torre Básica
- Costo: 60
- Vida: 100
- Daño: 15
- Alcance: 3
- Habilidad: cada cierto número de turnos dispara dos veces al mismo objetivo.

### Torre Pesada
- Costo: 120
- Vida: 200
- Daño: 25
- Alcance: 2
- Habilidad: hace daño adicional a las unidades enemigas en rango.

### Torre Mágica
- Costo: 100
- Vida: 80
- Daño: 10
- Alcance: 3
- Habilidad: congela a la unidad atacada, reduciendo su movimiento en el siguiente turno.

### Muro
- Costo: 20
- Vida: 50
- Función: bloquea el avance de unidades enemigas y sirve como barrera de defensa.

### Base
- Vida inicial: 200
- Daño: 20
- Alcance: 2
- Función: ataca a la unidad enemiga más cercana dentro de su alcance. Si se destruye, el atacante gana la ronda.

## Condiciones de victoria

- Gana el atacante si destruye la base enemiga.
- Gana el defensor si el atacante se queda sin unidades vivas y sin dinero para desplegar más.
- El primer jugador que llega a 3 rondas ganadas gana la partida.

## Temas visuales

El proyecto soporta al menos tres temas:

- `Medieval`
- `Futurista`
- `Acuático`

Cada tema cambia los colores, y el juego puede usar imágenes específicas para torres, base, muros y unidades.

## Estructura de archivos

- `main.py`: punto de entrada del juego.
- `ventanas.py`: controla menus, pantallas y navegación entre fases.
- `tablero.py`: representa el tablero y dibuja las celdas en Tkinter.
- `defensa.py`: define `Base` y `Torre`.
- `atacantes.py`: define las clases `Soldado`, `Tanque` y `Rapida`.
- `combate.py`: contiene toda la lógica de combate, movimiento y dinero.
- `usuarios.py`: maneja login, registro y datos de usuarios.
- `ranking.py`: guarda y muestra el ranking de jugadores.
- `temas.py`: define los colores y nombres de los temas.
- `imagenes.py/`: carpeta con recursos gráficos para cada tema y para las unidades.

## Detalles técnicos

- Las unidades atacantes se colocan solo en las últimas columnas del tablero.
- Las torres y muros del defensor se pueden colocar en cualquier celda vacía durante la fase de construcción.
- Durante el combate, las unidades atacantes usan un algoritmo BFS para encontrar el camino a la estructura defensiva más cercana y, cuando ya no quedan torres ni muros, atacan la base.
- El sistema de dinero recompensa al atacante por dañar o destruir torres y la base, y al defensor por matar unidades enemigas.

