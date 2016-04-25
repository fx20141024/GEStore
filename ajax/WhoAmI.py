from flask.ext.httpauth import HTTPBasicAuth
from flask import make_response
from flask import render_template
from flask import jsonify

auth = HTTPBasicAuth()

@auth.verify_position
def verify_position():
    response = make_response(render_template('login.html', foo=42))
    response.headers['position'] = 'engineer'
    return response



@app.route('/_get_current_user')
def get_current_user():
    return jsonify(username=g.user.username,
                   email=g.user.email,
                   id=g.user.id)

