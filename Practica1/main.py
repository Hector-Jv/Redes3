import tkinter as tk
from Tkinter import pantalla_inicio as home

# root
root = tk.Tk()

# Obtener el ancho y la altura de la pantalla
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
# Calcular la posición x e y de la ventana para que esté centrada
x = int((screen_width / 2) - (root.winfo_reqwidth() / 2) - 100)
y = int((screen_height / 2) - (root.winfo_reqheight() / 2) - 100)
# Establecer la posición de la ventana
root.geometry("+{}+{}".format(x, y))
home.pantalla_inicio(root)
root.mainloop()
