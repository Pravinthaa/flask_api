from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
api = Api(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"User(name = {self.name}"

    
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String
}


class Users(Resource):
    @marshal_with(resource_fields)
    def get(self):
        users = UserModel.query.all()
        return users
    
    @marshal_with(resource_fields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args["name"])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users,201
    
class User(Resource):
    @marshal_with(resource_fields)
    def get(self,id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404,"User not found")
        return user
    
    @marshal_with(resource_fields)
    def patch(self,id):
        args = user_args.parse_args()
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404,"User not found")
        user.name = args["name"]
        db.session.commit()
        return user
    
    @marshal_with(resource_fields)
    def delete(self,id):
        user = UserModel.query.filter_by(id=id).first()
        if not user:
            abort(404,"User not found")
        db.session.delete(user)
        db.session.commit()
        users = UserModel.query.all()
        return users
    
 
    

api.add_resource(Users,'/api/users/')
api.add_resource(User,'/api/users/<int:id>')


@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'

@app.route('/add')
def add_user():
    mock_user = UserModel(name="Prav")
    db.session.add(mock_user)
    db.session.commit()
    return jsonify({"message": "successssssssssss"})

if __name__ == '__main__':
    app.run(debug=True)
