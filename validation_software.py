import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import random

# Crear ventana principal
root = tk.Tk()
root.title("Color Selector")

# Función para actualizar la imagen en "Image 1"
def update_image():
    selected = selected_color.get()  # Obtener el color seleccionado
    if selected:  # Si hay un color seleccionado
        image_path = os.path.join(vita_dir, f"{selected}.png")
        if os.path.exists(image_path):  # Verificar que el archivo existe
            # Cargar la imagen con transparencia
            img = Image.open(image_path).convert("RGBA")
            img = img.resize((100, 100), Image.Resampling.LANCZOS)

            # Convertir a formato Tkinter
            img_tk = ImageTk.PhotoImage(img)

            # Limpiar el canvas antes de agregar una nueva imagen
            placeholder_1.delete("all")
            placeholder_1.create_image(0, 0, anchor="nw", image=img_tk)  # Dibujar la imagen
            placeholder_1.image = img_tk  # Guardar referencia para evitar garbage collection
        else:
            placeholder_1.delete("all")  # Limpiar el canvas si no hay imagen
            placeholder_1.create_text(50, 50, text="Image 1")  # Mostrar texto si no hay imagen
    else:
        placeholder_1.delete("all")  # Limpiar el canvas si no hay selección
        placeholder_1.create_text(50, 50, text="Image 1")

def load_vita_images():
    """Carga todas las imágenes de vita_tooth y las prepara para mostrar aleatoriamente."""
    global vita_images
    vita_images = []

    # Buscar imágenes en el directorio de vita_tooth
    for filename in os.listdir(vita_dir):
        if filename.endswith(".png"):
            image_path = os.path.join(vita_dir, filename)
            img = Image.open(image_path).convert("RGBA")  # Cargar con transparencia
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            vita_images.append((filename, ImageTk.PhotoImage(img)))  # Guardar el nombre y la imagen

    # Barajar las imágenes al inicio
    random.shuffle(vita_images)

def show_next_image():
    """Muestra la siguiente imagen aleatoria en Image 2."""
    global current_index
    if vita_images:  # Asegurarse de que la lista no esté vacía
        current_index += 1
        if current_index >= len(vita_images):  # Si se acabaron las imágenes, volver a empezar
            current_index = 0
            random.shuffle(vita_images)  # Barajar de nuevo

        # Obtener la imagen actual
        _, img_tk = vita_images[current_index]

        # Mostrar la imagen en el canvas
        placeholder_2.delete("all")
        placeholder_2.create_image(0, 0, anchor="nw", image=img_tk)
        placeholder_2.image = img_tk  # Guardar referencia para evitar garbage collection


def validate_first_column():
    """Valida que los Combobox y Sliders de la primera columna estén llenos."""
    all_valid = True

    # Validar que todos los Combobox tengan un valor distinto del inicial
    for combo in first_column_comboboxes:
        if combo.get() == " ":  # Valor predeterminado
            all_valid = False
            break

    # Validar que todos los Sliders tengan un valor mayor a 0
    if all_valid:  # Solo seguir si los Combobox son válidos
        for scale in first_column_scales:
            if scale.get() == 0.0:  # Slider en su posición inicial
                all_valid = False
                break

    # Habilitar o deshabilitar el botón "Next" según la validación
    next_button.config(state="normal" if all_valid else "disabled")

def reset_all_inputs():
    """Reinicia todos los Combobox y Sliders."""
    # Reiniciar todos los Combobox
    for combo in all_comboboxes:
        combo.set(" ")  # Valor inicial

    # Reiniciar todos los Sliders
    for scale in all_scales:
        scale.set(0)  # Valor inicial

def show_next_image():
    """Muestra la siguiente imagen aleatoria en Image 2 y reinicia los valores."""
    global current_index
    if vita_images:  # Asegurarse de que la lista no esté vacía
        current_index += 1
        if current_index >= len(vita_images):  # Si se acabaron las imágenes, volver a empezar
            current_index = 0
            random.shuffle(vita_images)  # Barajar de nuevo

        # Obtener la imagen actual
        _, img_tk = vita_images[current_index]

        # Mostrar la imagen en el canvas
        placeholder_2.delete("all")
        placeholder_2.create_image(0, 0, anchor="nw", image=img_tk)
        placeholder_2.image = img_tk  # Guardar referencia para evitar garbage collection

    # Reiniciar todos los valores de Combobox y Sliders
    reset_all_inputs()




# Crear el frame principal para los colores
frame = tk.Frame(root)
frame.pack(pady=10, padx=10)

# Crear las imágenes y asignar checkboxes
color_labels = ["A1", "A2", "A3", "A3_5", "A4", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4", "D2", "D4"]
image_dir = os.path.join(os.getcwd(), "Datasets", "reference_colors")  # Directorio de imágenes iniciales
vita_dir = os.path.join(os.getcwd(), "Datasets", "vita_tooth")  # Directorio de imágenes para 'Image 1'
image_files = [f"{label}.png" for label in color_labels]

# Cargar imágenes
images = [tk.PhotoImage(file=os.path.join(image_dir, image)) for image in image_files]

# Variable compartida para los checkboxes
selected_color = tk.StringVar(value="")  # Mantendrá el valor del checkbox seleccionado

# Crear los contenedores para imágenes y checkboxes
for idx, (color, img) in enumerate(zip(color_labels, images)):
    col_frame = tk.Frame(frame)  # Frame para cada imagen y checkbox
    col_frame.grid(row=0, column=idx, padx=5, pady=5)

    # Imagen
    img_label = tk.Label(col_frame, image=img)
    img_label.pack()

    # Radiobutton debajo de la imagen
    chk = tk.Radiobutton(
        col_frame, 
        text=color, 
        variable=selected_color, 
        value=color, 
        command=update_image  # Llamar a la función al seleccionarlo
    )
    chk.pack()

# Crear un marco principal para organizar el centro y la derecha
main_center_frame = tk.Frame(root)
main_center_frame.pack(pady=20, padx=20)

# Crear el área para las imágenes centrales
center_frame = tk.Frame(main_center_frame)
center_frame.grid(row=0, column=0, padx=10)

# Reducir espaciadores superiores para bajar las imágenes
tk.Label(center_frame, height=7).grid(row=0, column=0, columnspan=2)  # Reducimos la altura del espaciador

# Placeholder para "Image 1"
placeholder_1 = tk.Canvas(center_frame, width=100, height=100, bg="SystemButtonFace", highlightthickness=0)
placeholder_1.grid(row=1, column=0, padx=10, pady=10)

# Placeholder para "Image 2" (no modificado)
placeholder_2 = tk.Canvas(center_frame, width=100, height=100, bg="SystemButtonFace", highlightthickness=0)
placeholder_2.grid(row=1, column=1, padx=10, pady=10)

# Botones y checkboxes debajo de las imágenes centrales
buttons_frame = tk.Frame(center_frame)
buttons_frame.grid(row=2, column=0, columnspan=2, pady=10)

next_button = tk.Button(buttons_frame, text="Next", command=show_next_image)
next_button.grid(row=0, column=0, columnspan=2, pady=5)

tk.Checkbutton(buttons_frame, text="Reference Color").grid(row=1, column=0, padx=10)
tk.Checkbutton(buttons_frame, text="Reference Tooth").grid(row=1, column=1, padx=10)

tk.Button(buttons_frame, text="Reset all").grid(row=2, column=0, columnspan=2, pady=5)

# Crear los sliders con comboboxes a la derecha de las imágenes centrales
sliders_frame = tk.Frame(main_center_frame)
sliders_frame.grid(row=0, column=1, padx=20)

# Crear listas globales para almacenar referencias a los Combobox y Sliders
all_comboboxes = []  # Todos los Combobox
all_scales = []      # Todos los Sliders

# Crear listas específicas para la primera columna (para validación)
first_column_comboboxes = []
first_column_scales = []

# Nombres de las filas
row_names = ["Upper Tooth", "Central Tooth", "Lower Tooth"]

# Crear los sliders en filas correspondientes
for row_idx, row_name in enumerate(row_names):
    # Etiqueta para cada fila
    row_label = tk.Label(sliders_frame, text=row_name, font=("Arial", 10, "bold"))
    row_label.grid(row=row_idx, column=0, padx=10, pady=5)

    # Añadir sliders y comboboxes en columnas correspondientes
    for col_idx in range(3):  # Tres columnas de sliders y comboboxes por fila
        slider_frame = tk.Frame(sliders_frame)
        slider_frame.grid(row=row_idx, column=col_idx + 1, padx=10, pady=5)

        # Combobox
        combo = ttk.Combobox(slider_frame, values=color_labels, width=4, state="readonly")
        combo.set(" ")  # Valor inicial
        combo.pack()
        all_comboboxes.append(combo)  # Guardar referencia global

        if col_idx == 0:  # Primera columna
            first_column_comboboxes.append(combo)

        # Slider
        scale = tk.Scale(slider_frame, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL)
        scale.pack()
        all_scales.append(scale)  # Guardar referencia global

        if col_idx == 0:  # Primera columna
            first_column_scales.append(scale)

# Deshabilitar el botón "Next" al inicio
next_button.config(state="disabled")

# Asociar validación a eventos
for combo in first_column_comboboxes:
    combo.bind("<<ComboboxSelected>>", lambda e: validate_first_column())

for scale in first_column_scales:
    scale.bind("<ButtonRelease-1>", lambda e: validate_first_column())
    scale.bind("<Motion>", lambda e: validate_first_column())

vita_images = []
current_index = -1

# Cargar las imágenes al inicio
load_vita_images()

# Mostrar la primera imagen aleatoria
show_next_image()

# Ejecutar la interfaz
root.mainloop()
