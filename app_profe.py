import datetime
import os

import certifi
from bson import json_util
from bson.objectid import ObjectId
from dotenv import load_dotenv
from flask import Flask, Response, render_template, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

################################################################
########################## CONEXIÓN BD #########################
################################################################

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


################################################################
########################## MODELO ##############################
################################################################
# Función para el modelo: sobre la conexión de BD, obtiene datos
todos = []


def obtenerDatos():
    todos = list(db.students.find())
    todos = json_util.dumps(todos, indent=4)
    print(todos)
    return todos


def obtenerPorID(id):
    student = db.students.find({"_id": ObjectId(id)})
    return json_util.dumps(student)


def enviarDocumento(documento):
    db.students.insert_one(documento)
    print("Documento insertado correctamente")


# independientemente del navegador, se prueba que funciona bien
# el fetch desde el modelo:
losEstudiantes = obtenerDatos()


################################################################
########################## VISTA ###############################
################################################################
# Esta función es para la vista, sólo para invocar por navegador:
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


################################################################
########################## CONTROLADORES #######################
################################################################


@app.route("/api/v1.0/students", methods=["GET"])
def students():
    return Response(obtenerDatos(), mimetype="application/json")


# Igualamente para la vista, sólo que la presentación es dinámica
@app.route("/students/<id>", methods=["GET"])
def single_student(id):
    student = obtenerPorID(id)
    return Response(student, mimetype="application/json")


@app.route("/students/result", methods=["POST"])
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
    enviarDocumento(student)
    return "Documento insertado correctamente"


def update_student(id):
    pass


################################################################
########################## LANZA EL SERVIDOR ###################
################################################################
if __name__ == "__main__":
    # usado en despliegue
    # para que funcione en producción y desarrollo
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port, use_reloader=False)
