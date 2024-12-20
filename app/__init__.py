from flask import Flask
from .models import db
from flask_migrate import Migrate

migrate = Migrate()

def create_app(config_class='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app,db)

    with app.app_context():
        from .routes import bp as routes_bp
        app.register_blueprint(routes_bp)
        db.create_all()
        

    return app
