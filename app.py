# importar flask

import os

import certifi
from bson import json_util
from dotenv import load_dotenv
from flask import Flask, Response, render_template
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# //////////////////////////////////////////////////////////////////////////////////////////    BASE DE DATOS    //// #

load_dotenv()
ca = certifi.where()

MONGO_URI = os.environ.get("MONGO_URI")
# Create a new client and connect to the server
client = MongoClient(MONGO_URI, server_api=ServerApi("1"), tlsCAFile=ca)

# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")

except Exception as e:
    print(e)

# CREAR BASE DE DATOS: db = client["thirty_days_of_python"]
db = client.thirty_days_of_python  # la primera vez se crea la base de datos


# /////////////////////////////////////////////////////////////////////////////////////////////////    MODELO    //// #
def obtenerDatos():
    data_list = list(db.students.find())
    data_list = json_util.dumps(data_list, indent=4)
    print(data_list)
    return data_list


# independientemente del navegador, se prueba que funciona bien
# el fetch desde el modelo:
# losEstudiantes = obtenerDatos()


# //////////////////////////////////////////////////////////////////////////////////////////////////    VISTA    //// #

app = Flask(__name__)


@app.route("/")  # este decorador crea la ruta de inicio
def home():
    """
    Esta función es llamada cuando se ingresa a la ruta principal
    de la aplicación. Renderiza la plantilla home.html con
    los datos necesarios para mostrar la página principal.
    """
    techs = ["HTML", "CSS", "Flask", "Python"]
    name = "API Project, testeando las APIs"
    return render_template(
        "home.html", techs=techs, name=name, title="Página principal"
    )


@app.route("/about")
def about():
    name = "Sobre Nosotros"
    return render_template("about.html", name=name, title="Acerca de nosotros")


@app.route("/post", methods=["GET"])
def post():
    name = "Formulario"
    return render_template("post.html", name=name, title="Formulario")


@app.route("/result", methods=["POST"])
def result():
    """first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    old_job = request.form["old_job"]
    current_job = request.form["current_job"]
    country = request.form["country"]
    print(first_name, last_name, old_job, current_job, country)
    result_data = {
        "first_name": first_name,
        "last_name": last_name,
        "old_job": old_job,
        "current_job": current_job,
        "country": country,
    }"""
    result_data = {}
    return render_template("result.html", result_data=result_data, title="Resultado")


# ////////////////////////////////////////////////////////////////////////////////////////////    CONTROLADOR    //// #


@app.route("/api/v1.0/students", methods=["GET"])
def api_students():
    """
    Obtener todos los estudiantes, desde la BBDD

    Returns:
        Response -- objeto de respuesta con los datos de los estudiantes en formato JSON
    """
    return Response(obtenerDatos(), mimetype="application/json")


@app.route("/students/result", methods=["POST"])
def store_student():
    print("hellouuu")


if __name__ == "__main__":
    # usado en despliegue
    # para que funcione en producción y desarrollo
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port, use_reloader=False)
