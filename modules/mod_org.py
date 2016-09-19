# Import section
from flask import Blueprint, jsonify,abort,request,render_template
import json
from database import db_session
from models import Organization, Administrator, CommonUser

# Initializing the blueprint
mod_org = Blueprint("mod_org",__name__)

# Initializing routes
@mod_org.route("/list",methods=['GET'])
def list_orgs():
    result = Organization.list()
    orgs = []
    for item in result:
    	orgs.append({"name":item.name,"id":item.id})
    return jsonify(orgs)

@mod_org.route("/add",methods=["POST"])
def add_org():
    admin = None
    user = None
    data = request.get_json()
    if "name" not in data or "email" not in data or "admin" not in data or "pass" not in data:
        abort(400)

    # First, we need to check if there are already users with this email
    admin = Administrator.query.filter_by(email=data['email']).first()
    if admin is not None:
    	abort(409)
    user = CommonUser.query.filter_by(email=data['email']).first()
    if user is not None:
    	abort(409)

    # Creating new organization, add administrator and user
    org = Organization(data['name'])
    admin = Administrator(name=data['admin'],email=data['email'])
    user = CommonUser(name=data['admin'],email=data['email'])
    admin.hash_password(data['pass'])
    user.hash_password(data['pass'])
    org.administrators.append(admin)
    org.users.append(user)
    db_session.add(org)
    db_session.add(admin)
    db_session.add(user)
    db_session.commit()
    return jsonify(status="ok")