# Import section
from flask import Blueprint, jsonify,abort,request,render_template,session
import json
from core.database import db_session
from core.models import Administrator
import safeglobals
import time


# Initializing the blueprint
mod_auth = Blueprint("mod_auth",__name__)

# Routes
@mod_auth.route("/",methods=["POST","GET"])
def signin():
    
    # IF its GET request, display the page
    if request.method == "GET":
        return render_template("signin.html",title="Application :: Sign In")

    # Getting JSON data
    data = request.get_json()

    # Checking the request
    if "email" not in data or "pass" not in data:
        abort(safeglobals.http_bad_request,{"message":safeglobals.error_mandatory_missing})

    # Checking that this admin exists
    admin = Administrator.query.filter_by(email=data['email']).first()
    if not admin or not admin.verify_password(data['pass']):
        abort(safeglobals.http_forbidden,{'message':safeglobals.error_access_denied})

    # Generating a token and put into session
    admin.generate_session_key()
    db_session.commit()
    session['token'] = admin.session_key

    # Sending response
    '''return jsonify(status=safeglobals.http_ok,\
        user=admin.name,\
        email=admin.email,\
        org=admin.orgs.name,\
        evaluate_to=time.mktime(admin.orgs.evaluate_to.timetuple()),\
        expires_in=time.mktime(admin.orgs.expires_in.timetuple()))'''

    return jsonify(status=safeglobals.http_ok)

