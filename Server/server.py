from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
# from json import dumps
# from flask_jsonpify import jsonify
# from datetime import datetime
# from hashlib import md5
# from os import urandom

# Initialize flask app and api
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lksh_sport.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)


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
