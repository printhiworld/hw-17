# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)
movie_ns = api.namespace('movies')
genre_ns = api.namespace('genres')
director_ns = api.namespace('directors')

class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))



class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()

class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))



class GenrerSchema(Schema):
    id = fields.Int()
    name = fields.Str()

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

genrere_schema = GenrerSchema()
genreres_schema = GenrerSchema(many=True)

@movie_ns.route('/')
class MoviesViews(Resource):
    def get(self):
        movies = Movie.query

        if genre_id:=request.args.get('genre_id'):
            movies = movies.filter(Movie.genre_id==genre_id)
        if director_id := request.args.get('director_id'):
            movies = movies.filter(Movie.director_id == director_id)
        return movies_schema.dump(movies.all())



@movie_ns.route('/<int:pk>')
class MoviesView(Resource):
    def get(self, pk):

        movie = Movie.query.get(pk)
        return movie_schema.dump(movie)



if __name__ == '__main__':
    app.run(debug=True)
