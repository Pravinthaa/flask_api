from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"User(name = {self.name}"

    

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
