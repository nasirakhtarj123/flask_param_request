from flask import Blueprint, jsonify, request
from flask.views import MethodView
from app.models.persons import Persons
from app import db
from schemas import PersonSchema

blp = Blueprint('api', __name__)

@blp.route('/humans', methods=['GET', 'POST'])
def get_people():
    if request.method == 'GET':
        return PeopleAPI.get()
    elif request.method == 'POST':
        return PeopleAPI.post()

class PeopleAPI(MethodView):
    @staticmethod
    def get():
        persons = Persons.query.all()
        persons_schema = PersonSchema(many=True)  # Instantiate schema here
        result = persons_schema.dump(persons)
        return jsonify(result)

    @staticmethod
    def post():
        data = request.json
        person_schema = PersonSchema()  # Instantiate schema here
        errors = person_schema.validate(data)
        if errors:
            return jsonify(errors), 400
        new_person = Persons(name=data['name'], age=data['age'])
        db.session.add(new_person)
        db.session.commit()
        result = person_schema.dump(new_person)
        return jsonify(result), 201
    
@blp.route('/humans/<int:person_id>', methods=['GET', 'PUT', 'DELETE'])
def get_put_delete_person(person_id):
    return PersonAPI.as_view('person_api')(person_id)

class PersonAPI(MethodView):
    def get(self, person_id):
        person = Persons.query.get(person_id)
        if person:
            person_schema = PersonSchema()  
            result = person_schema.dump(person)
            return jsonify(result)
        return jsonify({"message": "person not found"}), 404

    def put(self, person_id):
        person = Persons.query.get(person_id)
        if person:
            data = request.json
            person_schema = PersonSchema()  
            errors = person_schema.validate(data)
            if errors:
                return jsonify(errors), 400
            person.name = data['name']
            person.age = data['age']
            db.session.commit()
            result = person_schema.dump(person)
            return jsonify(result)
        return jsonify({"message": "person not found"}), 404

    def delete(self, person_id):
        person = Persons.query.get(person_id)
        if person:
            db.session.delete(person)
            db.session.commit()
            return jsonify({"message": "Person deleted successfully"}), 200
        return jsonify({"message": "person not found"}), 404
