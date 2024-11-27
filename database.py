# estas son todas las importaciones necesarias para configurar nuestra base de datos ademas de importar el modulo "models" con nuestros modelos ORM y el modulo utileria para almacenar nuestra base de datos
import sqlalchemy as db
import models as modelos
from utileria.funciones import crear_carpeta

# aqui vamos a configurar el directorio donde se va a almacenar la base de datos
nombre = "bd"
ruta = "./"

crear_carpeta(ruta, nombre)

# con esta linea creamos el motor de la base de datos
# a url es donde se va a almacenar nuesra base de datos
# el resto de parametros son para que nos mande mensajes en la consola
# ademas ponemos el directorio db para almacenar la base de datos 
engine = db.create_engine("sqlite:///bd/inventario.db", echo=True, future=True) 

# aqui creamos las tablas 
modelos.Base.metadata.create_all(engine)