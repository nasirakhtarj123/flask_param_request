from flask import Blueprint, jsonify, request
from flask.views import MethodView
from app.models.persons import Persons
from app import db

class PeopleAPI(MethodView):
    def get(self):
        persons = Persons.query.all()
        result = [{'id': person.id, 'name': person.name, 'age': person.age} for person in persons]
        return jsonify(result)

    def post(self):
        data = request.json
        new_person = Persons(name=data['name'], age=data['age'])
        db.session.add(new_person)
        db.session.commit()
        return jsonify({'id': new_person.id, 'name': new_person.name, 'age': new_person.age}), 201

class PersonAPI(MethodView):
    def get(self, person_id):
        person = Persons.query.get(person_id)
        if person:
            return jsonify({'id': person.id, 'name': person.name, 'age': person.age})
        return jsonify({"message": "person not found"}), 404

    def put(self, person_id):
        person = Persons.query.get(person_id)
        if person:
            data = request.json
            person.name = data['name']
            person.age = data['age']
            db.session.commit()
            return jsonify({'id': person.id, 'name': person.name, 'age': person.age})
        return jsonify({"message": "person not found"}), 404

    def delete(self, person_id):
        person = Persons.query.get(person_id)
        if person:
            db.session.delete(person)
            db.session.commit()
            return jsonify({"message": "Person deleted successfully"}), 200
        return jsonify({"message": "person not found"}), 404

# Create blueprint
blp = Blueprint('api', __name__)

# Register views with the blueprint
blp.add_url_rule('/humans', view_func=PeopleAPI.as_view('people_api'))
blp.add_url_rule('/humans/<int:person_id>', view_func=PersonAPI.as_view('person_api'))

