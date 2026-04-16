# importar flask

import os

import certifi
from bson import ObjectId, json_util
from dotenv import load_dotenv
from flask import Flask, Response, render_template
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# ////////////////////////////////////////////////////////////////////////   BASE DE DATOS    //// #

load_dotenv()
ca = certifi.where()

MONGO_URI = os.environ.get("MONGO_URI")
BBDD = os.environ.get("BBDD")


con = MongoClient(MONGO_URI, server_api=ServerApi("1"), tlsCAFile=ca)
if not BBDD:
    raise ValueError("BBDD environment variable is not set")

try:
    db = con[BBDD]

    # Send a ping to confirm a successful connection
    con.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except ValueError as e:
    print(e)
except Exception as e:
    print(e)


# //////////////////////////////////////////////////////////////////////////////    MODELO    //// #
def fetch_all_data():
    data_list = list(db.students.find())
    data_list = json_util.dumps(data_list, indent=4)
    # print(data_list)
    return data_list


def fetch_student_by_id(id):
    student = db.students.find({"_id": ObjectId(id)})
    return json_util.dumps(student)


def insert_student_document(document):
    db.students.insert_one(document)
    print("Documento insertado correctamente")


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


@app.route("/result", methods=["POST"])
def result():
    """
    Muestra el resultado de los datos recogidos en el formulario en la plantilla result.html.

    Returns:
        Response -- objeto de respuesta con el resultado del formulario en formato HTML
    """

    result_data = {}
    return render_template("result.html", result_data=result_data, title="Resultado")


# /////////////////////////////////////////////////////////////////////////    CONTROLADOR    //// #


@app.route("/api/v1.0/students", methods=["GET"])
def api_students():
    """
    Obtener todos los estudiantes, desde la BBDD

    Returns:
        Response -- objeto de respuesta con los datos de los estudiantes en formato JSON
    """
    return Response(fetch_all_data(), mimetype="application/json")


@app.route("/students/result", methods=["POST"])
def store_student():
    return "hellouuu"


if __name__ == "__main__":
    # usado en despliegue
    # para que funcione en producción y desarrollo
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port, use_reloader=False)
