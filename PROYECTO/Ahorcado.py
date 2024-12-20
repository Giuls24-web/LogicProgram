import random

# Función para mostrar el menú de temáticas y permitir al usuario elegir una
# Retorna el número de la temática seleccionada
def mostrar_menu_tematicas():
    print("EL AHORCADO")
    print("Tenemos Diferentes Temáticas")
    print("1. Animales")
    print("2. Deportes")
    print("3. Lenguajes de Programación")
    return int(input("Elije un número: "))
 
# Función para elegir una palabra aleatoria de la temática seleccionada
# Retorna una palabra aleatoria de la categoría elegida
def elegir_palabra(tema):
    if tema == 1:
        opciones = ("Perro", "Gato", "Gallina", "Pato", "Serpiente", "Ganzo", "Camello")
    elif tema == 2:
        opciones = ("Futbol", "Basket", "Tennis", "Badminton", "Volleyball", "Beisbol")
    else:
        opciones = ("C++", "Java", "Python", "Ruby", "HTML")
    return random.choice(opciones)

# Función para mostrar el progreso actual de la palabra
# Retorna un string con las letras adivinadas y guiones bajos para las restantes
def mostrar_progreso(palabra, letras_adivinadas):
    progreso = ""
    for letra in palabra:
        if letra.upper() in letras_adivinadas:
            progreso += letra  # Agrega la letra si ha sido adivinada
        else:
            progreso += "_"  # Agrega un guion bajo si no ha sido adivinada
    return progreso

# Función principal del juego del ahorcado
# Parámetro: palabra (la palabra que debe adivinarse)
def jugar_ahorcado(palabra):
    dibujo = ('  |  ','  |  ', '  O  ',' /|\\', '  |  ',' / \\ ') # Representación gráfica del ahorcado
    intentos = 0 # Contador de intentos fallidos
    letras_adivinadas = [] # Lista para almacenar las letras ya adivinadas

    while True:
        # Mostrar el progreso actual de la palabra
        print(f"Palabra: {mostrar_progreso(palabra, letras_adivinadas)}")
        letra = input("Escribe una letra: ").upper()

        # Verificar si la letra ya fue adivinada
        if letra in letras_adivinadas:
            print(f"Ya adivinaste la letra '{letra}'. Intenta con otra.")
        elif letra in palabra.upper():
            letras_adivinadas.append(letra) # Añadir la letra a la lista de adivinadas
            print(f"¡TIENES SUERTE! La letra '{letra}' está en la palabra.")

            # Verificar si todas las letras de la palabra han sido adivinadas
            if all(letra.upper() in letras_adivinadas for letra in set(palabra.upper())):
                print(f"¡GANASTE! La palabra es {palabra}")
                return
        else:
            letras_adivinadas.append(letra) # Añadir la letra a la lista de intentos
            intentos += 1 # Incrementar el contador de intentos fallidos
            print(f"MALA SUERTE. La letra '{letra}' no está en la palabra.")
            # Mostrar la parte correspondiente del dibujo del ahorcado
            for j in range(intentos):
                print(dibujo[j])

            # Verificar si se han agotado los intentos
            if intentos >= len(dibujo):
                print(f"¡PERDISTE! La palabra era: {palabra}")
                for linea in dibujo:
                    print(linea) # Mostrar el dibujo completo
                return

# Función principal para gestionar el flujo del juego
def main():
    while True:
        tema = mostrar_menu_tematicas() # Mostrar el menú y obtener la temática seleccionada
        palabra = elegir_palabra(tema) # Elegir una palabra aleatoria de la temática seleccionada
        jugar_ahorcado(palabra) # Iniciar el juego con la palabra seleccionada

        # Preguntar al usuario si desea jugar nuevamente
        jugar_otra_vez = input("¿Quieres volver a jugar? (si/no): ").strip().lower()
        if jugar_otra_vez != "si":
            print("¡Gracias por jugar! Hasta la próxima.")
            break

# Punto de entrada del programa
if __name__ == "__main__":
    main()