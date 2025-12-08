from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Episode, Guest, Appearance

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)


class EpisodesResource(Resource):
    def get(self):
        episodes = Episode.query.all()
        return make_response(
            jsonify([episode.to_dict(rules=('-appearances',)) for episode in episodes]),
            200
        )


class EpisodeByIdResource(Resource):
    def get(self, id):
        episode = Episode.query.get(id)
        if not episode:
            return make_response(jsonify({"error": "Episode not found"}), 404)
        return make_response(jsonify(episode.to_dict()), 200)
    
    def delete(self, id):
        episode = Episode.query.get(id)
        if not episode:
            return make_response(jsonify({"error": "Episode not found"}), 404)
        db.session.delete(episode)
        db.session.commit()
        return make_response('', 204)


class GuestsResource(Resource):
    def get(self):
        guests = Guest.query.all()
        return make_response(
            jsonify([guest.to_dict(rules=('-appearances',)) for guest in guests]),
            200
        )


class AppearancesResource(Resource):
    def post(self):
        data = request.get_json()
        try:
            appearance = Appearance(
                rating=data.get('rating'),
                episode_id=data.get('episode_id'),
                guest_id=data.get('guest_id')
            )
            db.session.add(appearance)
            db.session.commit()
            return make_response(jsonify(appearance.to_dict()), 201)
        except ValueError as e:
            return make_response(jsonify({"errors": [str(e)]}), 400)
        except Exception:
            return make_response(jsonify({"errors": ["Validation errors"]}), 400)


api.add_resource(EpisodesResource, '/episodes')
api.add_resource(EpisodeByIdResource, '/episodes/<int:id>')
api.add_resource(GuestsResource, '/guests')
api.add_resource(AppearancesResource, '/appearances')


@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Podcast API"})


if __name__ == '__main__':
    app.run(port=5555, debug=True)
