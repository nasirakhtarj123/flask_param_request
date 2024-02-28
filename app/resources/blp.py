from flask import Blueprint, jsonify, request
from flask.views import MethodView
from app.models.persons import Persons
from app import db
from schemas import ParentSchema, ParentsSchema
from flask_smorest import Blueprint

blp = Blueprint('api', __name__)

@blp.route('/humans')
class PeopleAPI(MethodView):

    @blp.response(200, ParentsSchema(many=True))
    def get(self):
        age = request.args.get('age')
        name = request.args.get('name')
        person_id = request.args.get('id')
        query_filter = {}
        if age:
            query_filter['age'] = age
        if name:
            query_filter['name'] = name
        if person_id:
            query_filter['id'] = person_id
        persons = Persons.query.filter_by(**query_filter).all()
        result = [{'id': person.id, 'name': person.name, 'age': person.age} for person in persons]
        return jsonify(result)

    @blp.response(201, ParentSchema)
    def post(self):
        name = request.args.get('name')
        age = request.args.get('age')
        if not name or not age:
            return jsonify({"message": "Name and age are required parameters"}), 400
        new_person = Persons(name=name, age=age)
        db.session.add(new_person)
        db.session.commit()
        result = {'id': new_person.id, 'name': new_person.name, 'age': new_person.age}
        return jsonify(result), 201

@blp.route('/humans', methods=['PUT', 'DELETE'])
class PersonAPI(MethodView):

    @blp.response(200, ParentSchema)
    def put(self):
        try:
            person_id = request.args.get('id')
            name = request.args.get('name')
            age = request.args.get('age')
            if person_id is None:
                return jsonify({"message": "Person ID is required"}), 400
            person = Persons.query.get_or_404(person_id)
            if name:
                person.name = name
            if age:
                person.age = age
            db.session.commit()
            updated_person = {'id': person.id, 'name': person.name, 'age': person.age}
            return jsonify(updated_person), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": str(e)}), 500

    @blp.response(200)
    def delete(self):
        try:
            person_id = request.args.get('id')
            if person_id is None:
                return jsonify({"message": "Person ID is required"}), 400
            person = Persons.query.get_or_404(person_id)
            db.session.delete(person)
            db.session.commit()
            return jsonify({"message": "Person deleted successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": str(e)}), 500
