# Import section
from flask import Blueprint, jsonify,abort,request,render_template
import json
from core.database import db_session
from core.models import Administrator, Organization, CommonUser, Plan, Service
import safeglobals


# Initializing the blueprint
mod_signup = Blueprint("mod_signup",__name__)

# Routes
@mod_signup.route("/",methods=["POST","GET"])
def sign_up():
    if request.method == "GET":
        return render_template("signup.html",title="Application :: Sign Up")
    else:
        data = request.get_json()
        try:
            if not data['name'] or not data['email'] or not data['pass'] or not data['plan'] or not data['admin']:
                abort(safeglobals.http_bad_request,{'message':safeglobals.error_mandatory_missing})
        except KeyError:
            abort(safeglobals.http_bad_request,{'message':safeglobals.error_mandatory_missing})

        # Checking that no user with this "email" already exists
        user = Administrator.query.filter_by(email=data['email']).first()
        if user is not None:
            abort(safeglobals.http_conflict,{'message':safeglobals.error_account_exists})
        user = CommonUser.query.filter_by(email=data['email']).first()
        if user is not None:
            abort(safeglobals.http_conflict,{'message':safeglobals.error_account_exists})

        # Creating new Administrator
        admin = Administrator(data['admin'],data['email'])
        admin.hash_password(data['pass'])

        # Getting all services
        services = Service.query.all()

        # Common user
        user = CommonUser(data['admin'],data['email'])
        user.hash_password(data['pass'])
        user.services = services
        
        # Creating a plan
        plan = Plan.query.get(data['plan'])

        # Creating organization
        org = Organization(data['name'])
        org.administrators.append(admin)
        org.users.append(user)
        org.plan = plan
        org.set_expiration_values(data['plan'])
        org.set_premium(data['plan'])

        db_session.add(org)
        db_session.add(admin)
        db_session.add(user)
        db_session.commit()

        return jsonify(status=safeglobals.http_created),safeglobals.http_created



