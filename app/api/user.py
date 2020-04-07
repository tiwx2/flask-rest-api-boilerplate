from flask import g
from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth

@bp.route('/unprotected')
def unprotected_endpoint():
    return {'message': 'This is an unprotected endpoint'}

@bp.route('/protected')
@basic_auth.login_required
def protected_endpoint():
    return {'message': 'This is a basic auth protected endpoint'}

@bp.route('/token-protected')
@token_auth.login_required
def token_protected_endpoint():
    return {'message': 'This is a token auth protected endpoint'}
