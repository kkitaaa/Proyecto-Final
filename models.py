from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, DateTime, event
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Base para los modelos
Base = declarative_base()


# Modelo Ingrediente
class Ingrediente(Base):
    __tablename__ = 'ingredientes'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True) 
    nombre = Column(String, nullable=False, unique=True)  # Nombre del ingrediente
    tipo = Column(String, nullable=False)  # Tipo del ingrediente (carbohidratos, proteínas, etc.)
    cantidad = Column(Float, nullable=False)  # Cantidad en stock
    unidad = Column(String, nullable=False)  # Unidad de medida (kg, litros, etc.)

    # Relación inversa con Menu
    menus = relationship("Menu", secondary="menu_ingrediente", back_populates="ingredientes")

    def __repr__(self):
        return f"<Ingrediente(nombre={self.nombre}, cantidad={self.cantidad}, unidad={self.unidad})>"

# Tabla intermedia para la relación Menu-Ingrediente
menu_ingrediente = Table(
    'menu_ingrediente', Base.metadata,
    Column('menu_id', Integer, ForeignKey('menus.id'), primary_key=True),
    Column('ingrediente_id', Integer, ForeignKey('ingredientes.id'), primary_key=True),
    Column('cantidad', Float, nullable=False)  # Cantidad requerida del ingrediente para este menú
)

# Modelo Menu
class Menu(Base):
    __tablename__ = 'menus'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False, unique=True)
    descripcion = Column(String, nullable=False, unique=True)
    precio = Column(Float, nullable=False, unique=True)

    # Relación con Ingrediente
    ingredientes = relationship("Ingrediente", secondary=menu_ingrediente, back_populates="menus")

    # Relación con Pedido
    pedidos = relationship("Pedido", secondary="pedido_menu", back_populates="menus")

    def __repr__(self):
        return f"<Menu(nombre={self.nombre})>"

# Modelo Cliente
class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)

    # Relación con Pedido
    pedidos = relationship("Pedido", back_populates="cliente")

    def __repr__(self):
        return f"<Cliente(nombre={self.nombre}, email={self.email})>"

# Tabla intermedia para la relación Pedido-Menu
pedido_menu = Table(
    'pedido_menu', Base.metadata,
    Column('pedido_id', Integer, ForeignKey('pedidos.id'), primary_key=True),
    Column('menu_id', Integer, ForeignKey('menus.id'), primary_key=True),
    Column('cantidad', Integer, nullable=False)  # Cantidad de este menú en el pedido
)

# Modelo Pedido
class Pedido(Base):
    __tablename__ = 'pedidos'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    fecha = Column(DateTime, default=datetime.utcnow)  # Fecha y hora de creación
    total = Column(Float, default=0.0, nullable=False)  # Monto total del pedido

    # Relación con Cliente
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    cliente = relationship("Cliente", back_populates="pedidos")

    # Relación con Menu
    menus = relationship("Menu", secondary=pedido_menu, back_populates="pedidos")

    def __repr__(self):
        return f"<Pedido(id={self.id}, fecha={self.fecha}, total={self.total})>"

# Evento para actualizar el total del pedido antes de guardar
@event.listens_for(Pedido.menus, 'append')
def actualizar_total_pedido(target, value, initiator):
    """
    Actualiza el total del pedido cuando se agregan menús.
    """
    pedido_menu_entry = next(
        (entry for entry in target.menus if entry.id == value.id), None
    )
    if pedido_menu_entry:
        cantidad = pedido_menu_entry.cantidad
        target.total += value.precio * cantidad