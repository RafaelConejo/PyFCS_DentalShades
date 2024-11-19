import tkinter as tk
from tkinter import ttk
import os

# Crear ventana principal
root = tk.Tk()
root.title("Color Selector")

# Crear el frame principal para los colores
frame = tk.Frame(root)
frame.pack(pady=10, padx=10)

# Crear las imágenes y asignar checkboxes
color_labels = ["A1", "A2", "A3", "A3_5", "A4", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4", "D2", "D4"]
image_dir = os.path.join(os.getcwd(), "Datasets", "reference_colors")  # Directorio de imágenes
image_files = [f"{label}.png" for label in color_labels]

# Cargar imágenes
images = [tk.PhotoImage(file=os.path.join(image_dir, image)) for image in image_files]

# Crear los contenedores para imágenes y checkboxes
for idx, (color, img) in enumerate(zip(color_labels, images)):
    col_frame = tk.Frame(frame)  # Frame para cada imagen y checkbox
    col_frame.grid(row=0, column=idx, padx=5, pady=5)

    # Imagen
    img_label = tk.Label(col_frame, image=img)
    img_label.pack()

    # Checkbox debajo de la imagen
    chk = tk.Checkbutton(col_frame, text=color)
    chk.pack()

# Crear los sliders con comboboxes
sliders_frame = tk.Frame(root)
sliders_frame.pack(pady=10)

slider_data = []
for i in range(9):
    row = i // 3
    col = i % 3
    slider_frame = tk.Frame(sliders_frame)
    slider_frame.grid(row=row, column=col, padx=10, pady=5)

    combo = ttk.Combobox(slider_frame, values=color_labels, width=4, state="readonly")
    combo.set("A1")
    combo.pack()

    scale = tk.Scale(slider_frame, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL)
    scale.pack()

# Crear el área de color de referencia
reference_frame = tk.Frame(root)
reference_frame.pack(pady=10)

tk.Label(reference_frame, text=" ").grid(row=0, column=0, padx=10)
tk.Label(reference_frame, text=" ").grid(row=0, column=1, padx=10)

# Botón Next
tk.Button(reference_frame, text="Next").grid(row=1, column=0, columnspan=2, pady=10)

# Checkboxes de referencia
options_frame = tk.Frame(root)
options_frame.pack(pady=5)

tk.Checkbutton(options_frame, text="Reference Color").grid(row=0, column=0, padx=10)
tk.Checkbutton(options_frame, text="Reference Tooth").grid(row=0, column=1, padx=10)

# Botón Reset
tk.Button(root, text="Reset all").pack(pady=10)

# Ejecutar la interfaz
root.mainloop()
