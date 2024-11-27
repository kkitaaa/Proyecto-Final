import re
import inspect
import tkinter.messagebox
import customtkinter as ctk
import tkinter 
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
from fpdf import FPDF
from PIL import Image


class Ingrediente:
    def __init__(self, nombre, cantidad):
        self.nombre = nombre
        self.cantidad = cantidad    


class Inventario:
    def __init__(self):
        self.ingredientes = []
    
    def agregar_ingrediente(self, ingrediente):
        
        actualizado = False
        
        for i in self.ingredientes:
            if i.nombre == ingrediente.nombre:
                i.cantidad += ingrediente.cantidad
                actualizado = True
                CTkMessagebox(title="Exito", message="Cantidad de ingrediente actualizado.", icon="check")
                break
        if not actualizado:
            self.ingredientes.append(ingrediente)
     
    def quitar_ingrediente(self, index):
        if 0 <= index < len(self.ingredientes):
            del self.ingredientes[index]
            
    def obtener_inventario(self):
        # Devolver una lista de tuplas
        return [(ingrediente.nombre, ingrediente.cantidad) for ingrediente in self.ingredientes]    


inventario = Inventario()

def ingresar_ingrediente(nombre, cantidad):
    if nombre and cantidad:
        try:
            cantidad = int(cantidad) # convierte el campo
            ingrediente = Ingrediente(nombre, cantidad)
            # instanciamos la clase con los valores de la funcion
            inventario.agregar_ingrediente(ingrediente) # agregamos al inventario
            actualizar_inventario() # actualizamos el inventario
            actualizar_stock_ing()
            entry_ingrediente.delete(0, 'end')
            entry_cantidad.delete(0, 'end')
            inven = inventario.obtener_inventario()
            print(inven)
        except:
            CTkMessagebox(title="Error", message="El dato ingresado no es un numero, por favor intentelo de nuevo.", icon="warning")
            entry_cantidad.delete(0, 'end')
    else:
        CTkMessagebox(title="Error", message="Los campos estan vacios, por favor intentelo de nuevo.", icon="warning")         


def eliminar_ingrediente():
    seleccion = tree.selection()
    if not seleccion:
        CTkMessagebox(title="Error", message="No se ha seleccionado ninguna fila.", icon="warning")
        return
    index = tree.index(seleccion[0])
    inventario.quitar_ingrediente(index)
    actualizar_inventario()


def actualizar_inventario():
    tree.delete(*tree.get_children())
    for ingrediente in inventario.obtener_inventario():
        tree.insert("", "end", values=ingrediente)    


def verificar_existencia(treeview, valor):
    for item_id in treeview.children():
        valores = treeview.item(item_id, 'values')
        if valor in valores:
            print("existe")
    




class Menus:
    def __init__(self, nombre, precio, ingredientesnecesarios, rutaicon):
        self.nombre = nombre
        self.precio = precio
        self.ingredientesnecesarios = ingredientesnecesarios
        self.cantidaddis = 0
        self.iconomenu = ctk.CTkImage(Image.open(rutaicon))
    
    def verificardisp(self, stockdisp):
        """
        Verifica cuántos menús se pueden preparar con los ingredientes disponibles.
        stock_ingredientes es un diccionario con {nombre_ingrediente: cantidad_disponible}.
        """
        cantidades_posibles = []
        
        for ingrediente, ingnecesarios in self.ingredientesnecesarios.items():
            if ingrediente in stockdisp:
                cantidad_disponible = stockdisp[ingrediente]
                max_por_ingrediente = cantidad_disponible // ingnecesarios
                cantidades_posibles.append(max_por_ingrediente)
            else:
                return 0  # Si falta un ingrediente, no se puede preparar ningún menú
        
        self.cantidaddis = min(cantidades_posibles)
        return self.cantidaddis  


class Pedidos:
    def __init__(self):
        self.listamenus = []
        self.total = 0.0

    def agregarmenu(self, menu):
        self.listamenus.append(menu)
        self.total += menu.precio

    def eliminarmenu(self, menu):
        if menu in self.listamenus:
            self.listamenus.remove(menu)
            self.total -= menu.precio

    def vaciarpedido(self):
        self.listamenus.clear()
        self.total = 0.0

    def calctotal(self):
        return self.total  


listamenus = []


listatarjetas = []
stock_ing = []
pedido = Pedidos()


def actualizar_stock_ing():
    global stock_ing
    stock_ing = [Ingrediente(nombre, cantidad) for nombre, cantidad in inventario.obtener_inventario()]
    


def crearmenus():
    ing_papas = {"Papas":5}
    ing_pepsi = {"Bebida":1}
    ing_completo = {"Vienesa":1, "Pan de completo":1, "Tomate":1, "Palta":1}
    ing_hamburguesa = {"Pan de hamburguesa":1, "Lamina de queso":1, "Churrasco de carne":1}        

    papas = Menus("Papas Fritas", 500, ing_papas, "icono_papas_fritas_64x64.png")
    pepsi = Menus("Pepsi", 1100, ing_pepsi, "icono_cola_64x64.png")
    completo = Menus("Completos", 1800, ing_completo, "icono_hotdog_sin_texto_64x64.png")
    hamburguesa = Menus("Hamburguesa", 3500, ing_hamburguesa, "icono_hamburguesa_negra_64x64.png")

    listamenus.append(papas)
    listamenus.append(pepsi)
    listamenus.append(completo)
    listamenus.append(hamburguesa)

crearmenus()




# FUNCIONES DE ACTUALIZACION DE LA INTERFAZ SECCION PEDIDOS

def actutablamenus():
    # Crear un diccionario para contar las cantidades de cada menú
    menuses = {}
        
    for menu in  pedido.listamenus:
        if menu.nombre in menuses:
            menuses[menu.nombre]['cantidad'] += 1
            menuses[menu.nombre]['precio_total'] += menu.precio
        else:
            menuses[menu.nombre] = {'cantidad': 1, 'precio_total': menu.precio}

    # Limpiar el Treeview antes de actualizarlo
    for item in tablamenus.get_children():
        tablamenus.delete(item)

    # Insertar los menús en el Treeview
    for nombre, datos in menuses.items():
        tablamenus.insert("", "end", values=(nombre, datos['cantidad'], f"${datos['precio_total']:.2f}"))



def eliminarmenu():
    menu = tablamenus.focus()
    if not menu:
        CTkMessagebox(title="Error", message="Seleccione un Menu a eliminar.", icon="warning")
        return
    confirmacion = tkinter.messagebox.askyesno(title="Confirmacion", message="¿Esta seguro de eliminar la existencia de este Menu?")
    if confirmacion:
        Nombre = tablamenus.item(menu, "values")[0]      
        for menu in pedido.listamenus:
            if menu.nombre == Nombre:
                for ingnombre, ingcantidad in menu.ingredientesnecesarios.items():
                    ingstock = next((ing for ing in stock_ing if ing.nombre == ingnombre), None)
                    if ingstock:
                        ingstock.cantidad += ingcantidad
                        pedido.eliminarmenu(menu)
                            
                    else:
                        ing = Ingrediente(Nombre, 0) #medio arreglado       se instancian cada uno, se tienen que actualizar
                        ing.cantidad += ingcantidad
                        stock_ing.append(ing)

        actutablaing()
        actutablamenus()
        CTkMessagebox(title="Exito", message="Menu eliminado.", icon="warning")        
        return True 


def generarmenus():

        for tarjetas in listatarjetas:
            tarjetas.destroy()   
            
        for menu in listamenus:
            mcantidad = menu.verificardisp({ing.nombre: ing.cantidad for ing in stock_ing})
            if mcantidad > 0:
                crear_tarjeta(menu)
            else:
                CTkMessagebox(title="Ingredientes Insuficientes", message=f"No hay suficientes ingredientes para crear el menú '{menu.nombre}'.", icon="warning")


def crear_tarjeta(menu):
    # Obtener el número de columnas y filas actuales
    num_tarjetas = len(listatarjetas) ############### Menus creados     Lista de menus #########
    fila = num_tarjetas // 2
    columna = num_tarjetas % 2

    # Crear la tarjeta con un tamaño fijo
    tarjeta = ctk.CTkFrame(img_frame, corner_radius=10, border_width=1, border_color="#4CAF50", width=64, height=140, fg_color="transparent")
    tarjeta.grid(row=fila, column=columna, padx=15, pady=15, )

    # Hacer que la tarjeta sea completamente clickeable 
    tarjeta.bind("<Button-1>", lambda event: tarjeta_click(event, menu))

    # Cambiar el color del borde cuando el mouse pasa sobre la tarjeta
    tarjeta.bind("<Enter>", lambda event: tarjeta.configure(border_color="#FF0000"))  # Cambia a rojo al pasar el mouse
    tarjeta.bind("<Leave>", lambda event: tarjeta.configure(border_color="#4CAF50"))  # Vuelve al verde al salir

    # Verifica si hay una imagen asociada con el menú
    if menu.iconomenu:
        # Crear y empaquetar el CTkLabel con la imagen, sin texto y con fondo transparente
        imagen_label = ctk.CTkLabel(tarjeta, image=menu.iconomenu, width=64, height=64, text="", bg_color="transparent")
        imagen_label.pack(anchor="center", pady=5, padx=10)
        imagen_label.bind("<Button-1>", lambda event: tarjeta_click(event, menu))  # Asegura que el clic en la imagen funcione

        # Agregar un Label debajo de la imagen para mostrar el nombre del menú
        texto_label = ctk.CTkLabel(tarjeta, text=f"{menu.nombre}", text_color="black", font=("Helvetica", 12, "bold"), bg_color="transparent")
        texto_label.pack(anchor="center", pady=1)
        texto_label.bind("<Button-1>", lambda event: tarjeta_click(event, menu))  # Asegura que el clic en el texto funcione

    else:
        print(f"No se pudo cargar la imagen para el menú '{menu.nombre}'")   

    listatarjetas.append(tarjeta)



def tarjeta_click(event, menu):
    # Verificar si hay suficientes ingredientes en el stock para preparar el menú
    suficiente_stock = True
    if stock_ing==[]:
        suficiente_stock=False
    for ingnecesario, ingcantidad in menu.ingredientesnecesarios.items():
        for ingrediente_stock in stock_ing:
            if ingnecesario == ingrediente_stock.nombre:
                if int(ingrediente_stock.cantidad) < int(ingcantidad):
                    suficiente_stock = False
                    break
        if not suficiente_stock:
            break

    if suficiente_stock:
        # Descontar los ingredientes del stock
        for ingnecesario, ingcantidad in menu.ingredientesnecesarios.items():
            for ingrediente_stock in stock_ing:
                if ingnecesario == ingrediente_stock.nombre:
                    ingrediente_stock.cantidad = int(ingrediente_stock.cantidad) - int(ingcantidad)

        # Agregar el menú al pedido
            pedido.agregarmenu(menu)
            actutablaing()
            # Actualizar el Treeview
            actutablamenus()
            lbl_total.configure(text=f"El Total del pedido es: ${pedido.total:.2f}")
    else:
        CTkMessagebox(title="Stock Insuficiente", message=f"No hay suficientes ingredientes para preparar el menú '{menu.nombre}'.", icon="warning")        


def actutablaing():
    for child in tree.get_children():
        tree.delete(child)

    for ing in stock_ing:
        tree.insert("", "end", values=(ing.nombre, ing.cantidad))


# SUPER FUNCION DE GENERAR PDF

def generarboleta():
        if not pedido.listamenus:
            CTkMessagebox(title="Pedido Vacío", message="No hay menús en el pedido para generar la boleta.", icon="warning")
            return

        # Crear una instancia de FPDF
        pdf = FPDF()
        pdf.add_page()

        # Encabezado de la boleta
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "Boleta Restaurante", ln=True, align="C")
        pdf.ln(10)
        
        # Detalles del restaurante (se pueden personalizar)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, "Razón Social del Negocio", ln=True)
        pdf.cell(0, 10, "RUT: 12345678-9", ln=True)
        pdf.cell(0, 10, "Dirección: Calle Falsa 123", ln=True)
        pdf.cell(0, 10, "Teléfono: +56 9 1234 5678", ln=True)
        pdf.ln(10)
        
        # Detalles del pedido
        pdf.set_font("Arial", "B", 12)
        pdf.cell(50, 10, "Nombre", 1)
        pdf.cell(30, 10, "Cantidad", 1)
        pdf.cell(50, 10, "Precio Unitario", 1)
        pdf.cell(50, 10, "Subtotal", 1)
        pdf.ln()
        
        pdf.set_font("Arial", size=12)

        menuses = {}
        
        for menu in pedido.listamenus:
            if menu.nombre in menuses:
                menuses[menu.nombre]['cantidad'] += 1
                menuses[menu.nombre]['precio_total'] += menu.precio
            else:
                menuses[menu.nombre] = {'cantidad': 1, 'precio_total': menu.precio}        

        for menu, datos in menuses.items():
            pdf.cell(50, 10, menu, 1)
            pdf.cell(30, 10, str(datos['cantidad']), 1)
            pdf.cell(50, 10, f"${datos['precio_total'] / datos['cantidad']:.2f}", 1)  # Precio unitario
            pdf.cell(50, 10, f"${datos['precio_total']:.2f}", 1)
            pdf.ln()

        # Calcular totales
        total = pedido.calctotal()
        iva = total * 0.19
        total_con_iva = total + iva
        
        # Mostrar subtotales y totales
        pdf.ln(10)
        pdf.cell(0, 10, f"Subtotal: ${total:.2f}", 0, 1, "R")
        pdf.cell(0, 10, f"IVA (19%): ${iva:.2f}", 0, 1, "R")
        pdf.cell(0, 10, f"Total: ${total_con_iva:.2f}", 0, 1, "R")
        
        # Guardar el archivo PDF
        pdf_output = "C:/Users/chaco/Desktop/Carrrera/Progra II/Entregas/codigos/Proyecto 1-20240909T132227Z-001/Proyecto 1/boleta.pdf" 
        pdf.output(pdf_output)

        CTkMessagebox(title="Boleta Generada", message=f"Boleta generada con éxito como '{pdf_output}'.", icon="info") 



# aqui creo la ventana de customtkinter    
app = ctk.CTk()

# aqui genero las ventanas (de ingredientes y pedidos)
tabview = ctk.CTkTabview(app, 10,10)
tabview.pack()  

# asigno nombres a las ventanas   
tab_ingredientes = tabview.add("Ingreso de Ingredientes")
tab_pedidos = tabview.add("Pedido")


# ************ SECCION FRAME 1 ************ 
# en esta parte configuro y creo el frame y los botones de la seccion de ingredientes

ing_frame = ctk.CTkFrame(tab_ingredientes)
ing_frame.grid(row=0, column=0)

lbl_nombre = ctk.CTkLabel(ing_frame, text= "Ingrese el nombre del ingrediente.")
lbl_nombre.pack(pady=10)
entry_ingrediente = ctk.CTkEntry(ing_frame)
entry_ingrediente.pack(pady=10)

lbl_cantidad = ctk.CTkLabel(ing_frame, text= "Ingrese la cantidad.")
lbl_cantidad.pack(pady=10)
entry_cantidad = ctk.CTkEntry(ing_frame)
entry_cantidad.pack(pady=10)

bttn_ingresar = ctk.CTkButton(ing_frame, text="Ingresar Ingrediente", command=lambda:ingresar_ingrediente(entry_ingrediente.get(),entry_cantidad.get()), hover_color="purple")
bttn_ingresar.pack(pady=10)

tabla_frame = ctk.CTkFrame(tab_ingredientes)
tabla_frame.grid(row=0, column=1, padx=20)

bttn_eliminar = ctk.CTkButton(tabla_frame, text="Eliminar Ingrediente.", command=eliminar_ingrediente, hover_color="red")
bttn_eliminar.grid(row=0, column=1, pady=10)

bttn_menu = ctk.CTkButton(tabla_frame, text="Generar Menú", command=generarmenus, hover_color="green")
bttn_menu.grid(row=2, column=1, pady=10)

# aqui creo y configuro la tabla treeview

tree = ttk.Treeview(tabla_frame, columns=("Nombre", "Cantidad"), show="headings")
tree.heading("Nombre", text="Nombre")
tree.heading("Cantidad", text="Cantidad")
tree.grid(column=1, row=1, padx=40, pady=40)
tree.column("Nombre", width=250)
tree.column("Cantidad", width=250)


# ************ SECCION FRAME 2 ************ 





img_frame = ctk.CTkFrame(tab_pedidos)
img_frame.grid(row=0, column=0)

total_frame = ctk.CTkFrame(tab_pedidos)
total_frame.grid(row=1, column=0)

lbl_total = ctk.CTkLabel(total_frame, text=f"El Total del pedido es: $0")
lbl_total.grid(row=0, column=0)

bttn_delete = ctk.CTkButton(total_frame, text="Eliminar Menu.", command=lambda:eliminarmenu)
bttn_delete.grid(row=0, column=1, padx=100)

menus_frame = ctk.CTkFrame(tab_pedidos)
menus_frame.grid(row=2, column=0) 

tablamenus = ttk.Treeview(menus_frame, columns=("nombre", "cantidad", "total"), show="headings")
tablamenus.heading("nombre", text="Nombre del Menu")
tablamenus.heading("cantidad", text="Cantidad")
tablamenus.heading("total", text="Precio Total")

tablamenus.grid(row=0, column=0) 

bttn_pdf = ctk.CTkButton(menus_frame, text="Generar boleta.", command=generarboleta)
bttn_pdf.grid(row=1)


app.mainloop()