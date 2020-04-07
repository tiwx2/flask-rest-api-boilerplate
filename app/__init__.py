from flask import Flask

from log import debug_logger
import config

import os

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=config.Config):
	flask_env = os.getenv('FLASK_ENV')
	
	app = Flask(__name__)
	
	#overrides the configuration when FLASK_ENV environment variable is set to development
	if flask_env == 'development':
		app.config.from_object(config.DevelopmentConfig)
		debug_logger.info('Development configuration loaded')
	else:
		app.config.from_object(config_class)

	db.init_app(app)
	migrate.init_app(app, db)

	debug_logger.info("database url: {}".format(app.config['SQLALCHEMY_DATABASE_URI']))

	from app.main import bp as main_bp
	app.register_blueprint(main_bp)
	from app.api import bp as api_bp
	app.register_blueprint(api_bp, url_prefix='/api')
	
	return app

from app import models