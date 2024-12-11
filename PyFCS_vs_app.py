import os
import sys
import random
import tkinter as tk
from openpyxl import Workbook, load_workbook
from tkinter import ttk, simpledialog, messagebox
from PIL import Image, ImageTk
import pandas as pd
import ast
import time

current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)


############################################################ FUNTIONS ############################################################

def exit_fullscreen(event):
    root.attributes('-fullscreen', False)


def parse_column(cell):
    try:
        # Usar `ast.literal_eval` para evaluar la cadena de forma segura
        return ast.literal_eval(cell) if isinstance(cell, str) else cell
    except Exception as e:
        print(f"Error al parsear: {cell}. Error: {e}")
        return []


def update_counter_label():
    """Updates the counter label with the current file number."""
    counter_label.config(text=f"{current_file_index}/{total_files}")

def next_file():
    """Moves to the next file, if possible."""
    global current_file_index
    if current_file_index < total_files:
        current_file_index += 1
        update_counter_label()

def previous_file():
    """Moves to the previous file, if possible."""
    global current_file_index
    if current_file_index > 0:
        current_file_index -= 1
        update_counter_label()


def ask_user_name():
    """Asks the user to enter a name."""
    global user_name
    user_name = simpledialog.askstring("ID", "Enter user ID:")
    if not user_name:  # If the user doesn't enter anything
        messagebox.showerror("Error", "You must enter a name to continue.")
        ask_user_name()  # Ask for the name again


# Function to load the corresponding image from the selected options
def update_image_from_selection():
    global image_id1
    selected_label = selected_color.get()
    
    if not selected_label:
        shared_canvas.delete("image1")  # Borrar solo la imagen 1
        return
    
    directory = "Datasets/vita_tooth_test" if image_source.get() == "tooth" else "Datasets/reference_colors"
    new_size = (62,90) if directory == "Datasets/vita_tooth_test" else (50,50)
    image_path = os.path.join(directory, f"{selected_label}.png")
    
    if os.path.exists(image_path):
        img = Image.open(image_path).convert("RGBA").resize((new_size), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        shared_canvas.delete("image1")  # Borrar cualquier imagen previa
        shared_canvas.image1 = img_tk  # Guardar referencia
        image_id1 = shared_canvas.create_image(*coords_img1, image=img_tk, tag="image1")

        shared_canvas.bind("<ButtonPress-1>", on_image_press)
        shared_canvas.bind("<B1-Motion>", on_image_drag)
        shared_canvas.bind("<ButtonRelease-1>", on_image_release)
    else:
        shared_canvas.delete("image1")
        shared_canvas.create_text(*coords_img1, text=" ", tag="image1")


def on_image_press(event):
    global offset_x, offset_y
    # Guardar las coordenadas iniciales del clic dentro del Canvas
    offset_x = event.x
    offset_y = event.y

def on_image_drag(event):
    global offset_x, offset_y
    # Mover la imagen izquierda dentro del Canvas si el clic fue sobre ella
    canvas_items = shared_canvas.find_closest(event.x, event.y)
    if canvas_items and canvas_items[0] == image_id1:
        dx = event.x - offset_x
        dy = event.y - offset_y
        shared_canvas.move(image_id1, dx, dy)
        offset_x = event.x
        offset_y = event.y

def on_image_release(event):
    global original_position_left_image, image_id1
    # Volver a la posición original de la imagen izquierda
    shared_canvas.coords(image_id1, original_position_left_image[0], original_position_left_image[1])


# Function to update images according to the selected Radiobutton
def update_image_source():
    update_image_from_selection()


def load_vita_images():
    """Loads all vita_tooth images and prepares them for random display."""
    global vita_images
    vita_images = []

    # Search for images in the vita_tooth directory
    for filename in os.listdir(vita_dir):
        if filename.endswith(".png"):
            image_path = os.path.join(vita_dir, filename)
            img = Image.open(image_path).convert("RGBA")  # Load with transparency
            img = img.resize((62, 90), Image.Resampling.LANCZOS)
            vita_images.append((filename, ImageTk.PhotoImage(img)))  # Save the name and image

    # Shuffle images at the start
    random.shuffle(vita_images)        


def next_file_timer():
    global start_time
    if start_time is None:
        elapsed_time = 0
    else: 
        elapsed_time = time.time() - start_time
        start_time = time.time()  # Restart

    return elapsed_time


def load_image_for_tooth(tooth_name, img_frame):
    """Carga y muestra la imagen correspondiente para un diente dado."""
    global image_dir
    image_path = os.path.join(image_dir, f"{tooth_name}.png")

    # Verifica si la imagen existe
    if os.path.exists(image_path):
        try:
            # Carga la imagen y la redimensiona
            img = Image.open(image_path).convert("RGBA")
            img = img.resize((20, 20), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)

            # Inserta la imagen en un Label dentro del frame
            label = tk.Label(image_frames[img_frame], image=img_tk)
            label.image = img_tk  # Guarda una referencia para evitar que se recolecte por el GC
            label.pack(expand=True)  # Ajusta la posición en el frame
        except Exception as e:
            print(f"Error al cargar la imagen {image_path}: {e}")
            return None
    else:
        print(f"Advertencia: La imagen para {tooth_name} no existe en {image_dir}.")
        return None


def show_next_image():
    """Shows the next random image in Image 2 and resets the values."""
    global current_index, results_matrix, time_matrix

    # Save results of the current case
    if current_index >= 0:
        current_tooth = vita_images[current_index][0].split(".")[0]  # Get the tooth name

        update_results_matrix(current_tooth)
        update_comments_matrix(current_tooth)

        current_time = next_file_timer()
        row_index = color_labels.index(current_tooth)
        time_matrix[row_index] = current_time

    reset_all_inputs()
    # Move to the next index
    current_index += 1
    next_file()

    # If there are still images available
    if current_index < len(vita_images):  
        _, img_tk = vita_images[current_index]

        # Display the image on the canvas
        shared_canvas.delete("image2")  
        shared_canvas.image2 = img_tk  
        shared_canvas.create_image(*coords_img2, image=img_tk, tag="image2")

        # Restore saved values or reset inputs
        current_tooth = vita_images[current_index][0].split(".")[0] 
        current_idx_t = color_labels.index(current_tooth)
        current_row = data.iloc[current_idx_t]
        current_row_results = results_matrix[current_idx_t]

        top_values = current_row['top']    
        middle_values = current_row['middle']
        bottom_values = current_row['bottom']

        # Para "top"
        for idx in range(len(top_values)):  # Índices 0 a 2 para "top"
            if top_values[idx][1] <= 0.1:  # Verificar si el valor es menor o igual a 0.1
                all_static_texts[idx].config(text="")
                all_static_texts[idx].grid_forget()  # Ocultar texto
                for rb in all_radiobuttons[idx * 5: (idx + 1) * 5]:  # Ocultar botones (5 por fila)
                    rb.pack_forget()
            else:
                all_static_texts[idx].config(text=f"{top_values[idx][0]} -> {top_values[idx][1]}")
                load_image_for_tooth(top_values[idx][0], idx)

        # Ocultar elementos sobrantes si la longitud de top_values es menor que 3
        for idx in range(len(top_values), 3):
            all_static_texts[current_idx].config(text="")
            all_static_texts[idx].grid_forget()
            for rb in all_radiobuttons[idx * 5: (idx + 1) * 5]:
                rb.pack_forget()

        # Para "middle"
        for idx in range(len(middle_values)):  # Índices 3 a 5 para "middle"
            current_idx = idx + len(top_values)
            if middle_values[idx][1] <= 0.1:
                all_static_texts[current_idx].config(text="")
                all_static_texts[current_idx].grid_forget()
                for rb in all_radiobuttons[current_idx * 5: (current_idx + 1) * 5]:
                    rb.pack_forget()
            else:
                all_static_texts[current_idx].config(text=f"{middle_values[idx][0]} -> {middle_values[idx][1]}")
                load_image_for_tooth(middle_values[idx][0], current_idx)

        # Ocultar elementos sobrantes si la longitud de middle_values es menor que 3
        for idx in range(len(middle_values), 3):
            current_idx = idx + len(top_values)
            all_static_texts[current_idx].config(text="")
            all_static_texts[current_idx].grid_forget()
            for rb in all_radiobuttons[current_idx * 5: (current_idx + 1) * 5]:
                rb.pack_forget()

        # Para "bottom"
        for idx in range(len(bottom_values)):    # Índices 6 a 8 para "bottom"
            current_idx = idx + len(middle_values) + len(top_values)
            if bottom_values[idx][1] <= 0.1:
                all_static_texts[current_idx].config(text="")
                all_static_texts[current_idx].grid_forget()
                for rb in all_radiobuttons[current_idx * 5: (current_idx + 1) * 5]:
                    rb.pack_forget()
            else:
                all_static_texts[current_idx].config(text=f"{bottom_values[idx][0]} -> {bottom_values[idx][1]}")
                load_image_for_tooth(bottom_values[idx][0], current_idx)

        # Ocultar elementos sobrantes si la longitud de bottom_values es menor que 3
        for idx in range(len(bottom_values), 3):
            current_idx = idx + len(middle_values) + len(top_values)
            all_static_texts[current_idx].config(text="")
            all_static_texts[current_idx].grid_forget()
            for rb in all_radiobuttons[current_idx * 5: (current_idx + 1) * 5]:
                rb.pack_forget()

   
        
        if current_row_results and any(value is not None for value in current_row_results):
            restore_previous_values(current_tooth)
        

        # Update button states
        prev_button.config(state="normal" if current_index > 0 else "disabled")
        next_button.config(state="normal" if current_index < len(vita_images) - 1 else "disabled")
        update_image_from_selection()
        validate_visible()

    else:
        # All images have been shown, ask user if they want to finalize
        finalize = messagebox.askyesno("Finalize", "Your selections will be saved. Do you want to finalize?")
        if finalize:
            save_results_to_excel()
            save_time_to_excel()

            prev_button.config(state="disabled")
            next_button.config(state="disabled")  # Disable "Next"
            reset_button.config(state="normal")  # Enable "Reset all"
        else:
            current_index -= 1  # Return to the last index


def show_previous_image():
    """Shows the previous image and restores its values."""
    global current_index, results_matrix

    if current_index > 0:  # Prevent going to negative indices
        # Save current results
        current_tooth = vita_images[current_index][0].split(".")[0]

        current_idx = color_labels.index(current_tooth)
        if all(value is not None for value in results_matrix[current_idx]):  # Verifica si todos los valores son diferentes de -1
            update_results_matrix(current_tooth)
            update_comments_matrix(current_tooth)

        # Move to the previous index
        reset_all_inputs()
        current_index -= 1

        # Display the previous image
        _, img_tk = vita_images[current_index]
        shared_canvas.delete("image2")
        shared_canvas.image2 = img_tk
        shared_canvas.create_image(*coords_img2, image=img_tk, tag="image2")

        # Restore saved values or reset inputs
        current_tooth = vita_images[current_index][0].split(".")[0] 
        current_idx_t = color_labels.index(current_tooth)
        current_row = data.iloc[current_idx_t]

        top_values = current_row['top']    
        middle_values = current_row['middle']
        bottom_values = current_row['bottom']

        # Para "top"
        for idx in range(len(top_values)):  # Índices 0 a 2 para "top"
            if top_values[idx][1] <= 0.1:  # Verificar si el valor es menor o igual a 0.1
                all_static_texts[idx].config(text="")
                all_static_texts[idx].grid_forget()  # Ocultar texto
                for rb in all_radiobuttons[idx * 5: (idx + 1) * 5]:  # Ocultar botones (5 por fila)
                    rb.pack_forget()
            else:
                all_static_texts[idx].config(text=f"{top_values[idx][0]} -> {top_values[idx][1]}")
                load_image_for_tooth(top_values[idx][0], idx)

        # Ocultar elementos sobrantes si la longitud de top_values es menor que 3
        for idx in range(len(top_values), 3):
            all_static_texts[current_idx].config(text="")
            all_static_texts[idx].grid_forget()
            for rb in all_radiobuttons[idx * 5: (idx + 1) * 5]:
                rb.pack_forget()

        # Para "middle"
        for idx in range(len(middle_values)):  # Índices 3 a 5 para "middle"
            current_idx = idx + len(top_values)
            if middle_values[idx][1] <= 0.1:
                all_static_texts[current_idx].config(text="")
                all_static_texts[current_idx].grid_forget()
                for rb in all_radiobuttons[current_idx * 5: (current_idx + 1) * 5]:
                    rb.pack_forget()
            else:
                all_static_texts[current_idx].config(text=f"{middle_values[idx][0]} -> {middle_values[idx][1]}")
                load_image_for_tooth(middle_values[idx][0], current_idx)

        # Ocultar elementos sobrantes si la longitud de middle_values es menor que 3
        for idx in range(len(middle_values), 3):
            current_idx = idx + len(top_values)
            all_static_texts[current_idx].config(text="")
            all_static_texts[current_idx].grid_forget()
            for rb in all_radiobuttons[current_idx * 5: (current_idx + 1) * 5]:
                rb.pack_forget()

        # Para "bottom"
        for idx in range(len(bottom_values)):    # Índices 6 a 8 para "bottom"
            current_idx = idx + len(middle_values) + len(top_values)
            if bottom_values[idx][1] <= 0.1:
                all_static_texts[current_idx].config(text="")
                all_static_texts[current_idx].grid_forget()
                for rb in all_radiobuttons[current_idx * 5: (current_idx + 1) * 5]:
                    rb.pack_forget()
            else:
                all_static_texts[current_idx].config(text=f"{bottom_values[idx][0]} -> {bottom_values[idx][1]}")
                load_image_for_tooth(bottom_values[idx][0], current_idx)

        # Ocultar elementos sobrantes si la longitud de bottom_values es menor que 3
        for idx in range(len(bottom_values), 3):
            current_idx = idx + len(middle_values) + len(top_values)
            all_static_texts[current_idx].config(text="")
            all_static_texts[current_idx].grid_forget()
            for rb in all_radiobuttons[current_idx * 5: (current_idx + 1) * 5]:
                rb.pack_forget()

        restore_previous_values(current_tooth)
        update_image_from_selection()

    # Update button states
    prev_button.config(state="normal" if current_index > 0 else "disabled")
    next_button.config(state="normal" if current_index < len(vita_images) - 1 else "disabled")
    previous_file()



def restore_previous_values(current_tooth):
    """Restaura los valores de los Radiobuttons y textos para el diente actual o reinicia si no hay valores previos."""
    global results_matrix, comments_matrix

    try:
        # Recuperar el índice del diente en la lista de etiquetas
        current_index = color_labels.index(current_tooth)
    except ValueError:
        messagebox.showerror("Error", f"Tooth '{current_tooth}' not found in the list.")
        return


    current_row = data.iloc[current_index]
    current_comment_row = comments_matrix[current_index]

    top_values = current_row['top']    
    middle_values = current_row['middle']
    bottom_values = current_row['bottom']

    # Recuperar la fila correspondiente de la matriz de resultados
    current_row = results_matrix[current_index]

    # Comprobar si la fila tiene valores no nulos
    if current_row and any(value is not None for value in current_row):
        # Iterar por las 9 columnas de la fila (top, middle, bottom)
        for col_idx in range(9):  # 9 columnas por fila (3 para "top", 3 para "middle", 3 para "bottom")
            value = current_row[col_idx]

            # Verificar si hay un valor en la celda actual
            if value != -1:  # Si hay valor restaurado
                if col_idx < 3:
                    all_static_texts[col_idx].config(text=f"{top_values[col_idx][0]} -> {top_values[col_idx][1]}")
                elif col_idx >= 3 and col_idx < 6:
                    all_static_texts[col_idx].config(text=f"{middle_values[col_idx - 3][0]} -> {middle_values[col_idx - 3][1]}")
                else:
                    all_static_texts[col_idx].config(text=f"{bottom_values[col_idx - 6][0]} -> {bottom_values[col_idx - 6][1]}")

                # Restaurar el valor del Radiobutton
                radiobutton_values[col_idx].set(value)

                # Asegurarse de que los Radiobuttons sean visibles
                for rb in all_radiobuttons[col_idx * 5: (col_idx + 1) * 5]:  # 5 botones por fila
                    rb.pack(side=tk.LEFT)

        for col_comment in range(3):
            # Restaurar los comentarios en las casillas de texto correspondientes
            comment = current_comment_row[col_comment]
            additional_text_entries[col_comment].delete(0, tk.END)  # Limpiar el texto anterior
            additional_text_entries[col_comment].insert(0, comment if comment else "")


    else:
        # Si la fila está vacía o contiene solo None, restablecer todo
        reset_all_inputs()




def clear_comments():
    """Limpia las casillas de texto y resetea la matriz de comentarios."""
    global comments_matrix

    for entry in additional_text_entries:
        if isinstance(entry, tk.Entry):  # Asegurarse de que es una instancia de tk.Entry
            entry.delete(0, tk.END)  # Limpia el contenido de la casilla
        else:
            print(f"Advertencia: {entry} no es un tk.Entry") 



def validate_visible():
    """Validates that at least one Radiobutton in each visible row is selected."""
    all_valid = True  # Inicialmente asumimos que todos son válidos

    # Iterar por las variables asociadas a los Radiobuttons visibles
    for idx, rb_value in enumerate(radiobutton_values):
        # Si el texto relacionado con los Radiobuttons está oculto, ignorar
        if all_static_texts[idx].cget("text") != "":   # Verificar si la etiqueta es visible
            if rb_value.get() == -1:  # Ningún botón seleccionado
                all_valid = False
                break

    # Habilitar o deshabilitar el botón "Next" en función de la validación
    next_button.config(state="normal" if all_valid else "disabled")



def reset_all_inputs():
    """Resets all Radiobuttons to their initial state (value -1) and restores visibility."""
    clear_comments()

    # Restablecer todos los valores de los radiobuttons a -1 (deseleccionar)
    for rb_value in radiobutton_values:
        rb_value.set(-1)  # Restablecer a su valor inicial

    # Iterar sobre todos los índices de los textos estáticos y radiobuttons
    for idx in range(len(all_static_texts)):
        # Verificar si el texto está vacío (indicando que la fila está oculta)
        if all_static_texts[idx].cget("text") == "":  # Si el texto está vacío, restaurar la visibilidad
            # Hacer visibles los Radiobuttons si estaban ocultos
            for rb in all_radiobuttons[idx * 5: (idx + 1) * 5]:  # Considerando que hay 5 botones por fila
                if not rb.winfo_ismapped():  # Si el Radiobutton está oculto
                    rb.pack(side=tk.LEFT)  # Hacerlo visible de nuevo
            # También restaurar el texto si es necesario
            all_static_texts[idx].config(text="")  # Puedes poner el texto que desees aquí

        # Deseleccionar todos los Radiobuttons
        for rb in all_radiobuttons[idx * 5: (idx + 1) * 5]:
            rb.deselect()  # Deseleccionar los radiobuttons

        for frame in image_frames:
        # Destruir todos los widgets dentro del frame (incluidas las imágenes)
            for widget in frame.winfo_children():
                widget.destroy()




def reset_cycle():
    """Resets the image cycle and controls."""
    global current_index
    global user_name
    global current_file_index
    global start_time

    current_file_index = 0

    # Save results to Excel before resetting
    initialize_results_matrix()

    # Ask for the name again
    ask_user_name()
    start_time = time.time()

    # Shuffle images again
    random.shuffle(vita_images)  
    current_index = -1  # Reset index
    shared_canvas.delete("image2")  # Clear the second image canvas
    next_button.config(state="normal")  # Enable the "Next" button
    reset_button.config(state="disabled")  # Disable the "Reset all" button
    show_next_image()
    prev_button.config(state="disabled")


# Initialize results matrix with empty rows
def initialize_results_matrix():
    global results_matrix
    results_matrix = [[None] * 9 for _ in color_labels]  # 9 columns for each tooth

def initialize_comments_matrix():
    global comments_matrix
    comments_matrix = [[None] * 3 for _ in color_labels]  # 3 columns for each tooth

def initialize_time_matrix():
    global time_matrix
    time_matrix = [None for _ in color_labels]

def update_results_matrix(diente):
    """Updates the results matrix with the values from dropdowns and sliders."""
    global results_matrix

    try:
        row_idx = color_labels.index(diente)
    except ValueError:
        messagebox.showerror("Error", f"Diente '{diente}' no encontrado en la lista.")
        return

    for col_idx in range(9):  # 3 columnas: top, middle, bottom
        # Verificar si el conjunto de radiobuttons es visible
        if results_matrix[row_idx][col_idx] != -1:  # Si los radiobuttons están visibles
            # Obtener el valor seleccionado de los radiobuttons
            selected_value = radiobutton_values[col_idx].get()
            results_matrix[row_idx][col_idx] = selected_value


def update_comments_matrix(diente):
    """Actualiza la matriz de comentarios con los valores de las entradas de texto para el diente dado."""
    global comments_matrix

    try:
        # Obtener el índice de la fila del diente en la matriz
        row_idx = color_labels.index(diente)
    except ValueError:
        messagebox.showerror("Error", f"Diente '{diente}' no encontrado en la lista.")
        return

    # Recorrer las entradas de texto para el diente actual
    for col_idx, entry in enumerate(additional_text_entries):
        # Obtener y limpiar el texto de la entrada
        comment = entry.get().strip()
        # Guardar el comentario en la matriz, o `None` si está vacío
        comments_matrix[row_idx][col_idx] = comment if comment else None



def save_results_to_excel():
    """Saves the results matrix to an Excel file."""
    global user_name, comments_matrix, results_matrix

    # File and sheet
    file_name = "Results\PyFCS_Val_Results.xlsx"
    sheet_name = user_name

    # Create file if it doesn't exist
    if not os.path.exists(file_name):
        wb = Workbook()
        wb.save(file_name)

    # Load the existing file
    wb = load_workbook(file_name)

    # If the sheet already exists, add an incremental suffix
    original_sheet_name = sheet_name
    counter = 1
    while sheet_name in wb.sheetnames:
        sheet_name = f"{original_sheet_name}_{counter}"
        counter += 1

    # Create a new sheet
    ws = wb.create_sheet(title=sheet_name)

    # Add headers
    headers = [
        "Tooth",
        "UP_1", "UP_2", "UP_3", "U_Comment", 
        "CP_1", "CP_2", "CP_3", "C_Comment", 
        "LP_1", "LP_2", "LP_3", "L_Comment"
    ]
    ws.append(headers)

    # Write the data from the results_matrix to Excel
    for tooth_label, row_data, comment_row in zip(color_labels, results_matrix, comments_matrix):
            # Procesar valores numéricos
            numeric_values = [value if value != -1 else "" for value in row_data]
            
            # Procesar comentarios (dejar tal cual o reemplazar None por "")
            processed_comments = [comment if comment is not None else "" for comment in comment_row]

            # Combinar datos numéricos y comentarios
            full_row = numeric_values[:3] + [processed_comments[0]] + numeric_values[3:6] + [processed_comments[1]] + numeric_values[6:] + [processed_comments[2]]
            
            # Agregar fila al Excel
            ws.append([tooth_label] + full_row)

    # Save the file
    wb.save(file_name)
    messagebox.showinfo("Success", f"Results saved to {file_name}.")



def save_time_to_excel():
    """Saves the results Time matrix to an Excel file."""
    global user_name, time_matrix

    # Archivo y hoja
    file_name = "Results\PyFCS_Val_Time.xlsx"
    sheet_name = f"{user_name}_Time"

    # Crea el archivo si no existe
    if not os.path.exists(file_name):
        wb = Workbook()
        wb.save(file_name)

    # Carga el archivo existente
    wb = load_workbook(file_name)

    # Si la hoja ya existe, añade un sufijo incremental
    original_sheet_name = sheet_name
    counter = 1
    while sheet_name in wb.sheetnames:
        sheet_name = f"{original_sheet_name}_{counter}"
        counter += 1

    # Crea una nueva hoja
    ws = wb.create_sheet(title=sheet_name)

    # Añade encabezados
    ws.append(["Tooth", "Elapsed Time (seconds)", "Elapsed Time (minutes)"])

    # Escribe los tiempos en el Excel
    total_time = 0
    for tooth_label, elapsed_time in zip(color_labels, time_matrix):
        # Reemplazar valores `None` con 0
        if elapsed_time is None:
            elapsed_time = 0
        elapsed_time_minutes = elapsed_time / 60  # Convertir a minutos
        ws.append([tooth_label, elapsed_time, elapsed_time_minutes])
        total_time += elapsed_time

    # Añade una fila para el total
    total_time_minutes = total_time / 60  # Convertir el total a minutos
    ws.append(["Total", total_time, total_time_minutes])

    # Guarda el archivo
    wb.save(file_name)




############################################################ Main Windown ############################################################

root = tk.Tk()
# root.geometry("1300x800") 
root.attributes('-fullscreen', True)
root.bind('<Escape>', exit_fullscreen)
root.title("Color Selector")

# Excel with PyFCS data
file_path = os.path.join(os.getcwd(), "Datasets", "results_opt_1.xlsx") 
data = pd.read_excel(file_path)

columns_to_convert = ['top', 'middle', 'bottom']

# Convertir las cadenas a listas de tuplas para las columnas especificadas
for col in columns_to_convert:
    data[col] = data[col].apply(ast.literal_eval)

for idx, row in data.iterrows():
    top_values = row['top']    
    middle_values = row['middle']  
    bottom_values = row['bottom'] 

start_time = None
time_matrix = []


############################################################ INTERFACE ############################################################

# Create the main frame for the colors
frame = tk.Frame(root)
frame.pack(pady=10, padx=10)

# Global variable to store the user's name
user_name = ""
results_matrix = [] 
comments_matrix = []
original_position_left_image = (150, 200)  # left image original position
left_image_id = None  # ID left image
current_file_index = 0

# Ask for the user's ID at the start
ask_user_name()
start_time = time.time()

# Variable to store the selected option
image_source = tk.StringVar(value="tooth")  # By default, use 'Vita Tooth'

# Create the images and assign checkboxes
color_labels = ["A1", "A2", "A3", "A3_5", "A4", "B1", "B2", "B3", "B4", "C1", "C2", "C3", "C4", "D2", "D3", "D4"]
image_dir = os.path.join(os.getcwd(), "Datasets", "reference_colors")  # Initial image directory
vita_dir = os.path.join(os.getcwd(), "Datasets", "vita_tooth")  # Image directory for 'Image 2'
image_files = [f"{label}.png" for label in color_labels]

total_files = len([f for f in os.listdir(vita_dir) if os.path.isfile(os.path.join(vita_dir, f))])

# Create matrix to save results
initialize_results_matrix()
initialize_comments_matrix()
initialize_time_matrix()

# Load images
images = [tk.PhotoImage(file=os.path.join(image_dir, image)) for image in image_files]

# Shared variable for the checkboxes
selected_color = tk.StringVar(value=0)  

# Create containers for images and checkboxes
for idx, (color, img) in enumerate(zip(color_labels, images)):
    col_frame = tk.Frame(frame)  # Frame for each image and checkbox
    col_frame.grid(row=0, column=idx, padx=5, pady=5)

    # Image
    img_label = tk.Label(col_frame, image=img)
    img_label.pack()

    # Radiobutton under the image
    chk = tk.Radiobutton(
        col_frame, 
        text=color, 
        variable=selected_color, 
        value=color, 
        command=update_image_from_selection  
    )
    chk.pack()

# Create a main frame for organizing the center and right sections
main_center_frame = tk.Frame(root)
main_center_frame.pack(pady=20, padx=20)

# Create the area for central images
center_frame = tk.Frame(main_center_frame)
center_frame.grid(row=0, column=0, padx=10)

# Reduce top spacers to bring down the images
tk.Label(center_frame, height=0).grid(row=0, column=0, columnspan=2)  

# Create canvas for two images
shared_canvas = tk.Canvas(center_frame, width=440, height=400, bg="SystemButtonFace", highlightthickness=0)
shared_canvas.grid(row=1, column=0, padx=10, pady=1, columnspan=2)

# Coordenates of the two images 
coords_img1 = original_position_left_image
coords_img2 = (300, 200)  

# Buttons and checkboxes under the central images
buttons_frame = tk.Frame(center_frame)
buttons_frame.grid(row=3, column=0, columnspan=2, pady=2)

counter_label = tk.Label(buttons_frame, text="1/16", font=("Arial", 10))
counter_label.grid(row=0, column=0, columnspan=2, pady=5)

prev_button = tk.Button(buttons_frame, text="Previous", command=show_previous_image, state="disabled")
prev_button.grid(row=1, column=0, padx=10)

next_button = tk.Button(buttons_frame, text="Next", command=show_next_image)
next_button.grid(row=1, column=1, padx=10)

# "Reset all" button to restart the cycle
reset_button = tk.Button(buttons_frame, text="Reset all", command=reset_cycle, state="disabled")
reset_button.grid(row=3, column=0, columnspan=2, pady=5)

# Create the sliders with comboboxes to the right of the central images
sliders_frame = tk.Frame(main_center_frame)
sliders_frame.grid(row=0, column=1, padx=10, pady=1)

# Create global lists 
all_static_texts = []  # Referencias a textos estáticos
all_radiobuttons = []  # Referencias a radiobuttons
radiobutton_values = []  # Almacenará los valores seleccionados de los radiobuttons
image_frames = []  # Referencias a los widgets de imagen

# Nombres de filas
row_names = ["Upper Tooth", "Central Tooth", "Lower Tooth"]

for row_idx, row_name in enumerate(row_names):
    # Etiqueta para cada fila
    row_label = tk.Label(sliders_frame, text=row_name, font=("Arial", 10, "bold"))
    row_label.grid(row=row_idx, column=0, padx=10, pady=0)

    # Agregar texto estático, imágenes y radiobuttons
    for col_idx in range(3):  # Tres columnas por fila
        control_frame = tk.Frame(sliders_frame)
        control_frame.grid(row=row_idx, column=col_idx + 1, padx=10, pady=7)

        # Frame vacío para imagen (a la izquierda del texto estático)
        image_frame = tk.Frame(control_frame, width=20, height=20)
        image_frame.pack(padx=5)
        image_frame.pack_propagate(False)   # Evita que el frame cambie de tamaño
        image_frames.append(image_frame)

        # Texto estático
        static_text = tk.Label(control_frame, text="Text", font=("Arial", 10))
        static_text.pack() 
        all_static_texts.append(static_text)  # Guardar referencia

        # Radiobuttons
        radiobutton_frame = tk.Frame(control_frame)
        radiobutton_frame.pack(side="bottom", pady=5)

        rb_value = tk.IntVar(value=-1)  # Valor predeterminado de los radiobuttons
        radiobutton_values.append(rb_value)

        for rb_idx in range(1, 6):  # Crear 5 radiobuttons (valores 1-5)
            rb = tk.Radiobutton(
                radiobutton_frame, 
                text=str(rb_idx),      # El texto del radiobutton
                variable=rb_value, 
                value=rb_idx,
                indicatoron=False,     # Hace que el botón sea cuadrado con texto alineado
                width=2,                # Ajusta el ancho para mejorar la apariencia
                command=validate_visible
            )
            rb.pack(side=tk.LEFT)
            all_radiobuttons.append(rb)


# Create a new frame for the additional sliders to the right
additional_text_frame = tk.Frame(main_center_frame)
additional_text_frame.grid(row=0, column=2, padx=10, pady=1)

# Agregar un encabezado para la nueva columna
header_label = tk.Label(additional_text_frame, text="Comments", font=("Arial", 12, "bold"))
header_label.grid(row=0, column=0, padx=0, pady=0, columnspan=2)

# Crear una lista para almacenar las referencias de las casillas de texto
additional_text_entries = []

# Agregar casillas de texto para cada fila
for row_idx in range(len(row_names)):
    # Crear una casilla de texto
    text_entry = tk.Entry(additional_text_frame, width=25, font=("Arial", 10))
    text_entry.grid(row=row_idx + 1, column=0, padx=10, pady=20)  # Espaciado para cada fila

    # Guardar la referencia a la casilla de texto
    additional_text_entries.append(text_entry)

vita_images = []
current_index = -1


# Create Radiobuttons to select the reference type
reference_options_frame = tk.Frame(buttons_frame)
reference_options_frame.grid(row=2, column=0, columnspan=2, pady=10)

# When selected, image_source will be "tooth"
tk.Radiobutton(
    reference_options_frame,
    text="Reference Tooth",
    variable=image_source,
    value="tooth",  
    command=update_image_source  
).grid(row=0, column=0, padx=10)

# When selected, image_source will be "color"
tk.Radiobutton(
    reference_options_frame,
    text="Reference Color",
    variable=image_source,
    value="color",  
    command=update_image_source  
).grid(row=0, column=1, padx=10)

# Load the images at the start
load_vita_images()
update_image_from_selection()

# Show the first random image
show_next_image()

next_button.config(state="disabled")
prev_button.config(state="disabled")

# Run the interface
root.mainloop()
