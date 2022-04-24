import json
from logging import exception

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Drink(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),unique=True)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f'{self.name}-{self.description}'


@app.route('/',methods=['GET','POST'])
@app.route("/index", methods=['GET', 'POST'])
def index(*args, **kwargs):
    data = request.get_json()
    name = request.args.get("name1", "")
    return f"I am {data.get.name1},{name}"


@app.route('/drinks')
def all_drinks():

    data = Drink.query.all()
    output = []
    for d in data:
        d_data = {"name":d.name,"desc":d.description}
        output.append(d_data)

    return {"output":output}


@app.route('/drink/<id>')
def get_drink(id):

    data = Drink.query.get(id)
    return jsonify({"desc":data.description, "name": data.name,})


@app.route('/add_drink', methods=['POST'])
def add_drink():
    data = request.get_json()
    d_1 = Drink(name=data.get("name"), description=data.get("description"))
    db.session.add(d_1)
    try:
        db.session.commit()
    except:
        return {"Output":f"Data failed to upload"}
    return {"Output":"Data ho gaya upload"}


@app.route('/update_drink/<id>',methods=['POST'])
def update_drink(id):
    data = request.get_json()
    new_name = data.get("new_name")
    new_desc = data.get("new_desc")
    old_data = Drink.query.get(id)
    old_data.name = new_name
    old_data.description = new_desc
    db.session.commit()

    return {"name":old_data.name,"desc":old_data.description}


@app.route("/Delete/<id>",methods=["DELETE"])
def delete(id):
    data = Drink.query.get(id)
    if data is None:
        return{"Error":"not found"}

    db.session.delete(data)
    db.session.commit()
    return {"Output": data.name}



