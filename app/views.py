__author__ = 'Madison'

from app import app
# from app.http_access import crossdomain
from flask import jsonify
from app.generic_error import GenericError
from flask import render_template

# @crossdomain(origin='*')  # this can probably get scrapped
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
    # return app.send_static_file('index.html')
    # return "Index is working"


@app.errorhandler(GenericError)
def handle_generic_error(error):
    return jsonify({'success': False, 'response': error.message})


#
#
# this CORS junk can probably be scrapped.
@app.after_request
def after(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods',
                         'POST, GET, PUT, PATCH, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, X-Requested-With')
    response.headers.add('Access-Control-Max-Age', '1728000')

    return response
