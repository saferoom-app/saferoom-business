# Import section
import os
from flask import Flask, abort, request, jsonify, g, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from core.database import db_session,init_db
from modules.mod_org import mod_org
from modules.mod_users import mod_users
from modules.mod_auth import mod_auth
from modules.mod_signup import mod_signup
from modules.mod_admin import mod_admin
from modules.mod_modal import mod_modal
from core.models import Administrator, Plan, Service
import safeglobals


# Initializing the app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.register_blueprint(mod_org,url_prefix="/orgs")
app.register_blueprint(mod_users,url_prefix="/users")
app.register_blueprint(mod_auth,url_prefix="/signin")
app.register_blueprint(mod_signup,url_prefix="/signup")
app.register_blueprint(mod_admin,url_prefix="/admin");
app.register_blueprint(mod_modal,url_prefix="/modal")


@app.route("/init",methods=["GET"])
def init_database():
    init_db()

    # Creating plans
    plans = [Plan("Free",False),Plan("Basic",False),Plan("Premium",True)]
    
    # Creating services
    services = [Service(name="Evernote"),Service(name="Onenote")]

    db_session.add_all(plans)
    db_session.add_all(services)
    db_session.commit()
    return jsonify(status="ok")


@app.errorhandler(400)
def custom_400(error):
    return jsonify({'message': error.description['message']}),400

@app.errorhandler(403)
def custom_403(error):
    return jsonify({'message': error.description['message']}),403

@app.errorhandler(500)
def custom_500(error):
	return jsonify({'message': safeglobals.error_server_internal}),500

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.errorhandler(409)
def custom_409(error):
    return jsonify({'message': error.description['message']}),409



@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == '__main__':
    app.run(debug=True)