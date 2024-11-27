import sqlalchemy as db
from sqlalchemy.orm import Session
from models import Cliente
from typing import List
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound


class ClienteCRUD:
    def __init__(self):
        # Configuración de la conexión a la base de datos
        self.engine = db.create_engine("sqlite:///bd/inventario.db", echo=True, future=True)
    
    def ingresar_cliente(self, nombre: str, email: str):
        """
        Inserta un nuevo cliente en la base de datos.
        """
        try:
            # Crear un objeto cliente
            nuevo_cliente = Cliente(nombre=nombre, email=email)
            
            # Abrir una sesión y agregar el cliente
            with Session(self.engine) as session:
                session.add(nuevo_cliente)
                session.commit()
                print(f"Cliente '{nombre}' agregado correctamente.")
        except IntegrityError:
            print(f"Error: Ya existe un cliente con el correo '{email}'.")
        except Exception as e:
            print(f"Error al agregar el cliente: {e}")

    def modificar_cliente(self, id: int, nombre: str, email: str):
        """
        Modifica un cliente existente en la base de datos.
        """
        try:
            # Buscar cliente por ID
            with Session(self.engine) as session:
                cliente = session.query(Cliente).filter_by(id=id).one()
                
                # Actualizar los datos del cliente
                cliente.nombre = nombre
                cliente.email = email
                session.commit()
                print(f"Cliente con ID {id} actualizado correctamente.")
        except NoResultFound:
            print(f"No se encontró ningún cliente con el ID {id}.")
        except IntegrityError:
            print(f"Error: Ya existe un cliente con el correo '{email}'.")
        except Exception as e:
            print(f"Error al modificar el cliente: {e}")

    def obtener_clientes(self) -> List[Cliente]:
        """
        Obtiene todos los clientes de la base de datos.
        """
        try:
            with Session(self.engine) as session:
                clientes = session.query(Cliente).all()
            return clientes
        except Exception as e:
            print(f"Error al obtener los clientes: {e}")
            return []

    def eliminar_cliente(self, id: int):
        """
        Elimina un cliente de la base de datos por su ID.
        """
        try:
            with Session(self.engine) as session:
                # Buscar cliente por ID
                cliente = session.query(Cliente).filter_by(id=id).first()
                if cliente:
                    session.delete(cliente)
                    session.commit()
                    print(f"Cliente con ID {id} eliminado correctamente.")
                else:
                    print(f"No se encontró ningún cliente con el ID {id}.")
        except IntegrityError as e:
            print(f"Error al eliminar el cliente con ID {id}: {e}")
        except Exception as e:
            print(f"Error general al eliminar el cliente: {e}")
