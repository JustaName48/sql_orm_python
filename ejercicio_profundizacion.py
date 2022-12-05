'''
SQL Alchemy [Python]
Ejercicios de Profundización
---------------------------
Autor: Valentín Imperio
Version: 1.0

Descripcion:
Programa creado para poner a prueba los conocimientos
adquiridos durante la clase
'''

import sqlite3
import csv
import requests
import json

import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey #  Herramientas para crear una tabla
from sqlalchemy.ext.declarative import declarative_base    # Molde para tablas de bases de datos
from sqlalchemy.orm import sessionmaker, relationship      # Sirve para poder relaciona dos tablas


# Visualizador de bases de datos .db:
# https://extendsclass.com/sqlite-browser.html 

# Crear el motor (engine) de la base de datos
engine = sqlalchemy.create_engine("sqlite:///meli_data.db")
base = declarative_base()


class Producto(base):
    __tablename__ = 'producto'
    id = Column(String, primary_key=True, autoincrement=False)
    site_id = Column(String)
    title = Column(String)
    price = Column(Integer)
    currency_id = Column(String)
    initial_quantity = Column(Integer)
    available_quantity = Column(Integer)
    sold_quantity = Column(Integer)

    def __repr__(self):
        return f'Producto\nId: {self.id}\nSite id: {self.site_id}\nTitle: {self.title}\
                 \nPrice: {self.price}\nCurrency id: {self.currency_id},\nInitial Quantity: {self.initial_quantity}\
                 \nAvailable Quantity: {self.initial_quantity}\nSold Quantity: {self.sold_quantity}'


def create_schema():
    # Borrar todos las tablas existentes en la base de datos
    # Esta linea puede comentarse para no eliminar los datos
    base.metadata.drop_all(engine)

    # Crear las tablas
    base.metadata.create_all(engine)

def insert_producto(url):
    try:
        data_json = requests.get(url).json()

        data_prod = data_json[0]["body"]

        # Crear la session
        Session = sessionmaker(bind=engine)
        session = Session()

        # Crear el nuevo producto
        producto = Producto(id=data_prod["id"], site_id=data_prod["site_id"], title=data_prod["title"],
                            price=data_prod["price"], currency_id=data_prod["currency_id"], initial_quantity=data_prod["initial_quantity"],
                            available_quantity=data_prod["available_quantity"], sold_quantity=data_prod["sold_quantity"]
                            )
        # Agregar al producto a la DB
        print(producto.id)
        session.add(producto)
        session.commit()
     
    except Exception as e:
        print("Estoy en la excepcion")
        return

def fill():
    # Insertar el archivo CSV de mercadolibre
    # Insertar fila a fila
    with open("meli_technical_challenge_data.csv", "r") as fi:
        data = list(csv.DictReader(fi))

        for row in data:
            item = row["site"] + row["id"]
            url = 'https://api.mercadolibre.com/items?ids={}'.format(item)

            insert_producto(url)
            print("estoy trabajando, esperen!")

def fetch(id_busqueda):
    try:
        print('Comprobemos su contenido, ¿qué hay en la tabla?')

        # Crear la session
        Session = sessionmaker(bind=engine)
        session = Session()

        # Buscar todas las personas
        query = session.query(Producto).filter(Producto.id == id_busqueda)
        producto_buscado = query.first()
        print(producto_buscado)
        
    except Exception as e:
        print("Error 404 - Id not found")
        return


if __name__ == "__main__":
    # Crear DB
    create_schema()

    # Completar la DB con el CSV
    fill()
    print("Listop, terminé!!")

    # Leer filas
    fetch('MLA845041373')
    fetch('MLA717159516')
