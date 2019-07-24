from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_jsonpify import jsonify
from flask_cors import CORS
from json import dumps
from datetime import datetime
from hashlib import md5
from os import urandom
import bot
import config as cfg
import threading

# Initialize flask app and api
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lksh_sport.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)
CORS(app)


class Participant(db.Model):
    __tablename__ = 'participant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    is_captain = db.Column(db.Boolean)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    team = db.relationship('Team', back_populates='participants')

    def __repr__(self):
        return f'<Participant(name=\"{self.name}\")>'


class Team(db.Model):
    __tablename__ = 'team'

    id = db.Column(db.Integer, primary_key=True)
    sport_id = db.Column(db.Integer, db.ForeignKey('sport.id'))
    name = db.Column(db.String)

    sport = db.relationship('Sport', back_populates='teams')
    participants = db.relationship(
        'Participant', order_by=Participant.id, back_populates='team')

    def __repr__(self):
        return f'<Team(name={self.name})>'


class Sport(db.Model):
    __tablename__ = 'sport'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    rules = db.Column(db.String)

    teams = db.relationship('Team', back_populates='sport')
    events = db.relationship('Event', back_populates='sport')

    def __repr__(self):
        return f'<Sport(name={self.name})>'


class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    team1_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    team2_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    time = db.Column(db.Time)
    sport_id = db.Column(db.Integer, db.ForeignKey('sport.id'))
    place = db.Column(db.String)

    team1 = db.relationship(
        'Team',
        foreign_keys=[team1_id]
    )
    team2 = db.relationship(
        'Team',
        foreign_keys=[team2_id]
    )
    sport = db.relationship('Sport', back_populates='events')


# classes responsible for request handling

class RegisterTeam(Resource):
    def post(self):
        args = reg_parser.parse_args()
        args['sport'] = cfg.sports[args['sports-type']]
        bot.approve_registration(args)
        return jsonify(
            {
                'message':
                'Your application is resieved and will soon be reviewed'
            }
        )


class Events(Resource):
    def get(self):
        return jsonify({'fuck': 'sirgay'})


class Approve(Resource):
    def post(self):
        pass


db.create_all()
reg_parser = reqparse.RequestParser()
reg_parser.add_argument('sports-type')
reg_parser.add_argument('team-name')
reg_parser.add_argument('participant')
reg_parser.add_argument('no-team')
for i in range(8):
    reg_parser.add_argument(f'participant-{i+1}')

aprv_parser = reqparse.RequestParser()
aprv_parser.add_argument('token')

api.add_resource(RegisterTeam, '/api/register_team')
api.add_resource(Events, '/api/events')
api.add_resource(Approve, '/api/admin/approve_registration')

if __name__ == '__main__':
    flask_thread = threading.Thread(
        target=app.run, kwargs={
            'debug': False,
            'use_reloader': False,
            'port': 42069
        }
    )
    flask_thread.start()
    bot.init()
