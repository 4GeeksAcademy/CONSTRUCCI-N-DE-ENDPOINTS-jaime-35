"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,Favorite,Favorite_types,Planet,People
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_get_user():
    user = User.query.all()
    user = list(map(lambda p: p.serialize(),user))
    return jsonify(user),200
   

   
@app.route('/planets', methods=['GET'])
def handle_get_planets():
    planets = Planet.query.all()
    planets = list(map(lambda p: p.serialize(),planets))
    return jsonify(planets)



@app.route('/people', methods=['GET'])
def handle_get_people():
    people = People.query.all()
    people = list(map(lambda p: p.serialize(),people))

    return jsonify(people)



@app.route("/favorites/<int:userId>", methods=["GET"])
def handle_get_favorites(userId):
    user_favorites = Favorite.query.filter_by(user_id=userId).all()
    user_favorites = list(map(lambda fav:fav.serialize(), user_favorites))
    return jsonify(user_favorites),200




@app.route("/favorites/planet/<int:planet_id>", methods=["POST"])
def handle_post_planet(planet_id):
    user= User.query.first()
    new_favorites = Favorite(user_id=user.id, planet_id=planet_id,type="planet")

    db.session.add(new_favorites)
    db.session.commit()
    return jsonify({"msg": "creado con exito"}),200



@app.route("/favorites/people/<int:people_id>", methods=["POST"])
def handle_post_people(people_id):
    user= User.query.first()
    new_favorites = Favorite(user_id=user.id, people_id=people_id,type="people")

    db.session.add(new_favorites)
    db.session.commit()
    return jsonify({"msg": "creado con exito"}),200



@app.route("/user", methods=["POST"])
def handle_post_user():
    data = request.get_json()
    new_user = User(
        username=data["username"],
        email=data["email"]
        # Puedes agregar otros campos si tienes (password, etc.)
    )
    
   

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "creado con exito"}),200


@app.route("/favorites/<int:favorite_id>", methods=["DELETE"])
def handle_delete_favorite(favorite_id):
    favorite = Favorite.query.get(favorite_id)
    if not favorite:
        return jsonify({"msg": "Favorito no encontrado"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorito eliminado exitosamente"}), 200










# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
