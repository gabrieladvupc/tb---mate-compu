import tkinter as tk
from tkinter import filedialog, ttk
import cv2
import numpy as np
from PIL import Image, ImageTk

class Filtroimg:
    def __init__(self, root):
        self.root = root
        self.root.title("Betterimg")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        self.imagen_original = 0
        self.imagen_actual = 0
        self.tamano_kernel = tk.StringVar(value="3")  

        self.crear_widgets()
        
    def crear_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.crear_pagina_inicio()
        self.crear_pagina_funcionamiento()
        self.crear_pagina_suavizado()
        self.crear_pagina_integrantes()


    def crear_pagina_inicio(self):
        marco_portada = tk.Frame(self.notebook, bg="#7FFFD4")  # verde agua
        self.notebook.add(marco_portada, text="Portada")

        etiqueta_titulo = tk.Label(marco_portada, text="BETTERIMG",
                                   font=("Cal Sans", 48, "bold"),
                                   fg="white", bg="#7FFFD4")
        etiqueta_titulo.pack(pady=50)

        etiqueta_subtitulo = tk.Label(marco_portada, text="App para filtrado de imágenes",
                                      font=("Cal Sans", 30),
                                      fg="white", bg="#7FFFD4")
        etiqueta_subtitulo.pack(pady=10)

        boton1 = tk.Button(marco_portada, text="Funcionamiento",
                           command=lambda: self.notebook.select(1),
                           fg="white", bg="#5AC8B3")
        boton1.pack(pady=10)

        boton2 = tk.Button(marco_portada, text="Filtros de Suavizado",
                           command=lambda: self.notebook.select(2),
                           fg="white", bg="#5AC8B3")
        boton2.pack(pady=10)

        boton3 = tk.Button(marco_portada, text="Integrantes",
                           command=lambda: self.notebook.select(3),
                           fg="white", bg="#5AC8B3")
        boton3.pack(pady=10)
    
    def crear_pagina_funcionamiento(self):
        marco_conceptos = ttk.Frame(self.notebook)
        self.notebook.add(marco_conceptos, text="Funcionamiento")
        
        widget_texto = tk.Text(marco_conceptos, wrap=tk.WORD, font=("Cal sans", 11))
        widget_texto.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        barra_desplazamiento = ttk.Scrollbar(widget_texto)
        barra_desplazamiento.pack(side=tk.RIGHT, fill=tk.Y)
        widget_texto.config(yscrollcommand=barra_desplazamiento.set)
        barra_desplazamiento.config(command=widget_texto.yview)
        
        widget_texto.insert(tk.END, "BIENVENIDO A BETTERIMG\n\n", "titulo")
        widget_texto.tag_config("titulo", font=("Arial", 14, "bold"))

        widget_texto.insert(tk.END, """BetterIMG: Mejora de imágenes clínicas al alcance de tu mano
                            

BetterIMG es una aplicación cuyo objetivo es ayudar a mejorar la calidad de 
imágenes médicas mediante filtros de suavizado,
facilitando así el diagnóstico y análisis clínico. 

Filtros que usa BetterIMG:

1. Filtro de Mediana en BetterIMG
   Cuando trabajas con radiografías óseas, el filtro de Mediana de BetterIMG elimina eficazmente 
   el ruido tipo "sal y pimienta" que aparece durante la captura. 
   Al utilizar este filtro, notarás cómo se preservan los bordes de los huesos de las fracturas, 
   proporcionando una imagen más limpia y nitida para el diagnóstico.

2. Filtro de Media en BetterIMG
   Para imágenes de resonancia magnética cerebral donde hay dificultad en la visualización de estructuras
   cerebrales complejas, el filtro de media que ofrece BetterIMG, permite que imágenes como 
   de los ventrículos cerebrales y otros tejidos blandos se aprecien con mayor facilidad. 

BetterIMG funciona en 5 simples pasos:

Paso 1: Carga tu imagen - Presiona el botón "Cargar imagen" y selecciona cualquier imagen médica de tu dispositivo. 
        BetterIMG admite formatos JPG, JPEG y PNG comúnmente usados en entornos clínicos.

Paso 2: Presiona el botón "Filtro de media" para suavizar tu imagen. Pese a su pérdida de nitidez, 
        es ideal para resonancias magnéticas 
        y otras imágenes donde necesites reducir el ruido general 
        manteniendo una buena visualización de los tejidos blandos.


Paso 3: Haz click en "Filtro de mediana" para eliminar ruidos puntuales preservando los bordes.
        Perfecto para radiografías, tomografías y cualquier imagen donde visualizar los bordes y 
        detalles finos sean cruciales.

Paso 4: Selecciona el botón "restaurar la imagen" para volver a visualizar la imagen original.

Paso 5: Finalmente, presiona en "Guardar imagen" para almacenar la imagen mejorada
        en tu dispositivo, lista para incluirla en informes médicos o presentaciones.

BetterIMG: Mejora la visualización de tus diagnósticos desde un solo click.
""")
        
        widget_texto.config(state=tk.DISABLED)  
    
    def crear_pagina_suavizado(self):
        marco_suavizado = ttk.Frame(self.notebook)
        self.notebook.add(marco_suavizado, text="Filtros de Suavizado")
        
        marco_control = ttk.LabelFrame(marco_suavizado, text="Controles")
        marco_control.pack(fill=tk.X, padx=10, pady=10)

        boton_cargar = ttk.Button(marco_control, text="Cargar Imagen", command=self.cargar_imagen)
        boton_cargar.pack(side=tk.LEFT, padx=5, pady=10)
        
        marco_kernel = ttk.Frame(marco_control)
        marco_kernel.pack(side=tk.LEFT, pady=10, padx=20)
        
        ttk.Label(marco_kernel, text="Tamaño del Kernel:").pack(side=tk.LEFT, padx=5)
        
        tamanos_kernel = [3, 5, 7, 9, 11]
        
        self.tamano_kernel = tk.StringVar()
        self.tamano_kernel.set("3")  
        
        combo_kernel = ttk.Combobox(marco_kernel, textvariable=self.tamano_kernel,
                                  values=tamanos_kernel, width=5)
        combo_kernel.pack(side=tk.LEFT, padx=5)
        
        marco_filtro = ttk.Frame(marco_control)
        marco_filtro.pack(side=tk.LEFT, pady=10, padx=20)
        
        ttk.Button(marco_filtro, text="Filtro de media",
                  command=self.aplicar_filtro_media).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(marco_filtro, text="Filtro de mediana",
                  command=self.aplicar_filtro_mediana).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(marco_filtro, text="Restaurar imagen",
                  command=self.restaurar_imagen).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(marco_filtro, text="Guardar imagen",
                  command=self.guardar_imagen).pack(side=tk.LEFT, padx=5)
        
        self.etiqueta_estado = ttk.Label(marco_control, text="Seleccionar imagen:")
        self.etiqueta_estado.pack(side=tk.RIGHT, padx=10)
        
        self.marco_imagenes = ttk.Frame(marco_suavizado)
        self.marco_imagenes.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.marco_original = ttk.LabelFrame(self.marco_imagenes, text="Imagen Original")
        self.marco_original.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.marco_filtrada = ttk.LabelFrame(self.marco_imagenes, text="Imagen Filtrada")
        self.marco_filtrada.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.label_imagen_original = ttk.Label(self.marco_original)
        self.label_imagen_original.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.label_imagen_filtrada = ttk.Label(self.marco_filtrada)
        self.label_imagen_filtrada.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def crear_pagina_integrantes(self):
        marco_integrantes = ttk.Frame(self.notebook)
        self.notebook.add(marco_integrantes, text="Integrantes")
        
        etiqueta_titulo = ttk.Label(marco_integrantes, text="INTEGRANTES:", 
                               font=("Cal sans", 16, "bold"))
        etiqueta_titulo.pack(pady=20)
        
        integrantes = [
            "Integrante 1 - Durand Gabriela",
            "Integrante 2 - Gamboa Diego",
            "Integrante 3 - Medina Magaly",
            "Integrante 4 - Palacios Sebastian",
            "Integrante 5 - Soto Diego",
        ]
        
        for i, integrante in enumerate(integrantes):
            ttk.Label(marco_integrantes, text=f"{i+1}. {integrante}", 
                     font=("Arial", 12)).pack(pady=10)
    
    def cargar_imagen(self):
        ruta_archivo = filedialog.askopenfilename(
            filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png *.bmp")]
        )
        
        if ruta_archivo:
            self.imagen_original = cv2.imread(ruta_archivo)
            if self.imagen_original is None:
                return
            
            self.imagen_original = cv2.cvtColor(self.imagen_original, cv2.COLOR_BGR2RGB)
            self.imagen_actual = self.imagen_original.copy()
            
            self.mostrar_en_gui(self.imagen_original, self.label_imagen_original)
            self.etiqueta_estado.config(text=f"Imagen subida: {ruta_archivo.split('/')[-1]}")
    
    def mostrar_en_gui(self, imagen, label):
        if imagen is 0:
            return
        
        ancho_label = label.winfo_width()
        alto_label = label.winfo_height()
        
        if ancho_label <= 1:
            ancho_label = 400
            alto_label = 300
        
        alto, ancho = imagen.shape[:2]
        ratio = min(ancho_label/ancho, alto_label/alto)
        nuevo_ancho = int(ancho * ratio)
        nuevo_alto = int(alto * ratio)
        
        imagen_redim = cv2.resize(imagen, (nuevo_ancho, nuevo_alto))
        
        img_pil = Image.fromarray(imagen_redim)
        img_tk = ImageTk.PhotoImage(image=img_pil)
        
        label.image = img_tk
        label.config(image=img_tk)
    
    def aplicar_filtro_media(self):
        if self.imagen_original is 0:
            return
        
        t_kernel = int(self.tamano_kernel.get())  # Convert StringVar to int
        
        altura, ancho = self.imagen_original.shape[:2]
        resultado = self.imagen_original.copy()  
        
        radio = int(t_kernel / 2)  
        
        for y in range(radio, altura - radio):
            for x in range(radio, ancho - radio):
                for c in range(3):
                    fila_inicio = y - radio
                    fila_fin = y + radio + 1  
                    
                    columna_inicio = x - radio
                    columna_fin = x + radio + 1
                    
                    vecinos = self.imagen_original[fila_inicio:fila_fin, columna_inicio:columna_fin, c]
                    
                    suma = 0
                    for fila in vecinos:
                        for valor in fila:
                            suma += valor
                    media = suma / (t_kernel * t_kernel)
                    
                    resultado[y, x, c] = media
        
        self.imagen_actual = resultado
        self.mostrar_en_gui(self.imagen_actual, self.label_imagen_filtrada)
        self.etiqueta_estado.config(text="Filtro de media aplicado")
    
    def aplicar_filtro_mediana(self):
        if self.imagen_original is 0:
            return
        
        t_kernel = int(self.tamano_kernel.get())  
        
        altura, ancho = self.imagen_original.shape[:2]
        resultado = self.imagen_original.copy() 
        
        radio = int(t_kernel / 2) 
        
        for y in range(radio, altura - radio):
            for x in range(radio, ancho - radio):
                for c in range(3):
                    fila_inicio = y - radio
                    fila_fin = y + radio + 1  
                    
                    columna_inicio = x - radio
                    columna_fin = x + radio + 1
                    
                    vecinos = self.imagen_original[fila_inicio:fila_fin, columna_inicio:columna_fin, c]
                    
                    lista_vecinos = []
                    for fila in vecinos:
                        for valor in fila:
                            lista_vecinos.append(valor)
                    
                    lista_vecinos.sort()  
                    mediana = lista_vecinos[len(lista_vecinos) // 2]  
                    
                    resultado[y, x, c] = mediana
        
        self.imagen_actual = resultado
        self.mostrar_en_gui(self.imagen_actual, self.label_imagen_filtrada)
        self.etiqueta_estado.config(text="Filtro de mediana aplicado")
    
    def restaurar_imagen(self):
        if self.imagen_original is not 0:
            self.imagen_actual = self.imagen_original.copy()
            self.mostrar_en_gui(self.imagen_actual, self.label_imagen_filtrada)
            self.etiqueta_estado.config(text="La imagen fue restaurada")
    
    def guardar_imagen(self):
        if self.imagen_actual is 0:
            return
        
        ruta_guardado = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                   filetypes=[("Archivos de imagen", "*.jpg *.jpeg *.png *.bmp")])
        
        if ruta_guardado:
            imagen_bgr = cv2.cvtColor(self.imagen_actual, cv2.COLOR_RGB2BGR)
            cv2.imwrite(ruta_guardado, imagen_bgr)
            self.etiqueta_estado.config(text=f"Imagen guardada como: {ruta_guardado.split('/')[-1]}")
    
if __name__ == "__main__":
    root = tk.Tk()
    app = Filtroimg(root)
    root.mainloop()