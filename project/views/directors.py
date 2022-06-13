from flask import request
from flask_restx import Resource, Namespace, abort

from project.exceptions import ItemNotFound
from project.container import director_service
from project.dao.models import DirectorSchema


director_ns = Namespace('directors', description='Views for directors')
directors_schema = DirectorSchema(many=True)
director_schema = DirectorSchema()


@director_ns.route('/')
class DirectorsViews(Resource):
    @director_ns.doc(description='Get directors', params={'page': 'Page number'})
    @director_ns.response(200, 'Success')
    @director_ns.response(404, 'Not found')
    def get(self):

        page = request.args.get('page', type=int)

        try:
            directors_found = director_service.get_all(page)
            return directors_schema.dump(directors_found), 200
        except ItemNotFound:
            abort(404, message=f'Page {page} not found')


@director_ns.route('/<int:uid>/')
class DirectorView(Resource):
    @director_ns.doc(description='Get director by id')
    @director_ns.response(200, 'Success')
    @director_ns.response(404, 'Not found')
    def get(self, uid):
        try:
            director = director_service.get_one(uid)
            return director_schema.dump(director), 200
        except ItemNotFound:
            abort(404, f'Director with id={uid} not found')
