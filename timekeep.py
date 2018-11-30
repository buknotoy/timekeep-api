from flask import Flask, request, jsonify
#from flask_sqlalchemy import SQLAlchemy
#from flask_marshmallow import Marshmallow
from costcentre import costcentre
#import os

app = Flask(__name__)
#basedir = os.path.abspath(os.path.dirname(__file__))
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'timekeeping.db')
#db = SQLAlchemy(app)
#ma = Marshmallow(app)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)