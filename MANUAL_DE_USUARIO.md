# Manual de Usuario

Este manual explica cómo usar el juego "Defensa y Asalto de Base" desde cero. Está pensado para personas que no tienen experiencia previa con Python ni con este proyecto.

---

## 1. Requisitos

Antes de ejecutar el juego, necesitas tener instalado:

- Python 3.8 o superior.
- Tkinter, que generalmente se instala junto con Python.

### Cómo verificar que Python está instalado

1. Abre la aplicación Terminal o PowerShell en Windows.
2. Escribe:

```bash
python --version
```

3. Si aparece una versión como `Python 3.8.x` o superior, ya tienes Python instalado.
4. Si recibes un error, instala Python desde https://www.python.org/downloads/ y marca la opción "Add Python to PATH" durante la instalación.

### Cómo verificar Tkinter

1. Abre Terminal o PowerShell.
2. Escribe:

```bash
python -m tkinter
```

3. Si se abre una ventana pequeña, Tkinter funciona correctamente.
4. Si aparece un error, puede que la instalación de Python no incluya Tkinter. Instala Python nuevamente con la opción completa.

---

## 2. Preparar los archivos del juego

1. Descarga o clona el repositorio en una carpeta de tu computadora.
2. Asegúrate de que los archivos principales estén en la misma carpeta, por ejemplo:
   - `main.py`
   - `ventanas.py`
   - `tablero.py`
   - `defensa.py`
   - `atacantes.py`
   - `combate.py`
   - `usuarios.py`
   - `ranking.py`
   - `temas.py`
   - Carpeta `imagenes.py` con recursos gráficos.

---

## 3. Ejecutar el juego

1. Abre Terminal o PowerShell.
2. Cambia la carpeta de trabajo a la carpeta del proyecto. Por ejemplo:

```bash
cd "C:\Users\TuUsuario\Desktop\Proyecto-Defensa-y-Asalto-de-Base"
```

3. Ejecuta el juego con este comando:

```bash
python main.py
```

4. Se abrirá una ventana con el menú principal del juego.

---

## 4. Navegación del juego

### Menú principal

Al iniciar, verás opciones como:

- `Jugar`: comienza una nueva partida.
- `Ranking`: muestra los mejores jugadores.
- `Salir`: cierra el juego.

### Inicio de sesión y registro

1. El jugador 1 debe iniciar sesión con su usuario y contraseña.
2. El jugador 2 hace lo mismo.
3. Si no tienes usuario, selecciona `Registrarse` y crea uno nuevo.
4. El juego no permite que ambos jugadores usen el mismo usuario.

### Selección de tema visual

Después del login, debes elegir un tema para la partida:

- Medieval
- Futurista
- Acuático

Este tema cambia colores e imágenes dentro del juego.

---

## 5. Roles y rondas

El juego se divide en rondas. En cada ronda:

1. Se asigna quién es el defensor y quién es el atacante.
2. El defensor coloca estructuras para proteger su base.
3. El atacante coloca unidades para atacar.
4. Se inicia el combate y se resuelve el turno.
5. El primero que gane 3 rondas gana la partida.

---

## 6. Fase de construcción (para el defensor)

En esta fase el defensor puede comprar y colocar:

- Torre Básica (60 de costo)
- Torre Pesada (120 de costo)
- Torre Mágica (100 de costo)
- Muro (20 de costo)

### Cómo colocar

1. Haz clic en el botón de la estructura que quieras.
2. Haz clic en una celda vacía del tablero.
3. El dinero se resta automáticamente.
4. No puedes colocar sobre una celda que ya esté ocupada.

### Consejos

- Las torres atacan a unidades enemigas que estén dentro de su alcance.
- Los muros bloquean el paso de las unidades.
- La base también puede disparar cuando las unidades enemigas se acercan.

---

## 7. Fase de ataque (para el atacante)

En esta fase el atacante puede comprar unidades y colocarlas en las columnas de entrada al tablero.

Unidades disponibles:

- Soldado (50 de costo)
- Tanque (120 de costo)
- Unidad Rápida (70 de costo)

### Cómo colocar

1. Selecciona la unidad que deseas comprar.
2. Haz clic en una celda vacía dentro de las últimas columnas del tablero.
3. El dinero se resta automáticamente.
4. Solo puedes colocar unidades en la zona de entrada indicada.

### Consejos

- El soldado es barato y equilibrado.
- El tanque es lento, pero resiste más daño.
- La unidad rápida avanza más lejos por turno.

---

## 8. Combate

Cuando el atacante termina su fase, el juego entra en modo combate.

### Qué sucede en cada turno de combate

1. Las torres disparan a las unidades enemigas dentro de su alcance.
2. La base dispara a la unidad enemiga más cercana si está dentro de alcance.
3. Las unidades atacantes se mueven y atacan.
4. Las habilidades especiales de las unidades se activan cada 3 turnos.
5. Se actualiza el dinero ganado por ambos jugadores.

### Cómo termina la ronda

La ronda termina cuando:

- El atacante destruye la base del defensor.
- El atacante se queda sin unidades vivas y sin dinero para comprar más.

---

## 9. Ganar la partida

- El atacante gana una ronda si destruye la base del defensor.
- El defensor gana una ronda si el atacante no tiene más unidades y no puede comprar más.
- El primero en alcanzar 3 rondas ganadas gana la partida.

---

## 10. Preguntas frecuentes

### ¿Qué hago si no veo la ventana del juego?

- Revisa que el comando `python main.py` se haya ejecutado sin errores.
- Asegúrate de estar en la carpeta correcta del proyecto.

### ¿Qué hago si aparece un error de importación?

- Comprueba que todos los archivos `.py` estén dentro de la carpeta del proyecto.
- Verifica que no cambiaste los nombres de los archivos.

### ¿Qué hago si no puedo colocar una unidad o torre?

- Verifica que tengas el dinero suficiente.
- Asegúrate de que la celda esté vacía.
- En el caso del atacante, solo coloca en las últimas columnas.

---

## 11. Guardar resultados

El juego registra el ranking de jugadores con victorias. Después de cada partida, podrás ver el ranking desde el menú principal.

---

## 12. Cerrar el juego

Para cerrar el juego, usa el botón `Salir` en el menú principal o cierra la ventana de la aplicación.
