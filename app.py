import customtkinter as ctk
from tkinter import ttk
from PIL import Image, ImageTk
import matplotlib
from CRUD.ingrediente_crud import IngredienteCRUD
from CRUD.menu_crud import MenuCRUD
from CRUD.pedido_crud import PedidoCRUD
from CRUD.cliente_crud import ClienteCRUD

ctk.set_default_color_theme("green")

app = ctk.CTk()
app.geometry("900x900")


#---Diccionario Colores
colores = {
    "naranjo" : "#de8c3a",
    "morado" : "#d362f5",
    "rosado" : "#f562b5"
}

#---Variables Colores
rosado = colores["rosado"]
morado = colores["morado"]
naranjo = colores["naranjo"]

#---Pestañas
pestañas = ctk.CTkTabview(app, 10, 10)
pestañas.pack()
p_ingredientes = pestañas.add("Ingredientes")
p_menu = pestañas.add("Menú")
p_clientes = pestañas.add("Clientes")
p_paneldecompra = pestañas.add("Panel de compra")
p_pedidos = pestañas.add("Pedidos")
p_graficos = pestañas.add("Gráficos")

#---Frames
f_ingredientes = ctk.CTkFrame(p_ingredientes)
f_ingredientes.grid(row=0, column=0, padx=20, pady=20)

f_menu = ctk.CTkFrame(p_menu)
f_menu.grid(pady=10, padx=10)

f_clientes = ctk.CTkFrame(p_clientes)
f_clientes.grid(padx=10, pady=10)

f_paneldecompra = ctk.CTkScrollableFrame(p_paneldecompra, width=700, height=700)
f_paneldecompra.grid(row=0, column=0, padx=20, pady=20)

f_img = ctk.CTkFrame(f_paneldecompra)
f_img.grid(row=0, column=0, pady=10)

f_total = ctk.CTkFrame(f_paneldecompra)
f_total.grid(row=1, column=0, pady=10)

f_pedidos = ctk.CTkScrollableFrame(p_pedidos, width=700, height=700)
f_pedidos.grid(pady=20, padx=20)

#---Elementos Frame Panel Ingredientes
  
ingrediente = IngredienteCRUD() 
  
def actualizar_lista():
    registros = t_ingredientes.get_children()
    for registro in registros:
        t_ingredientes.delete(registro) 
    productos = ingrediente.obtener_ingredientes()
    for ref, producto in enumerate(productos):
        t_ingredientes.insert("", "end", values=(producto.nombre, producto.tipo, producto.unidad, producto.cantidad))
  
def registrar_ingrediente():
    actualizar_lista()
    pass

def eliminar_ingrediente():
    actualizar_lista()
    pass

def modificar_ingrediente():
    actualizar_lista() 
    pass

def seleccionar_fila():
    pass

#---Ventana Ingreso Ingredientes
def IngresoIngredientes():
    v_ingredientes = ctk.CTkToplevel(app)
    v_ingredientes.geometry("400x400")
    v_ingredientes.title("Modificar datos") 
    v_ingredientes.lift()  
    v_ingredientes.focus_force() 
    v_ingredientes.grab_set()

    l_nombre = ctk.CTkLabel(v_ingredientes, text="Nombre:")
    l_nombre.pack(padx=2, pady=2)
    e_nombre = ctk.CTkEntry(v_ingredientes)
    e_nombre.pack(padx=2, pady=2)

    l_tipo = ctk.CTkLabel(v_ingredientes, text="Tipo:")
    l_tipo.pack(padx=2, pady=2)
    e_tipo = ctk.CTkEntry(v_ingredientes)
    e_tipo.pack(padx=2, pady=2)
    
    l_unidad = ctk.CTkLabel(v_ingredientes, text="Unidad:")
    l_unidad.pack(padx=2, pady=2)
    e_unidad = ctk.CTkEntry(v_ingredientes)
    e_unidad.pack(padx=2, pady=2)

    l_cantidad = ctk.CTkLabel(v_ingredientes, text="Cantidad:")
    l_cantidad.pack(padx=2, pady=2)
    e_cantidad = ctk.CTkEntry(v_ingredientes)
    e_cantidad.pack(padx=2, pady=2)

    b_guardar = ctk.CTkButton(v_ingredientes, text="Guardar", command=registrar_ingrediente, fg_color=rosado, hover_color="purple")
    b_guardar.pack(padx=10,pady=30)

def ModificarIngredientes():
    v_ingredientes = ctk.CTkToplevel(app)
    v_ingredientes.geometry("400x400")
    v_ingredientes.title("Modificar datos") 
    v_ingredientes.lift()  
    v_ingredientes.focus_force() 
    v_ingredientes.grab_set()

    l_nombre = ctk.CTkLabel(v_ingredientes, text="Nombre:")
    l_nombre.pack(padx=2, pady=2)
    e_nombre = ctk.CTkEntry(v_ingredientes)
    e_nombre.pack(padx=2, pady=2)

    l_tipo = ctk.CTkLabel(v_ingredientes, text="Tipo:")
    l_tipo.pack(padx=2, pady=2)
    e_tipo = ctk.CTkEntry(v_ingredientes)
    e_tipo.pack(padx=2, pady=2)
    
    l_unidad = ctk.CTkLabel(v_ingredientes, text="Unidad:")
    l_unidad.pack(padx=2, pady=2)
    e_unidad = ctk.CTkEntry(v_ingredientes)
    e_unidad.pack(padx=2, pady=2)

    l_cantidad = ctk.CTkLabel(v_ingredientes, text="Cantidad:")
    l_cantidad.pack(padx=2, pady=2)
    e_cantidad = ctk.CTkEntry(v_ingredientes)
    e_cantidad.pack(padx=2, pady=2)

    b_guardar = ctk.CTkButton(v_ingredientes, text="Guardar", command=modificar_ingrediente, fg_color=rosado, hover_color="purple")
    b_guardar.pack(padx=10,pady=30)



#---Botones Frame Ingredientes
b_ingresar_i = ctk.CTkButton(f_ingredientes, text="Ingresar Ingrediente", fg_color=rosado, hover_color="purple", command=IngresoIngredientes)
b_ingresar_i.grid(row=0, column=0, padx=10, pady=10, sticky="w")

b_modificar_i = ctk.CTkButton(f_ingredientes, text="Modificar Ingrediente", fg_color=rosado, hover_color="purple", command=ModificarIngredientes)
b_modificar_i.grid(row=0, column=0, padx=10, pady=10)

b_eliminar_i = ctk.CTkButton(f_ingredientes, text="Eliminar Ingrediente.", fg_color=naranjo, hover_color="red", command=eliminar_ingrediente)
b_eliminar_i.grid(row=0, column=0, padx=10, pady=10, sticky="e")

#---Tabla Ingredientes
t_ingredientes = ttk.Treeview(f_ingredientes, columns=("Nombre", "Tipo", "Unidad", "Cantidad"), show="headings")
t_ingredientes.grid(row=1, column=0, pady=10)  # Ocupa las dos columnas
t_ingredientes.heading("Nombre", text="Nombre")
t_ingredientes.heading("Tipo", text="Tipo")
t_ingredientes.heading("Unidad", text="Unidad")
t_ingredientes.heading("Cantidad", text="Cantidad")
t_ingredientes.column("Nombre")
t_ingredientes.column("Tipo")
t_ingredientes.column("Unidad")
t_ingredientes.column("Cantidad")

#---Elementos Frame Panel Menú

global v_menu

def AgregarMenu():
    global v_menu, f_crear_menu 
    v_menu = ctk.CTkToplevel(app)
    v_menu.geometry("600x600")
    v_menu.title("Modificar datos")
    v_menu.lift()
    v_menu.focus_force()
    v_menu.grab_set()


    f_crear_menu = ctk.CTkScrollableFrame(v_menu, width=450, height=300, orientation="horizontal")
    f_crear_menu.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")


    l_nombre = ctk.CTkLabel(f_crear_menu, text="Nombre:")
    l_nombre.grid(row=1, column=0, padx=10, pady=10)
    e_nombre = ctk.CTkEntry(f_crear_menu)
    e_nombre.grid(row=2, column=0, padx=10, pady=10)

    l_descripcion = ctk.CTkLabel(f_crear_menu, text="Descripción:")
    l_descripcion.grid(row=1, column=1, padx=10, pady=10)
    e_descripcion = ctk.CTkEntry(f_crear_menu)
    e_descripcion.grid(row=2, column=1, padx=10, pady=10)

    b_agregar_i = ctk.CTkButton(f_crear_menu, fg_color=rosado, text="Agregar ingrediente", hover_color="purple", command=agregar_combobox)
    b_agregar_i.grid(row=0, column=1, padx=10, pady=10)

def agregar_combobox():
    global f_crear_menu  # Usar el scrollable frame como contenedor
    opciones = ["Opción 1", "Opción 2", "Opción 3"]

    # Crear un nuevo combobox dentro del scrollable frame
    nuevo_combobox = ctk.CTkComboBox(f_crear_menu, values=opciones, border_color=rosado, dropdown_fg_color=rosado, button_color=rosado, button_hover_color="purple", dropdown_hover_color="purple")
    nuevo_combobox.grid(row=4, column=len(combobox_list), padx=10, pady=10)  # Colocar en la siguiente posición disponible

    # Agregar a la lista
    combobox_list.append(nuevo_combobox)

combobox_list = []

b_menu = ctk.CTkButton(f_menu, fg_color=rosado, text="Crear Menú", hover_color="purple", command=AgregarMenu)
b_menu.grid(row=2, column=0, pady=20)


#---Tabla Ingredientes
t_ingredientes = ttk.Treeview(f_menu, columns=("Nombre", "Descripcion"), show="headings")
t_ingredientes.grid(row=3, column=0, pady=10)  # Ocupa las dos columnas
t_ingredientes.heading("Nombre", text="Nombre")
t_ingredientes.heading("Descripcion", text="Descripcion")
t_ingredientes.column("Nombre")
t_ingredientes.column("Descripcion")

#---Elementos Frame Panel Clientes
l_nombre_c = ctk.CTkLabel(f_clientes, text="Ingrese el nombre del cliente")
l_nombre_c.grid(padx=30)
e_nombre_c = ctk.CTkEntry(f_clientes)
e_nombre_c.grid(row=1, padx=30)

l_correo = ctk.CTkLabel(f_clientes, text="Ingrese el correo eléctronico del cliente")
l_correo.grid(row=0, column=2, padx=30)
e_correo = ctk.CTkEntry(f_clientes)
e_correo.grid(row=1, column=2, padx=30)

b_crear_cliente = ctk.CTkButton(f_clientes, text="Crear Cliente", fg_color=rosado, hover_color="purple")
b_crear_cliente.grid(row=2, column=1, pady=10)

b_eliminar_cliente = ctk.CTkButton(f_clientes, text="Eliminar Cliente", fg_color=naranjo, hover_color="red")
b_eliminar_cliente.grid(row=3, column=0)

b_actualizar_cliente = ctk.CTkButton(f_clientes, text="Actualizar Cliente", fg_color=morado, hover_color="green")
b_actualizar_cliente.grid(row=3, column=2)

#---Tabla Clientes
t_clientes = ttk.Treeview(f_clientes, columns=("Correo", "Nombre"), show="headings")
t_clientes.heading("Correo", text="Correo")
t_clientes.heading("Nombre", text="Nombre")
t_clientes.grid(row=3,column=1, pady=30)

#---Elementos Frame Panel Compra
l_total = ctk.CTkLabel(f_total, text=f"El total del pedido es: $0")
l_total.grid(row=1, column=0, pady=10, padx=10)

#---Botón Generar Boleta
b_pdf = ctk.CTkButton(f_paneldecompra, text="Generar boleta.", command=lambda: generarboleta, hover_color="purple", fg_color=rosado)
b_pdf.grid(row=3, pady=30, sticky="e")

cb_menus = ctk.CTkComboBox(f_paneldecompra, border_color=rosado, dropdown_fg_color=rosado, button_color=rosado, button_hover_color="purple", dropdown_hover_color="purple", width=160)
cb_menus.grid(row=0)
cb_menus.set("Seleccione el menú")

#---Tabla Panel Compra
t_paneldecompra = ttk.Treeview(f_paneldecompra, columns=("Nombre", "Cantidad", "Total"), show="headings")
t_paneldecompra.heading("Nombre", text="Nombre")
t_paneldecompra.heading("Cantidad", text="Cantidad")
t_paneldecompra.heading("Total", text="Precio Total")
t_paneldecompra.grid(row=2, column=0, pady=20)

b_eliminar_pedido = ctk.CTkButton(f_paneldecompra, text="Eliminar Pedido.", command=lambda: eliminarpedido, hover_color="red", fg_color=naranjo)
b_eliminar_pedido.grid(row=3, column=0, pady=0, padx=10, sticky="w")

#---Elementos Frame Panel Pedidos
t_pedidos = ttk.Treeview(f_pedidos, columns=("Pedido", "Fecha", "Total"), show="headings")
t_pedidos.heading("Pedido", text="Pedido")
t_pedidos.heading("Fecha", text="Fecha")
t_pedidos.heading("Total", text="Total")
t_pedidos.grid(pady=20)

app.mainloop()

