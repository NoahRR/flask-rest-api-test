from flask import Flask, request, jsonify
from flask_restful import Api, Resource, abort, reqparse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databaseF.db'

db = SQLAlchemy(app)

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer)
    birthday = db.Column(db.String(10))

    def __repr__(self):
        return f"Name: {self.name}"

database_data = reqparse.RequestParser()
database_data.add_argument('age', type=int, help="Please input an age", required=True)
database_data.add_argument('birthday', type=str, help="Please input a birthday", required=True)
database_data.add_argument('name', type=str, help="Please input a name", required=True)

something = reqparse.RequestParser()
something.add_argument('name', type=str, help="Please input a name", required=True)
something.add_argument('age', type=int, help="Please input a age", required=True)
something.add_argument('birthday', type=str, help="Please input a birthday", required=True)

data = {
    'Noah' : {'age': 20, 'birthday': '11/13/00'},
    'Camille' : {'age': 20, 'birthday': '11/13/00'},
    'G' : {'age': 14, 'birthday': 'may/30/06'},
    'Random Man' : {'age': 28, 'birthday': '02/02/92'},
}

def check_for_name_else_abort(name):
    if name not in data:
        abort(404, message="no such humanoid")

class HelloWorld(Resource):
    def get(self):
        return data

class ca(Resource):
    def get(self, name):
        check_for_name_else_abort(name)
        return data[name]

class modifier(Resource):
    def post(self):
        try:
            data[request.form.get('name')] = {'age': request.form.get('age'), 
                                              'birthday': request.form.get('birthday')}
        except:
            abort(409, message='Person already exists')

        args = something.parse_args()

        context = {
            'type': request.method,
            'name': request.form.get('name'),
            'age': request.form.get('age'),
            'birthday': request.form.get('birthday'),
            'FINALFORM DATA': data,
            'ARGS': args,
        }
        return context, 201

    def put(self):
        return {'this is': 'a put request'}

    def delete(self):
        args = something.parse_args()
        name = args['name']
        check_for_name_else_abort(name)
        del data[name]
        return {'humanoid deleted': name, 'info': args}


def is_there_such_a_person(iden):
    try:
        person = People.query.filter_by(id=iden).first()
        hi = person.name
    except:
        abort(404, message="No such person!")

class datastuff(Resource):

    # return specified person data
    def get(self, iden):

        is_there_such_a_person(iden)
        person_data = People.query.filter_by(id=iden).first()
        context = {
            'name': person_data.name,
            'age': person_data.age,
            'birthday': person_data.birthday,
        }

        return context

    def put(self, iden):

        args = database_data.parse_args()
        is_there_such_a_person(iden)

        person = People.query.filter_by(id=iden).first()
        person.name = args.name
        person.age = args.age
        person.birthday = args.birthday

        db.session.add(person)
        db.session.commit()

        return 'Modified user: ' + args.name

    def delete(self, iden):

        is_there_such_a_person(iden)

        person = People.query.filter_by(id=iden).first()
        name = person.name

        db.session.delete(person)
        db.session.commit()

        return 'Exterminated user: ' + name


class datastuff2(Resource):
    # create person
    def post(self):

        #  age = request.form['age']
        args = database_data.parse_args()
        person = People(name=args['name'], age=args['age'], birthday=args['birthday']) 

        db.session.add(person)
        db.session.commit()

        return 'Added new user: ' + args['name']

class datastuff3(Resource):

    # show all database contents
    def get(self):

        context = {}
        all_data = People().query.all()
        for pers in all_data:
            context[pers.id] = {
                'name': pers.name,
                'age': pers.age,
                'birthday': pers.birthday,
            }

        return context

# http://127.0.0.1:12345/all
api.add_resource(HelloWorld, "/all")
# http://127.0.0.1:12345/sp/Noah
api.add_resource(ca, "/sp/<string:name>")
# http://127.0.0.1:12345/mod
api.add_resource(modifier, "/mod")
# http://127.0.0.1:12345/database/Noah
api.add_resource(datastuff, "/database/<int:iden>")
# http://127.0.0.1:12345/database
api.add_resource(datastuff2, "/database")
# http://127.0.0.1:12345/database/showall
api.add_resource(datastuff3, "/database/showall")


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=12345)
