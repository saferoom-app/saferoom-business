# Import section
from flask import Blueprint, jsonify,abort,request,render_template
import json
from core.decorators import token_required
from core.database import db_session
from core.models import CommonUser, Organization, Token, CommonUser

# Initializing the blueprint
mod_users = Blueprint("mod_users",__name__)

@mod_users.route("/add",methods=["POST"])
def add_user():
    data = request.get_json()
    if "org" not in data:
        abort(400,{"message":"Mandatory data is missing"})
    if "name" not in data:
    	abort(400,{"message":"Mandatory data is missing"})
    if "email" not in data:
    	abort(400,{"message":"Mandatory data is missing"})
    if "pass" not in data:
    	abort(400,{"message":"Mandatory data is missing"})

    # Creating a new user
    org = Organization.query.get(data['org'])
    if org is None:
        abort(400,{'message':'Organization not found'})
    u = CommonUser(name=data['name'],email=data['email'])
    u.hash_password(data['pass'])

    # Sending response
    return jsonify(status="ok",name=data['name'],email=data['email'])


@mod_users.route("/signin",methods=["POST"])
def sign_in():

    # Checking the request
    data = request.get_json()
    if "email" not in data or "pass" not in data:
        abort(400,{"message":"Mandatory information missing"})

    # Getting the user with the specified email
    user = CommonUser.query.filter_by(email=data['email']).first()
    if not user or not user.verify_password(data['pass']):
        abort(403,{'message':'User not found'})
   
    # Creating token
    token = Token(user.generate_auth_token())
    token.user = user

    # Deleting previous token
    Token.query.filter_by(uid=user.id).delete()

    # Inserting token into database
    db_session.add(token)
    db_session.commit()

    # Sending response
    return jsonify(token=token.token)

@mod_users.route("/list",methods=["GET"])
@token_required
def list_users():
    users = []
    result = CommonUser.query.all()
    for user in result:
        users.append({"name":user.name,"email":user.email})
    return jsonify(users)

