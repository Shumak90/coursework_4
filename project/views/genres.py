from flask import request
from flask_restx import Resource, Namespace, abort

from project.exceptions import ItemNotFound
from project.container import genre_service
from project.dao.models import GenreSchema


genre_ns = Namespace('genres', description='Views for genres')
genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()


@genre_ns.route('/')
class GenresViews(Resource):
    @genre_ns.doc(description='Get genres', params={'page': 'Page number'})
    @genre_ns.response(200, 'Success')
    @genre_ns.response(404, 'Not found')
    def get(self):

        page = request.args.get('page', type=int)

        # Get results
        try:
            genres_found = genre_service.get_all(page)
            return genres_schema.dump(genres_found), 200
        except ItemNotFound:
            abort(404, message=f'Page {page} not found')


@genre_ns.route('/<int:uid>/')
class GenreView(Resource):
    @genre_ns.doc(description='Get genre by id')
    @genre_ns.response(200, 'Success')
    @genre_ns.response(404, 'Not found')
    def get(self, uid):
        try:
            genre = genre_service.get_one(uid)
            return genre_schema.dump(genre), 200
        except ItemNotFound:
            abort(404, f'Genre with id={uid} not found')
