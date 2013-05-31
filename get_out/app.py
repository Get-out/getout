from flask.ext import admin
from functools import wraps
import traceback
import logging
import flask
import json

from get_out import interaction

log = logging.getLogger("get-out-app")

def jsonified(func):
	'''
		Decorator to use a function to return a JSON response

		If return of the function has 'error' in it set to a truthy value
		Then the status_code will be 500

		If calling the function raises an exception, then we return 500 with {error}

		If calling the function raises an exception and the exception has
		a status_code attribute, then that is the status_code of the response
	'''
	@wraps(func)
	def wrapped(*args, **kwargs):
		code = None
		try:
			result = func(*args, **kwargs)
		except Exception as error:
			if hasattr(error, 'status_code'):
				code = error.status_code
			result = {'traceback':traceback.format_exc(), 'error_message':"{}: {}".format(error.__class__.__name__, error)}
			log.exception('An exception occurred')

		if isinstance(result, flask.Response):
			return result

		if not code:
			code = 200
			if 'error_message' in result and result['error_message']:
				code = 500

		dumped = json.dumps(result, indent=None if flask.request.is_xhr else 2)
		return flask.current_app.response_class(dumped, code, mimetype="application/json")
	flask.jsonify
	return wrapped

class IndexView(admin.AdminIndexView):
	@admin.expose('/')
	def index(self):
		return self.render('index.html')

def make_app(debug=False):
	'''Create our Flask app'''
	app = flask.Flask(__name__, static_url_path='/assets')

	index_view = IndexView(name='Home', url='/')
	app_admin = admin.Admin(app, name='Get Out!', index_view=index_view)

	app.route('/lolz')(jsonified(interaction.lolz))

	@app.before_request
	def before_request():
		flask.g.debug = debug

	return app

