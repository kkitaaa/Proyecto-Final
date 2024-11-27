import sqlalchemy as db
from sqlalchemy.orm import Session
from models import Ingrediente
# para verificar tipos de dato de lista
from typing import List 
# para manejar excepciones
from sqlalchemy.exc import IntegrityError 
from sqlalchemy.orm.exc import NoResultFound

 
# esta clase se conecta a la base de datos cada vez que se instacia un objeto
class IngredienteCRUD():
    def __init__(self):
        self.engine = db.create_engine("sqlite:///bd/inventario.db", echo=True, future=True)
        
    # ahora vamos a crear el metodo para ingresar un nuevo ingrediente
    def ingresar_ingrediente(self, nombre, tipo, unidad, cantidad):
        # llamamos al modelo ORM en esta variable
        producto = Ingrediente()
        # Asignamos los valores
        producto.nombre = nombre
        producto.tipo = tipo
        producto.unidad = unidad
        producto.cantidad = cantidad
        # abrimos una sesion al motor y agregamos el modelo como un registro dentro de la tabla Ingrediente
        with Session(self.engine) as session:
            session.add(producto)
            session.commit()
    
    # ahora vamos a crear el metodo para modificar un ingrdiente existente dentro de la base de datos
    # vamos a usar el id como identificador unico para seleccionar un registro especifico de la base de datos            
    def modificar_ingrediente(self, nombre, tipo, unidad, cantidad, id):
        try:
            # aqui vamos a buscar el registro correspondiente al id ingresado
            # abrimos una sesion y filtramos los resultados por el id (que siempre dara un solo resultado)
            with Session(self.engine) as session:
                producto = session.query(Ingrediente).filter_by(id=id).one()
                
                # actualizamos el registro
                producto.nombre = nombre
                producto.tipo = tipo
                producto.unidad = unidad
                producto.cantidad = cantidad
                session.commit()
                print(f"Producto con ID {id} actualizado correctamente.")
            
        # usaremos manejo de errores para controlar el flujo del programa en caso de que algo salga mal
        except NoResultFound:       
            print(f"No se encontro ningun ingrediente con el ID {id}, Operacion fallida.")
            return False
        except Exception as e:
            print(f"Error al actualizar el prodicto: {e}")
            return False
        
    # ahora vamos a crear un metodo para obtener una lista con los registros de la base de datos
    def obtener_ingredientes(self) -> List[Ingrediente]:
        productos: Ingrediente = None
        # abrimos una sesion y hacemos una consulta que obtiene todos los registros de la tabla
        with Session (self.engine) as session:
            productos = session.query(Ingrediente).all()
        return productos
    
    # ahora vamos a crear un metodo para eliminar un registro de la tabla
    def eliminar_ingrediente(self, id):
        with Session(self.engine) as session:
            # verificamos si existe el registro correspondiente al id ingresado
            producto = session.query(Ingrediente).filter_by(id=id).first()       
            if producto:
                try:
                    # en caso de que todo salga bien eliminamos el registro seleccionado
                    session.delete(producto)
                    session.commit()
                    print(f"Producto con el ID {id} eliminado correctamente.")
                except IntegrityError as e:
                    # en caso de que falle la operacion, revertimos cualquier cambio realizado con rollback()
                    session.rollback()
                    print(f"No se pudo eliminar el producto con ID {id}. Error: {e}")
            else:
                print(f"No se encontro ningun ingrediente con el ID {id}.")