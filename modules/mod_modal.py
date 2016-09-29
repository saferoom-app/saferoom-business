# Import section
from flask import Blueprint, jsonify,abort,request,render_template,session
import json
import safeglobals
from core.decorators import is_authenticated
from core.models import CommonUser, Administrator, Organization

# Initializing the blueprint
mod_modal = Blueprint("mod_modal",__name__)

@mod_modal.route("/createuser",methods=["GET"])
@is_authenticated
def create_user():
	return render_template("dialog.user.create.html")


@mod_modal.route("/getuser",methods=["GET"])
@is_authenticated
def get_user():
    
    uid = ""
    # Checking if user ID has been sent
    if not request.args.get("uid"):
    	abort(safeglobals.http_bad_request,{'message':safeglobals.error_mandatory_missing})

    # Getting the UID from encrypted string
    try:
    	uid = CommonUser.decrypt_user_id(request.args.get('uid'),session['token'])
    except Exception as e:
    	print str(e)
    	abort(safeglobals.http_bad_request,{'message':safeglobals.error_user_notfound})

    # Getting the Admin and User Organization ID
    admin = Administrator.query.filter_by(session_key=session['token']).first()
    user = CommonUser.query.get(uid)
    if user is None:
    	abort(safeglobals.http_bad_request,{'message':safeglobals.error_user_notfound})
    if admin.org.id != user.org.id:
    	abort(safeglobals.http_bad_request,{'message':safeglobals.error_user_notfound})

    # Getting user information
    response = {"name":user.name,"email":user.email}
    response['evernote'] = False
    response['onenote'] = False
    services = user.services
    for service in services:
    	if "Evernote" in service.name:
            response['evernote'] = True
        elif "Onenote" in service.name:
            response['onenote'] = True
    print response
    # Sending response
    return render_template("dialog.user.update.html",user=response)
