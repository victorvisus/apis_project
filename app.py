# importar flask

import datetime
import os

from bson import ObjectId, json_util
from dotenv import load_dotenv
from flask import Flask, Response, render_template, request

import gest_db.gestores as gest

# importo la conexxion a la BBDD
from gest_db.conexion import connect_to_db

# ////////////////////////////////////////////////////////////////////////   BASE DE DATOS    //// #

load_dotenv()
MONGO_URI = os.environ.get("MONGO_URI")
DATABASE_NAME = os.environ.get("DATABASE_NAME")

try:
    db = connect_to_db(MONGO_URI, DATABASE_NAME)
    if db is not None:
        print(f"✅ Conectado con éxito a la base de datos: {DATABASE_NAME}")
except ValueError as e:
    print(e)
except Exception as e:
    print(e)


# //////////////////////////////////////////////////////////////////////////////    MODELO    //// #
def fetch_all_data(_db):
    data_list = list(_db.students.find())
    data_list = json_util.dumps(data_list, indent=4)
    # print(data_list)
    return data_list


def fetch_student_by_id(_db, _id):
    student = _db.students.find({"_id": ObjectId(_id)})
    return json_util.dumps(student)


# independientemente del navegador, se prueba que funciona bien
# el fetch desde el modelo:
# print(fetch_all_data())


# ///////////////////////////////////////////////////////////////////////////////    VISTA    //// #

app = Flask(__name__)


@app.route("/")  # este decorador crea la ruta de inicio
def index():
    """
    Esta función es llamada cuando se ingresa a la ruta principal
    de la aplicación. Renderiza la plantilla index.html con
    los datos necesarios para mostrar la página principal.
    """
    techs = ["HTML", "CSS", "Flask", "Python"]
    name = "API Project, testeando las APIs"
    return render_template(
        "index.html", techs=techs, name=name, title="Página principal"
    )


@app.route("/about")
def about():
    """
    Esta función es llamada cuando se ingresa a la ruta /about. Renderiza la
    plantilla about.html con los datos necesarios para mostrar la página
    de acerca de nosotros.
    """
    name = "Sobre Nosotros"
    return render_template("about.html", name=name, title="Acerca de nosotros")


@app.route("/formulario", methods=["GET"])
def formulario():
    """
    Esta función es llamada cuando se ingresa a la ruta /formulario. Renderiza la
    plantilla formulario.html con los datos necesarios para mostrar el formulario.
    """
    name = "Formulario"
    return render_template("formulario.html", name=name, title="Formulario")


# /////////////////////////////////////////////////////////////////////////    CONTROLADOR    //// #


@app.route("/api/v1.0/students", methods=["GET"])
def api_students():
    """
    Obtener todos los estudiantes, desde la BBDD

    Returns:
        Response -- objeto de respuesta con los datos de los estudiantes en formato JSON
    """
    return Response(fetch_all_data(db), mimetype="application/json")


@app.route("/result", methods=["POST"])
def store_student():
    name = request.form["name"]
    country = request.form["country"]
    city = request.form["city"]
    skills = request.form["skills"].split(", ")
    bio = request.form["bio"]
    birthyear = request.form["birthyear"]
    created_at = datetime.datetime.now()
    student = {
        "name": name,
        "country": country,
        "city": city,
        "birthyear": birthyear,
        "skills": skills,
        "bio": bio,
        "created_at": created_at,
    }
    gest.insert_document(db, "students", student)
    return render_template("result.html", result_data=student, title="Resultado")


if __name__ == "__main__":
    # usado en despliegue
    # para que funcione en producción y desarrollo
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port, use_reloader=False)
