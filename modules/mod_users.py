# Import section
from flask import Blueprint, jsonify,abort,request,render_template
import json
from database import db_session
from models import CommonUser, Organization

# Initializing the blueprint
mod_users = Blueprint("mod_users",__name__)

@mod_users.route("/add",methods=["POST"])
def add_user():
    data = request.get_json()
    if "org" not in data:
        abort(400)
    if "name" not in data:
    	abort(400)
    if "email" not in data:
    	abort(400)
    if "pass" not in data:
    	abort(400)

    # Creating a new user
    org = Organization.query.get(data['org'])
    u = CommonUser(name=data['name'],email=data['email'])
    u.hash_password(data['pass'])
    org.users.append(u)
    db_session.add(u)
    db_session.commit()
    return jsonify(status="ok",name=data['name'],email=data['email'])