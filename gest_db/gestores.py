from bson import ObjectId


def insert_document(_db, _type, _document):
    _db[_type].insert_one(_document)
    print("Documento insertado correctamente")


def update_document(_db, _type, _id, _document):
    _db[_type].update_one({"_id": ObjectId(_id)}, {"$set": _document})
    print("Documento actualizado correctamente")
