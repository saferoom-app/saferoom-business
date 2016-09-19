# Import section
import os
from flask import Flask, abort, request, jsonify, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from database import db_session,init_db
from modules.mod_org import mod_org
from modules.mod_users import mod_users
from models import Administrator


# Initializing the app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.register_blueprint(mod_org,url_prefix="/orgs")
app.register_blueprint(mod_users,url_prefix="/users")


@app.route("/init",methods=["GET"])
def init_database():
    init_db()
    return jsonify(status="ok")

@app.route("/signin",methods=["POST"])
def signin():
    
    # Getting JSON data
    data = request.get_json()

    # Checking the request
    if "email" not in data or "pass" not in data:
        abort(400)

    # Checking that this admin exists
    admin = Administrator.query.filter_by(email=data['email']).first()
    if not admin or not admin.verify_password(data['pass']):
        abort(403)

    # Sending response
    return "OK"    


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(debug=True)