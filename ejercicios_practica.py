#!/usr/bin/env python
'''
SQL Introducción [Python]
Ejercicios de práctica
---------------------------
Autor: Inove Coding School
Version: 1.1

Descripcion:
Programa creado para poner a prueba los conocimientos
adquiridos durante la clase
'''

__author__ = "Inove Coding School"
__email__ = "alumnos@inove.com.ar"
__version__ = "1.1"

import sqlite3
import os
import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey #  Herramientas para crear una tabla
from sqlalchemy.ext.declarative import declarative_base    # Molde para tablas de bases de datos
from sqlalchemy.orm import sessionmaker, relationship      # Sirve para poder relaciona dos tablas

# Visualizador de bases de datos .db:
# https://extendsclass.com/sqlite-browser.html 

# Crear el motor (engine) de la base de datos
engine = sqlalchemy.create_engine("sqlite:///secundaria.db")
base = declarative_base()


class Tutor(base):
    __tablename__ = "tutor"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    def __repr__(self):
        return f"Tutor: {self.name}"


class Estudiante(base):
    __tablename__ = "estudiante"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    grade = Column(Integer)
    tutor_id = Column(Integer, ForeignKey("tutor.id"))

    tutor = relationship("Tutor")

    def __repr__(self):
        return f"Estudiante: {self.name}, edad {self.age}, grado {self.grade}, tutor {self.tutor.name}"


def create_schema():
    # Borrar todos las tablas existentes en la base de datos
    # Esta linea puede comentarse para no eliminar los datos
    base.metadata.drop_all(engine)

    # Crear las tablas
    base.metadata.create_all(engine)


def insert_tutor(tutor_name):

   # Crear sesión
    Session = sessionmaker(bind=engine)
    session = Session()

    tutor = Tutor(name=tutor_name)

    # Agregar Tutor
    session.add(tutor)
    session.commit()
    print(f"Se añadió al tutor {tutor_name} a la db")


def insert_estudiante(estudiante_name, estudiante_age, grade, tutor_name):

    # Crear la session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Buscar el Tutor
    query = session.query(Tutor).filter(Tutor.name == tutor_name)
    tutor_Number = query.first()

    if tutor_Number is None:
        # Este condicional surge si el nombre del tutor no esta definido en la la tabla de tutores creada
        print(f"Error al crear el estudiante {estudiante_name}, no existe el tutor {tutor_name}")
        return

    # Crear el nuevo estudiante
    estudent = Estudiante(name=estudiante_name, age=estudiante_age, grade=grade)
    estudent.tutor = tutor_Number

    # estudent = Estudiante(name=estudiante_name, age=estudiante_age, tutor_id=tutor_Number)

    # Agregar el estudiante a la DB
    session.add(estudent)
    session.commit()
    print(f"Se añadió al estudiante {estudiante_name} a la db")




def fill():
    print('Completemos esta tablita!')
    # Llenar la tabla de la secundaria con al munos 2 tutores
    # Cada tutor tiene los campos:
    # id --> este campo es auto incremental por lo que no deberá completarlo
    # name --> El nombre del tutor (puede ser solo nombre sin apellido)

    # Llenar la tabla de la secundaria con al menos 5 estudiantes
    # Cada estudiante tiene los posibles campos:
    # id --> este campo es auto incremental por lo que no deberá completarlo
    # name --> El nombre del estudiante (puede ser solo nombre sin apellido)
    # age --> cuantos años tiene el estudiante
    # grade --> en que año de la secundaria Hogwarts se encuentra (1-7)
    # tutor --> el tutor de ese estudiante (el objeto creado antes)

    # No olvidarse que antes de poder crear un estudiante debe haberse
    # primero creado el tutor.

    # TUTORES
    insert_tutor("Godric Gryffindor")
    insert_tutor("Rowena Ravenclaw")
    insert_tutor("Helga Hufflepuff")
    insert_tutor("Salazar Slytherin")
    insert_tutor("La Muerte💀")

    # ESTUDIANTES
    # Recordar: insert_estudiante(name , age, grade, tutor)
    
    insert_estudiante("Rubeus Hagrid",13,3,"Godric Gryffindor")        # Fue expulsado en su 3er año acusado de abrir la cámara de los secretos.
    insert_estudiante("Fred Weasley",17,6,"Godric Gryffindor")         # Dejó la escuela en su 7mo año, desafiando a Umbridge.
    insert_estudiante("George Weasley",17,6,"Godric Gryffindor")       # Dejó la escuela en su 7mo año, desafiando a Umbridge.
    insert_estudiante("Thomas Riddle",18,7,"Salazar Slytherin")        # Terminó la escuela. Tuvo gran exito en sus futuros emprendimientos.
    insert_estudiante("Cedric Diggory ",18,7,"Helga Hufflepuff")       # Fue asesinado por Voldemort en el campeonato del Caliz de Fuego.
    insert_estudiante("Hermione Granger",18,7,"Godric Gryffindor")     # Terminó la escuela.
    insert_estudiante("Ron Weasley",18,7,"Godric Gryffindor")          # Terminó la escuela.
    insert_estudiante("Severus Snape",18,7,"Salazar Slytherin")        # Terminó la escuela, los rumores dicen que era el Príncipe Mestizo.
    insert_estudiante("Luna Lovegood",18,7,"Rowena Ravenclaw")         # Terminó la escuela.
    insert_estudiante("Jane Doe",15,5,"Helga Hufflepuff")              # A nadie le importa Hufflepuff.
    insert_estudiante("Myrtle Llorona Warren",14,4,"Rowena Ravenclaw") # Fue asesinada por el Basilisco al abrirse la cámara de los secretos.
    insert_estudiante("Garrick Ollivander",18,7,"Rowena Ravenclaw")    # Terminó la escuela.
    insert_estudiante("Dolores Umbridge",18,7,"Salazar Slytherin")     # Nadie la extraña.




def fetch():
    print('Comprobemos su contenido, ¿qué hay en la tabla?')
    # Crear una query para imprimir en pantalla
    # todos los objetos creados de la tabla estudiante.
    # Imprimir en pantalla cada objeto que traiga la query
    # Realizar un bucle para imprimir de una fila a la vez

    # Crear la session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Buscar todas las personas
    query = session.query(Estudiante)

    # Leer una persona a la vez e imprimir en pantalla
    for persona in query:
        print(persona)

def search_by_tutor(tutor):
    print('Operación búsqueda!')
    # Esta función recibe como parámetro el nombre de un posible tutor.
    # Crear una query para imprimir en pantalla
    # aquellos estudiantes que tengan asignado dicho tutor.

    # Para poder realizar esta query debe usar join, ya que
    # deberá crear la query para la tabla estudiante pero
    # buscar por la propiedad de tutor.name
    
    # Crear la session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Buscar todas las personas
    query = session.query(Estudiante).join(Estudiante.tutor).filter(Tutor.name == tutor)


    # Leer una persona a la vez e imprimir en pantalla
    for persona in query:
        print(persona)


def modify(student_id, name_tutor):
    print('Modificando la tabla')
    # Deberá actualizar el tutor de un estudiante, cambiarlo para eso debe
    # 1) buscar con una query el tutor por "tutor.name" usando name
    # pasado como parámetro y obtener el objeto del tutor
    # 2) buscar con una query el estudiante por "estudiante.id" usando
    # el id pasado como parámetro
    # 3) actualizar el objeto de tutor del estudiante con el obtenido
    # en el punto 1 y actualizar la base de datos

    # TIP: En clase se hizo lo mismo para las nacionalidades con
    # en la función update_persona_nationality

    # Crear la session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Buscar el tutor que se desea actualizar
    query1 = session.query(Tutor).filter(Tutor.name == name_tutor)
    tutor_updateado = query1.first()

    # Buscar la persona que se desea actualizar
    query2 = session.query(Estudiante).filter(Estudiante.id == student_id)
    estudiante_updateado = query2.first()

    # Actualizar la persona con nombre "name"
    estudiante_updateado.tutor = tutor_updateado

    # Aunque la persona ya existe, como el id coincide
    # se actualiza sin generar una nueva entrada en la DB
    session.add(estudiante_updateado)
    session.commit()

    print('Tutor actualizado:', name_tutor)


def count_grade(grade):
    print('Estudiante por grado')
    # Utilizar la sentencia COUNT para contar cuantos estudiante
    # se encuentran cursando el grado "grade" pasado como parámetro
    # Imprimir en pantalla el resultado

    # TIP: En clase se hizo lo mismo para las nacionalidades con
    # en la función count_persona

    # Crear la session
    Session = sessionmaker(bind=engine)
    session = Session()

    contador = session.query(Estudiante.grade).filter(Estudiante.grade == grade).count()
    print("En el año", grade, "hay", contador, "estudiantes.")


if __name__ == '__main__':

    # Seteo directorio
    os.getcwd()
    os.chdir(os.path.dirname(__file__))

    print("Bienvenidos a otra clase de Inove con Python")
    create_schema()   # create and reset database (DB)
    fill()
    fetch()

    tutor = 'Godric Gryffindor'
    search_by_tutor(tutor)

    nuevo_tutor = "La Muerte💀"
    student_id = 5
    modify(student_id, nuevo_tutor)
    fetch()

    grade = 7
    count_grade(grade)
