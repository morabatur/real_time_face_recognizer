from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://py:py@127.0.0.1:1436/db_py?driver=SQL+Server+Native+Client+11.0'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init
db = SQLAlchemy(app)

# init ma
ma = Marshmallow(app)


class Camera(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def __init__(self, id, name):
        self.id = id
        self.name = name


class CameraSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')


camera_schema = CameraSchema()
cameras_schema = CameraSchema(many=True)


@app.route('/product', methods=['POST'])
def add_prod():
    id = request.json['id']
    name = request.json['name']

    new_camera = Camera(id, name)
    db.session.add(new_camera)
    db.session.commit()

    return camera_schema.jsonify(new_camera)


@app.route('/product', methods=['GET'])
def get_prod():
    all_prod = Camera.query.all()
    result = cameras_schema.dump(all_prod)
    return jsonify(result)




if __name__ == '__main__':
    app.run(debug=True)
