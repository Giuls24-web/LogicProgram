print("EL AHORCADO")
#Temática (Animales, Deportes, Lenguajes de Programación)
Dibujo= [" | "," | ", "/", "O", " \ "," | ", "/", " \ " ]
i=0
a=0
print("Tenemos Diferentes Temáticas")
print("1. Animales")
print("2. Deportes")
print("3. Lenguaje de Programación")
Palabra=int(input("Elije un número: "))

if Palabra==1:
 Animales=("Perro", "Gato", "Gallina", "Pato", "Serpiente", "Ganzo", "Camello")
 Palabra=str("Perro")
elif Palabra==2:
 Deportes=("Futbol", "Basket", "Tennis","Badminton", "Volleyball", "Beisbol")
 Letra=str("Basket")
else: 
 Lenguajes_de_Programación=("C++", "Java", "Python", "Ruby", "HTML")
 Palabra=str("Python")

while True:  # Bucle infinito controlado por condiciones internas
    Letra = input("Escribe una letra: ")
    if Letra == "p" or Letra == "e" or Letra == "r" or Letra == "o":
        a += 1
        print(a)
        print(f"¡TIENES SUERTE! Tu letra fue: {Letra}")
        if a >= 5:  # Condición de victoria
            print("¡GANASTE! Llegaste a 5 letras correctas.")
            break
    else:
        i += 1
        print("MALA SUERTE!")
        if i >= 8:  # Condición de derrota
            print("¡PERDISTE! Llegaste a 8 intentos incorrectos.")
            break