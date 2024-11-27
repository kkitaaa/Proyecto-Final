import sqlalchemy as db
from sqlalchemy.orm import Session
from models import Menu, Ingrediente
# para verificar tipos de dato de lista
from typing import List 
# para manejar excepciones
from sqlalchemy.exc import IntegrityError 
from sqlalchemy.orm.exc import NoResultFound

 
# esta clase se conecta a la base de datos cada vez que se instacia un objeto
class MenuCRUD():
    def __init__(self):
        self.engine = db.create_engine("sqlite:///bd/inventario.db", echo=True, future=True)
        
    # ahora vamos a crear el metodo para ingresar un nuevo ingrediente
    def ingresar_menu(self, nombre, descripcion, ingredientes, precio):
        try:
            # Abrir sesión
            with Session(self.engine) as session:
                # Buscar ingredientes en la base de datos por sus IDs
                ingredientes = session.query(Ingrediente).filter(Ingrediente.id.in_(id)).all()
                if len(ingredientes) != len(id):
                    raise ValueError("Algunos ingredientes no existen en la base de datos.")

                # Crear el objeto Menu
                nuevo_menu = Menu(nombre=nombre, descripcion=descripcion, ingredientes=ingredientes, precio = precio)
                session.add(nuevo_menu)
                session.commit()
                print(f"Menú '{nombre}' agregado correctamente.")
        except Exception as e:
            print(f"Error al ingresar el menú: {e}")
    
    # ahora vamos a crear el metodo para modificar un menu existente dentro de la base de datos
    # vamos a usar el id como identificador unico para seleccionar un registro especifico de la base de datos            
    def modificar_menu(self, nombre, descripcion, ingredientes, precio, id):
        try:
            # aqui vamos a buscar el registro correspondiente al id ingresado
            # abrimos una sesion y filtramos los resultados por el id (que siempre dara un solo resultado)
            with Session(self.engine) as session:
                menu = session.query(Menu).filter_by(id=id).one()
                
                # actualizamos el registro
                menu.nombre = nombre
                menu.descripcion = descripcion
                menu.ingredientes = ingredientes
                menu.precio = precio
                session.commit()
                print(f"Menu con ID {id} actualizado correctamente.")
            
        # usaremos manejo de errores para controlar el flujo del programa en caso de que algo salga mal
        except NoResultFound:       
            print(f"No se encontro ningun Menu con el ID {id}, Operacion fallida.")
            return False
        except Exception as e:
            print(f"Error al actualizar el Menu: {e}")
            return False
        
    # ahora vamos a crear un metodo para obtener una lista con los registros de la base de datos
    def obtener_menus(self) -> List[Menu]:
        productos: Menu = None
        # abrimos una sesion y hacemos una consulta que obtiene todos los registros de la tabla
        with Session (self.engine) as session:
            productos = session.query(Menu).all()
        return productos
    
    # ahora vamos a crear un metodo para eliminar un registro de la tabla
    def eliminar_ingrediente(self, id):
        with Session(self.engine) as session:
            # verificamos si existe el registro correspondiente al id ingresado
            menu = session.query(Menu).filter_by(id=id).first()       
            if menu:
                try:
                    # en caso de que todo salga bien eliminamos el registro seleccionado
                    session.delete(menu)
                    session.commit()
                    print(f"Menu con el ID {id} eliminado correctamente.")
                except IntegrityError as e:
                    # en caso de que falle la operacion, revertimos cualquier cambio realizado con rollback()
                    session.rollback()
                    print(f"No se pudo eliminar el Menu con ID {id}. Error: {e}")
            else:
                print(f"No se encontro ningun Menu con el ID {id}.")