"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
import json
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Endpoint que muestra todos los miembros de la familia
@app.route('/members', methods=['GET'])
def route_get_members():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()

    return jsonify(members), 200

# Endpoint que muestra un miembro de la familia
@app.route('/member/<int:member_id>', methods=['GET'])
def route_get_member(member_id):

    member = jackson_family.get_member(member_id)

    return jsonify(member), 200

# Endpoint que agrega un miembro de la familia
@app.route('/member', methods=['POST'])
def route_add_member():

    body = json.loads(request.data)
    member = jackson_family.add_member(body)

    return "Se agregó el familiar de manera satisfactoria", 200

# Endpoint que elimina un miembro de la familia
@app.route('/member/<int:member_id>', methods=['DELETE'])
def route_delete_member(member_id):

    member = jackson_family.delete_member(member_id)

    if member == True:
        return "Se eliminó el familiar de manera satisfactoria", 200
    else:
        return "No se pudo eliminar el familiar", 400

# Endpoint que actualiza la lista de miembros de la familia
@app.route('/member/<int:member_id>', methods=['PUT'])
def route_put_member(member_id):

    body = json.loads(request.data)
    member = jackson_family.update_member(member_id, body)

    if member == True:
        return "Se actualizó el familiar de manera satisfactoria", 200
    else:
        return "No se pudo actualizar el familiar", 400

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
