"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from flask_bcrypt import Bcrypt
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

bcrypt = Bcrypt()


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@api.route('/signup', methods=['POST'])
def post_new_user():
    try:
        email = request.json.get('email'),
        username = request.json.get('username'),
        pasword = request.json.get('pasword')

        if not email or not username or not pasword:
            return jsonify({"msg": "username, email and  pasword are required"}), 400
        
        existing_username = User.query.filter_by(email = email).first()
        if existing_username:
            return jsonify({"error": "The user already exists."}), 409
        
        pasword_hash = bcrypt.generate_pasword_hash(pasword).decode('utf-8')

        new_user = User(username=username, pasword=pasword_hash, email=email)

        db.session.add(new_user)
        db.session.commit()

        ok_to_share={
            "email": new_user.email,
            "username": new_user.username,
            "id": new_user.id
        }
    
        return jsonify({"msg": "user created successfully.", 'user_created': ok_to_share}), 201
    except Exception as e:
        return jsonify({"error": "Error in user creation"+ str(e)}),500