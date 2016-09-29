from functools import wraps
from flask import request, abort,session
from models import Token,CommonUser, Administrator
from database import db_session
import safeglobals

def token_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		bearer_token = request.headers.get('Authorization')
		if bearer_token is None:
			abort(safeglobals.http_forbidden,{'message':safeglobals.error_token_missing})

		# Checking the token
		array = bearer_token.split("Bearer")
		auth_token = str(array[-1]).strip()

		# Verifying the token
		token = Token.query.filter_by(token=auth_token).first()
		if token is None:
			abort(safeglobals.http_forbidden,{'message':safeglobals.error_token_notfound})

		# Checking token expiration
		if Token.verify_auth_token(auth_token) == False:
			db_session.delete(token)
			db_session.commit()
			abort(safeglobals.http_forbidden,{'message':safeglobals.error_token_expired})

		return f(*args, **kwargs)
	return decorated_function

def is_authenticated(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if 'token' not in session:
			abort(safeglobals.http_forbidden,{'message':safeglobals.error_not_authenticated})
		else:
			admin = Administrator.query.filter_by(session_key=session['token'])
			if admin is None:
				abort(safeglobals.http_forbidden,{'message':safeglobals.error_not_authenticated})
		return f(*args, **kwargs)
	return decorated_function