from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'timekeeping.db')
db = SQLAlchemy(app)
ma = Marshmallow(app)


@app.route("/")
def hello():
    return "Hello World!!!"

class costcentre(db.Model):
    code = db.Column(db.String(20), primary_key = True, unique = True )
    description = db.Column(db.String(100))
    parentcode = db.Column(db.String(20))
    headeronly = db.Column(db.Integer)

    def __init__(self, code, description, parentcode, headeronly):
        self.code = code
        self.description = description
        self.parentcode = parentcode
        self.headeronly = headeronly

    def toJson(self):
        return {
            "code" : self.code,
            "description" : self.description,
            "parentcode" : self.parentcode,
            "headeronly" : self.headeronly
        }

class costcentreschema(ma.Schema):
    class Meta:
        #fields to expose
        fields = ('code','description', 'parentcode', 'headeronly')

costcentre_schema = costcentreschema()
costcentres_schema = costcentreschema(many=True)

#endpoint to create new cost centre
@app.route("/api/costcentre", methods=['POST'])        
def add_costcentre():
    code = request.json['code']
    description = request.json['description']
    if request.json['parentcode'] != None :
        parentcode = request.json['parentcode']
    headeronly = request.json['headeronly']

    new_costcentre = costcentre(code, description, parentcode, headeronly)

    db.session.add(new_costcentre)
    db.session.commit()

    return  jsonify(new_costcentre.toJson()) 

#endpoint to update cost centre
@app.route("/api/costcentre/<id>", methods=['PUT'])
def update_costcentre(id):
    lcostCentre = costcentre.query.get(id)

    description = request.json['description']
    parentcode = request.json['parentcode']
    headeronly = request.json['headeronly']

    lcostCentre.description = description
    lcostCentre.parentcode = parentcode
    lcostCentre.headeronly = headeronly

    db.session.commit()
    return costcentre_schema.jsonify(lcostCentre)

#endpoint to show all cost centres
@app.route("/api/costcentre", methods=['GET'])
def get_costcentre():
    all_costcentres = costcentre.query.all()
    result = costcentres_schema.dump(all_costcentres)
    return jsonify(result.data)

#endpoint to get cost centre detail
@app.route("/api/costcentre/<id>", methods=['GET'])
def costcentre_detail(id):
    #lcostCentre = costcentre.query.get(id)
    lcostCentre = costcentre.query.filter(costcentre.code.ilike(id)).first()
    return costcentre_schema.jsonify(lcostCentre)

#endpoint to delete cost centre
@app.route("/api/costcentre/<id>", methods=['DELETE'])
def delete_costcentre(id):
    lcostCentre = costcentre.query.get(id)
    db.session.delete(lcostCentre)
    db.session.commit()

    return costcentre_schema.jsonify(lcostCentre)


if __name__ == '__main__':
    app.run(debug=True)