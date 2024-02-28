from flask import Blueprint, jsonify
from flask.views import MethodView
from app.models.persons import Persons
from app import db
from schemas import ParentSchema, ParentsSchema
from flask_smorest import Blueprint

blp = Blueprint('api', __name__)

@blp.route('/humans')
class PeopleAPI(MethodView):
    @blp.response(200, ParentsSchema)
    def get(self):
        persons = Persons.query.all()
        # Serialize the data using the schema
        serialized_data = ParentsSchema(many=True).dump(persons)
        return jsonify(serialized_data)

    @blp.arguments(ParentSchema)
    @blp.response(201, ParentSchema)
    def post(self, data):
        new_person = Persons(name=data['name'], age=data['age'])
        db.session.add(new_person)
        db.session.commit()
        return new_person, 201

@blp.route('/humans/<int:person_id>')
class PersonAPI(MethodView):
    @blp.response(200, ParentSchema)
    def get(self, person_id):
        person = Persons.query.get(person_id)
        if person:
            return person
        return {"message": "person not found"}, 404

    @blp.arguments(ParentSchema)
    @blp.response(200, ParentSchema)
    def put(self, data, person_id):
        person = Persons.query.get(person_id)
        if person:
            person.name = data['name']
            person.age = data['age']
            db.session.commit()
            return person
        return {"message": "person not found"}, 404

    @blp.response(200, ParentSchema)
    def delete(self, person_id):
        person = Persons.query.get(person_id)
        if person:
            db.session.delete(person)
            db.session.commit()
            return {"message": "Person deleted successfully"}, 200
        return {"message": "person not found"}, 404
