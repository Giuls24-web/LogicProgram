# Importaciones necesarias para el funcionamiento del programa
import tkinter as tk        # Biblioteca para la interfaz gráfica
from tkinter import messagebox, ttk  # Componentes de interfaz adicionales
import json                # Para almacenar y cargar palabras
import random             # Para selección aleatoria de palabras
from unicodedata import normalize    # Para manejo de tildes

# Número máximo de intentos permitidos antes de perder el juego
INTENTOS_MAXIMOS = 6

# Lista de estados del ahorcado en ASCII art
# Cada elemento representa un estado del juego, desde la horca vacía hasta el ahorcado completo
# El índice de la lista corresponde al número de errores del jugador
AHORCADO = [
r"""
  +---+
  |   |
      |
      |
      |
      |
=========""",  # Estado inicial: solo la horca
r"""
  +---+
  |   |
  O   |
      |
      |
      |
=========""",  # Estado 1: cabeza
r"""
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",  # Estado 2: cabeza y torso
r"""
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",  # Estado 3: cabeza, torso y brazo izquierdo
r"""
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========""",  # Estado 4: cabeza, torso y brazos
r"""
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========""",  # Estado 5: cabeza, torso, brazos y pierna izquierda
r"""
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
========="""]  # Estado 6: ahorcado completo

class VentanaInicio:
    """
    Clase principal que maneja la ventana de inicio del juego.
   
    Esta clase es responsable de:
    - Mostrar el menú principal con los botones de jugar, administrar y salir
    - Gestionar la navegación entre diferentes ventanas
    - Manejar el inicio y cierre de ventanas del juego

    Nota: En versión final se agregarán funcionalidades adicionales de administración
    """
    def __init__(self):
        # Configuración inicial de la ventana principal
        self.root = tk.Tk()
        self.root.title("Bienvenido al Juego del Ahorcado")
       
        # Frame principal para contener todos los elementos
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0)

        # Configuración del estilo del título
        style = ttk.Style()
        style.configure("Green.TLabel", foreground="green", font=('Helvetica', 16, 'bold'))
       
        # Elementos de la interfaz
        titulo = ttk.Label(main_frame,
                          text="JUEGO DEL AHORCADO",
                          style="Green.TLabel")
        titulo.grid(row=0, column=0, pady=20)
       
        # Botones del menú principal
        btn_jugar = ttk.Button(main_frame,
                              text="JUGAR",
                              command=self.iniciar_juego,
                              width=20)
        btn_jugar.grid(row=1, column=0, pady=10)
       
        btn_admin = ttk.Button(main_frame,
                              text="ADMINISTRAR",
                              command=self.administrar,
                              width=20)
        btn_admin.grid(row=2, column=0, pady=10)
       
        btn_salir = ttk.Button(main_frame,
                              text="SALIR",
                              command=self.root.quit,
                              width=20)
        btn_salir.grid(row=3, column=0, pady=10)

    def center_window(self):
        """
        Centra la ventana en la pantalla del usuario.
        Calcula la posición basada en el tamaño de la pantalla.
        """
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def iniciar_juego(self):
        """
        Inicia una nueva partida del juego.
        Oculta la ventana principal y muestra la ventana del juego.
        """
        self.root.withdraw()
        game_window = tk.Toplevel()
        game_window.geometry("800x600")
        game_window.title("Juego del Ahorcado")
        app = AhorcadoGUI(game_window, self)
        app.crear_interfaz()
        game_window.protocol("WM_DELETE_WINDOW", lambda: self.cerrar_juego(game_window))

    def administrar(self):
        """
        Abre la ventana de administración de palabras.
        Nota: Funcionalidad básica implementada, pendiente sistema completo
        """
        self.root.withdraw() # Oculta ventana principal
        admin_window = tk.Toplevel()
        admin_window.title("Administración de Palabras")
        admin_window.geometry("400x500")
        app = AhorcadoGUI(admin_window, self)
        app.mostrar_admin()

    def cerrar_juego(self, game_window):
        """
        Maneja el cierre correcto de la ventana del juego.
        Restaura la ventana principal al cerrar el juego.
        """
        game_window.destroy()
        self.root.deiconify()

    def iniciar(self):
        """
        Inicia la aplicación:
        - Centra la ventana
        - Inicia el loop principal de la interfaz
        """
        self.center_window()
        self.root.mainloop()

class AhorcadoGUI:
    """
    Clase principal del juego que maneja toda la lógica e interfaz del juego.
   
    Esta clase es responsable de:
    - Manejar el estado del juego (palabra, intentos, letras usadas)
    - Procesar la entrada del usuario
    - Actualizar la interfaz según el progreso
    - Gestionar las palabras disponibles
    """
    def __init__(self, root, ventana_inicio=None):
        """
        Inicializa una nueva instancia del juego.
       
        Args:
            root: Ventana principal del juego
            ventana_inicio: Referencia a la ventana de inicio para navegación
        """
        self.root = root
        self.ventana_inicio = ventana_inicio

        # Variables para el estado del juego
        self.palabra_secreta = "" # Palabra que el jugador debe adivinar
        self.letras_adivinadas = [] # Lista de letras descubiertas
        self.intentos_restantes = INTENTOS_MAXIMOS # Intentos disponibles
        self.letras_usadas = set() # Conjunto de letras ya utilizadas
       
        self.palabra_var = tk.StringVar() # Muestra la palabra con guiones
        self.letras_usadas_var = tk.StringVar() # Muestra letras ya intentadas
        self.intentos_var = tk.StringVar() # Muestra intentos restantes
        self.ahorcado_var = tk.StringVar() # Muestra el dibujo actual
       
        self.palabras = self.cargar_palabras() # Carga inicial de palabras

    def crear_interfaz(self):
        """
        Crea todos los elementos visuales del juego.
        Organiza los elementos usando un sistema de grid.
        """
        # Frame principal que contiene todos los elementos
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
       
        # Palabra oculta - Muestra los guiones y letras adivinadas
        ttk.Label(self.main_frame,
                 textvariable=self.palabra_var,
                 font=('Courier', 24)).grid(row=0, column=0, columnspan=2, pady=20)
       
        # Campo para ingresar letras
        ttk.Label(self.main_frame, text="Ingresa una letra:").grid(row=1, column=0, pady=10)
        self.letra_entry = ttk.Entry(self.main_frame, width=5)
        self.letra_entry.grid(row=1, column=1, pady=10)
        # Vincula la tecla Enter para procesar la letra
        self.letra_entry.bind('<Return>', lambda e: self.procesar_letra())
       
        # Botón para intentar o probar la letra o probar
        ttk.Button(self.main_frame,
                  text="Intentar",
                  command=self.procesar_letra).grid(row=2, column=0, columnspan=2, pady=10)
       
        # Muestra las letras ya utilizadas
        ttk.Label(self.main_frame, text="Letras usadas:").grid(row=3, column=0, pady=10)
        ttk.Label(self.main_frame, textvariable=self.letras_usadas_var).grid(row=3, column=1, pady=10)
       
        # Muestra los intentos restantes
        ttk.Label(self.main_frame, textvariable=self.intentos_var).grid(row=4, column=0, columnspan=2, pady=10)
       
        # Muestra el dibujo del ahorcado
        ttk.Label(self.main_frame,
                 textvariable=self.ahorcado_var,
                 font=('Courier', 14)).grid(row=5, column=0, columnspan=2, pady=10)
                 
        self.iniciar_juego()
       
    def cargar_palabras(self): # En construccion no funcional
        try:
            with open('palabras.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return ["python", "programacion", "computadora"]
   
    def guardar_palabras(self): # En construccion no funcional
        with open('palabras.json', 'w', encoding='utf-8') as f:
            json.dump(self.palabras, f, ensure_ascii=False)
   
    def mostrar_admin(self): # En construccion no funcional
        # Frame principal para administración
        admin_frame = ttk.Frame(self.root, padding="10")
        admin_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        # Lista de palabras
        self.palabra_listbox = tk.Listbox(admin_frame, width=40, height=15)
        self.palabra_listbox.grid(row=0, column=0, columnspan=2, pady=10)
       
        for palabra in self.palabras:
            self.palabra_listbox.insert(tk.END, palabra)    
        # Botones de administración
        ttk.Button(admin_frame,
                  text="Volver al Menú",
                  command=self.volver_menu).grid(row=1, column=0, columnspan=2, pady=20)
   
    def volver_menu(self): # En construccion no funcional
        if self.ventana_inicio:
            self.root.destroy()
            self.ventana_inicio.root.deiconify()

    def iniciar_juego(self):
        """
        Inicia una nueva partida:
        - Selecciona una palabra aleatoria
        - Reinicia los intentos y letras usadas
        - Prepara la interfaz del juego
        """
        if not self.palabras:
            messagebox.showerror("Error", "No hay palabras disponibles")
            return
       
        self.palabra_secreta = random.choice(self.palabras)
        self.letras_adivinadas = ["_"] * len(self.palabra_secreta)
        self.intentos_restantes = INTENTOS_MAXIMOS
        self.letras_usadas = set()
        self.actualizar_interfaz()
        self.letra_entry.focus()

    def procesar_letra(self):
        """
        Procesa cada intento del jugador.
        """
        # Obtiene y normaliza la letra ingresada
        letra = normalize('NFKD', self.letra_entry.get().lower().strip())
        self.letra_entry.delete(0, tk.END)
       
        if not letra or len(letra) != 1 or not letra.isalpha():
            messagebox.showwarning("Error", "Por favor ingresa una sola letra.")
            return
       
        if letra in self.letras_usadas:
            messagebox.showinfo("Aviso", "Ya usaste esa letra.")
            return
       
        # Procesa la letra
        self.letras_usadas.add(letra)
       
        if letra in self.palabra_secreta:
             # Actualiza las posiciones donde aparece la letra
            for i in range(len(self.palabra_secreta)):
                if self.palabra_secreta[i] == letra:
                    self.letras_adivinadas[i] = letra
            messagebox.showinfo("¡Bien!", "¡La letra está en la palabra!")
        else:
            self.intentos_restantes -= 1
            messagebox.showinfo("¡Oh no!", "La letra no está en la palabra")
       
        # Actualiza la interfaz y verifica el estado del juego
        self.actualizar_interfaz()
        self.verificar_juego()
        self.letra_entry.focus()

    def actualizar_interfaz(self):
        """
        Actualiza todos los elementos visuales del juego.
        """
        self.palabra_var.set(" ".join(self.letras_adivinadas))
        self.letras_usadas_var.set(" ".join(sorted(self.letras_usadas)))
        self.intentos_var.set(f"Intentos restantes: {self.intentos_restantes}")
        self.ahorcado_var.set(AHORCADO[6 - self.intentos_restantes])

    def verificar_juego(self):
        """
        Verifica si el juego ha terminado.
        """
        if "_" not in self.letras_adivinadas:
            messagebox.showinfo("¡Felicitaciones!", "¡Ganaste!")
            if messagebox.askyesno("Nuevo Juego", "¿Quieres jugar otra vez?"):
                self.iniciar_juego()
            else:
                self.volver_menu()
        elif self.intentos_restantes == 0:
            messagebox.showinfo("Game Over", "¡Perdiste!")
            if messagebox.askyesno("Nuevo Juego", "¿Quieres intentar otra vez?"):
                self.iniciar_juego()
            else:
                self.volver_menu()

if __name__ == "__main__":
    app = VentanaInicio()
    app.iniciar()