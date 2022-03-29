from crypt import methods
from marshmallow import Schema, fields, ValidationError
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from shapely.geometry import Point, shape
from markupsafe import escape
import sqlalchemy
import json
import os

# Schemas de validacion
class ArtistSchema(Schema):
    name = fields.Str(required=True)
    age = fields.Int(required=True)

class AlbumSchema(Schema):
    title = fields.Str()
    release_date = fields.Date()
    artist = fields.Nested(ArtistSchema)

# instancia de Flask
app = Flask(__name__)

# configuracion ORM
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://node:node@localhost:3306/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# instancia base de datos
db = SQLAlchemy(app)

# Modelos a la base de datos
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    salary = db.Column(db.Float, nullable=False)

# squema para validar el request body
class SchemaUser(Schema):
    username = fields.Str(required=True)
    age = fields.Int(required=True)
    salary = fields.Float(required=True)

# metodo para crear las tablas
db.create_all()

# rutas
@app.route("/createUser", methods=['POST'])
def create_user():
    data_values = request.json
    schema = SchemaUser()
    try:
        schema.load(data_values)
    except ValidationError as err:
        return jsonify(err.messages), 400
    user = User(username=data_values['username'], age=data_values['age'], salary=data_values['salary'])
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({'success': 'Se inserto los registros'})
    except sqlalchemy.exc.IntegrityError as err:
        return jsonify({'error': err.__str__() }), 400

@app.route("/createMultipleUser", methods=['POST'])
def create_multiple_users():
    data_values = request.json
    schema = SchemaUser(many=True)
    try:
        schema.load(data_values)
    except ValidationError as err:
        return jsonify(err.messages), 400
    bulk_users = [User(username=row['username'], age=row['age'], salary=row['salary']) for row in data_values]
    try:
        db.session.add_all(bulk_users)
        db.session.commit()
        return jsonify({'success':'Se inserto los registros'})
    except sqlalchemy.exc.IntegrityError as err:
        return jsonify({'error': err.__str__() }), 400

class SchemaCoordinates(Schema):
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)

# proceso para las coordenadas
def locate_coordinates(latitude, longitude):
    path_geojson = "/Users/bryanlonso/proyectos/django_project/src/static/peru_distritos.geojson"
    if not os.path.isfile(path_geojson):
        return None
    with open(path_geojson) as read_geojson:
        dataset = json.load(read_geojson)
    point = Point(longitude, latitude)
    response_value = { 'nombdist':'', 'nomprov': '', 'nombdep':''}
    for row in dataset['features']:
        try:
            polygon = shape(row['geometry'])
            if polygon.contains(point):
                response_value['nombdist'] = row['properties']['NOMBDIST']
                response_value['nomprov'] = row['properties']['NOMBPROV']
                response_value['nombdep'] = row['properties']['NOMBDEP']
        except:
            None
    return response_value

@app.route('/locate', methods=['POST'])
def coordinates():
    req = request.json
    schema = SchemaCoordinates()
    try:
        schema.load(req)
    except ValidationError as err:
        return jsonify(err.messages), 400
    lat, lon = req['latitude'], req['longitude']
    response = locate_coordinates(lat, lon)
    if response is None:
        return jsonify({'error': 'No se encuentran coordenadas'}), 400
    return jsonify(response)

@app.route('/locateMultipleCoordinates', methods=['POST'])
def locate_multiple_coordinates():
    req = request.json
    schema = SchemaCoordinates(many=True)
    try:
        schema.load(req)
    except ValidationError as err:
        return jsonify(err.messages), 400
    data_values = []
    for row in req:
        lat, lon = row['latitude'], row['longitude']
        response = locate_coordinates(lat, lon)
        if response is None:
            None
        data_values.append(response)
    return jsonify(data_values)

@app.route("/task", methods=['POST'])
def create_task():
    response = request.json
    schema = ArtistSchema()
    try:
        result = schema.load(response)
        print(result)
        return jsonify(response)
    except ValidationError as err:
        print(err.messages)
        return jsonify(err.messages)

@app.route("/user/<username>")
def show_user_profile(username):
    return f"User {escape(username)}"

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    return f"Post {escape(post_id)}"

# instancia principal
if __name__ == '__main__':
    app.run(debug=True, port=4040)
