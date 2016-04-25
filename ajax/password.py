from flask.ext.httpauth import HTTPBasicAuth
from flask import render_template
from flask import request
from flask import jsonify

auth = HTTPBasicAuth()

@auth.route('ajax/password.py')
def verify_password():
    searchword = request.args.get('username', 'password')
    if searchword[0] == '123' and searchword[1] == '123456':
        return jsonify(result=True)