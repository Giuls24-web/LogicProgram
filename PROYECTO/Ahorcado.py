print("EL AHORCADO")
#Temática (Animales, Deportes, Lenguajes de Programación)
Dibujo= ["  |  ","  |  ", "  O  "," /|\ ", "  |  "," / \  "]
i=0
a=0
print("Tenemos Diferentes Temáticas")
print("1. Animales")
print("2. Deportes")
print("3. Lenguaje de Programación")
Palabra=int(input("Elije un número: "))

#Condicional para la elección de temática
if Palabra==1:
 Palabra=int(input("Escribe un número del 1-7: "))
 Animales=("Perro", "Gato", "Gallina", "Pato", "Serpiente", "Ganzo", "Camello")
 Palabra=Animales[Palabra]
elif Palabra==2:
 Palabra=int(input("Escribe un número del 1-6: "))
 Deportes=("Futbol", "Basket", "Tennis","Badminton", "Volleyball", "Beisbol")
 Palabra=Deportes[Palabra]
else: 
 Palabra=int(input("Escribe un número del 1-6: "))
 Lenguajes_de_Programación=("C++", "Java", "Python", "Ruby", "HTML")
 Palabra=Lenguajes_de_Programación[Palabra]

while True:  # Bucle infinito controlado por condiciones internas
    Letra = input("Escribe una letra: ")
    if Letra in Palabra:
        a += 1
        print(a)
        print(f"¡TIENES SUERTE! Tu letra fue: {Letra}")
        if a >= 5:  # Condición de victoria
            print(f"¡GANASTE! Tu pallabra es {Palabra}")
            break
    else:
        i += 1
        print("MALA SUERTE")
        for j in range(i):
          print(Dibujo[j])
        if i >= 5:  # Condición de derrota
             print(f"¡PERDISTE!.La palabra es: {Palabra}")
             for j in range(6):
              print(Dibujo[j])
             break