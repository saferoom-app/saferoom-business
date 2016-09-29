# Import section
from flask import Blueprint, jsonify,abort,request,render_template,session
import json
from core.database import db_session
import safeglobals
from core.decorators import is_authenticated
from core.models import CommonUser,Service,Administrator

# Initializing the blueprint
mod_admin = Blueprint("mod_admin",__name__)

# Routes
@mod_admin.route("/",methods=["GET"])
@is_authenticated
def index_page():
	return render_template("index.html",title="Main page")


# Services route
@mod_admin.route("/services",methods=["GET"])
@is_authenticated
def index_services():
	return render_template("services.html",title="Services")

@mod_admin.route("/users",methods=["GET","POST"])
@is_authenticated
def index_users():
	if request.method == "GET":
		return render_template("users.html",title="Users")
	else:
		response = []
		users = CommonUser.query.all()
		for user in users:
			response.append({"name":user.name,\
				"email":user.email,\
				"created":user.created,\
				"id":user.encrypt_user_id(session['token'])})
		print response
		return render_template("users.list.html",items=response);

@mod_admin.route("/users/create",methods=["POST"])
@is_authenticated
def create_user():
	
	# Getting JSON data
	data = request.get_json()
	
	# Checking request
	if "name" not in data or "email" not in data or "pass" not in data:
		abort(safeglobals.http_bad_request,{"message":safeglobals.error_mandatory_missing})

	# Checking if user already exists
	user = CommonUser.query.filter_by(email=data['email']).first()
	if user is not None:
		abort(safeglobals.http_conflict,{"message":safeglobals.error_account_exists})

	# Getting Organization ID
	admin = Administrator.query.filter_by(session_key=session['token']).first()

	# Creating new user
	user = CommonUser(data['name'],data['email'])
	user.hash_password(data['pass'])
	user.org = admin.org
	services = []
	result = None

	# Setting services
	for service in data['services']:
		if service['enabled'] == True:
			result = Service.query.get(service['id'])
			if result is not None:
				services.append(result)

	user.services = services
	# Adding user to database
	db_session.add(user)
	db_session.commit()

	# Sending response
	return jsonify(status=safeglobals.http_created)