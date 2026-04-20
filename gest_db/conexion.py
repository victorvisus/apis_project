import certifi
from pymongo import MongoClient
from pymongo.server_api import ServerApi


def connect_to_db(_MONGO_URI, _DATABASE_NAME):
    ca = certifi.where()
    try:
        con = MongoClient(_MONGO_URI, server_api=ServerApi("1"), tlsCAFile=ca)
        db = con[_DATABASE_NAME]
        con.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")

        return db
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return None
