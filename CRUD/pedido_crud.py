import sqlalchemy as db
from sqlalchemy.orm import Session
from models import Pedido
# para verificar tipos de dato de lista
from typing import List 
# para manejar excepciones
from sqlalchemy.exc import IntegrityError 
from sqlalchemy.orm.exc import NoResultFound

 
# esta clase se conecta a la base de datos cada vez que se instacia un objeto
class PedidoCRUD():
    def __init__(self):
        self.engine = db.create_engine("sqlite:///bd/inventario.db", echo=True, future=True)
        
    # ahora vamos a crear el metodo para ingresar un nuevo Pedido
    def ingresar_pedido(self, cliente, menus):
        # llamamos al modelo ORM en esta variable
        producto = Pedido()
        # Asignamos los valores
        producto.cliente = cliente
        producto.menus = menus
        # abrimos una sesion al motor y agregamos el modelo como un registro dentro de la tabla Ingrediente
        with Session(self.engine) as session:
            session.add(producto)
            session.commit()
        
    # ahora vamos a crear un metodo para obtener una lista con los registros de la base de datos
    def obtener_pedidos(self) -> List[Pedido]:
        productos: Pedido = None
        # abrimos una sesion y hacemos una consulta que obtiene todos los registros de la tabla
        with Session (self.engine) as session:
            productos = session.query(Pedido).all()
        return productos
    