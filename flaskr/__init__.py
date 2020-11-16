import os

from flask import (Flask, send_from_directory)

def create_app(test_config=None):
  # create and configura the app
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
  )

  if test_config is None:
    # laod the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=True)
  else:
    # load the test config if passed in
    app.config.from_mapping(test_config)

  # ensure the isntance folder exists
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass

  from . import db
  db.init_app(app)

  from . import auth
  app.register_blueprint(auth.bp)

  from . import blog
  app.register_blueprint(blog.bp)
  app.add_url_rule('/', endpoint='index')

  from . import uploads
  app.register_blueprint(uploads.bp)

  @app.route('/hello')
  def hello():
    return 'Hello, World!'

  return app
