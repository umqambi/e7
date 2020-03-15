from flask import Flask
from flask_mongoengine import MongoEngine
import os

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "my_bulletin"}
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY') or "Thi5_i5_my_5ecret_k33p_it_5afe"

db = MongoEngine(app)

def register_blueprints(app):
    # Prevents circular imports
    from bulletin.routes import adverts
    app.register_blueprint(adverts)

register_blueprints(app)

if __name__ == '__main__':
    app.run()