from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_jsonpify import jsonify
from flask_cors import CORS
from json import dumps, loads
from datetime import datetime
from hashlib import md5
import bot
import config as cfg
import threading
import logging

# Initialize flask app and api
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lksh_sport.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)
CORS(app)

# Initialize registering dict
applications = {}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

<<<<<<< HEAD
jsonfile = open('participants.json', 'r')
participants = loads(jsonfile.read(), encoding='utf-8')
=======
jsonfile = open('participants.json', 'r').read()
participants = loads(jsonfile, encoding='utf-8')
>>>>>>> 2ac618d3553a7ba14307e6e69129a082e41d3bb8
groups = {}
teachers = []

for p in participants:
    if p['is_teacher']:
        teachers.append(p)
    groups[p['name']] = p['group']


# Classes responsible for db work


class Participant(db.Model):
    __tablename__ = 'participant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    is_captain = db.Column(db.Boolean)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    sport_id = db.Column(db.Integer, db.ForeignKey('sport.id'))

    team = db.relationship('Team', back_populates='participants')
    sport = db.relationship('Sport', back_populates='participants')

    def __repr__(self):
        return f'<Participant(name=\"{self.name}\")>'

    def toDict(self):
        return {
            'name': self.name,
            'team': self.team.name
        }


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
    participants = db.relationship('Participant', back_populates='sport')

    def __repr__(self):
        return f'<Sport(name={self.name})>'


class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    team1_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    team2_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    time = db.Column(db.DateTime)
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

    def toDict(self):
        return {
            'name': self.name,
            'time': self.time,
            'team1': self.team1.name,
            'team2': self.team2.name,
            'sport': self.sport.name,
            'place': self.place
        }


# classes responsible for request handling

def existsParticipant(name, sport_id):
    return Participant.query.filter_by(
        name=name,
        sport_id=sport_id
    ).first() is not None


def existsTeam(name, sport_id):
    return Team.query.filter_by(
        name=name,
        sport_id=sport_id
    ).first() is not None


class RegisterTeam(Resource):
    def post(self):
        args = reg_parser.parse_args()
        args['sport'] = cfg.sports[args['sports-type']]
        args['hash'] = md5(str(args).encode('utf-8')).hexdigest()
        applications[args['hash']] = args
        sport = Sport.query.filter_by(name=args['sport']).first()
        if args['no-team']:
            part_name = args['participant'] + groups[args['participant']]
            if existsParticipant(part_name, sport.id):
                return 'There is already a participant with the same name '
                'registered for this sport'
            else:
                bot.requestApproval(args)
        else:
            if Team.query.filter_by(name=args['team-name']).first() is not None:
                return jsonify(
                    {
                        'message':
                        'There is already a registered team with that name'
                    }
                )
            illegal_participants = []
            i = 1
            part_name = f'participant-{i}'

            while args.get(part_name, '') != '':
                if existsParticipant(
                        args[part_name] + groups[args[part_name]],
                        sport.id):
                    illegal_participants.append(args[part_name])
                i += 1
                part_name = f'participant-{i}'

            if len(illegal_participants) > 0:
                response = 'These people are already registered '
                response += 'for this sport in another team(s):<br/>'
                response += '<br/>'.join(illegal_participants)
                return response
            else:
                bot.requestApproval(args)

        return jsonify(
            {
                'message':
                'Your application is received and will soon be reviewed'
            }
        )


class Events(Resource):
    def get(self):
        events = [x.toDict() for x in Event.query.all()]
        return jsonify(events)


class Participants(Resource):
    def get(self):
        args = part_parser.parse_args()
        participants = Participant.query.filter_by(
            sport_id=Sport.query.filter_by(name=cfg.sports[args['sport']]).first().id)
        return jsonify([x.toDict() for x in participants])


class Approve(Resource):
    def post(self):
        token = aprv_parser.parse_args()['token']
        args = applications[token]
        sport = Sport.query.filter_by(name=args['sport']).first()
        if args['no-team'] is not None or args['sport'] in cfg.solo_sports:
            p = Participant(
                name=args['participant'],
                team_id=69420,
                sport_id=sport.id
            )
            db.session.add(p)
            db.session.commit()
        else:
            participants = []
            t = Team(name=args['team-name'], sport_id=sport.id)
            db.session.add(t)
            db.session.commit()
            i = 1
            while args.get(f'participant-{i}', '') != '':
                p = Participant(
                    name=args[f'participant-{i}'],
                    sport_id=sport.id,
                    team_id=t.id
                )
                participants.append(p)
                i += 1
                part_name = args[f'participant-{i}']
            db.session.add_all(participants)
            db.session.commit()
        bot.success(args['hash'], 'подтверждена')


class Shutdown(Resource):
    def post(self):
        token = aprv_parser.parse_args()['token']
        if token == 'denislox':
            exit()


db.create_all()

for sport in cfg.sports.values():
    if Sport.query.filter_by(name=sport).first() is None:
        sp = Sport(name=sport)
        db.session.add(sp)
<<<<<<< HEAD
        db.session.commit()
=======
>>>>>>> 2ac618d3553a7ba14307e6e69129a082e41d3bb8
    db.session.commit()

reg_parser = reqparse.RequestParser()
reg_parser.add_argument('sports-type')
reg_parser.add_argument('team-name')
reg_parser.add_argument('participant')
reg_parser.add_argument('no-team')
for i in range(8):
    reg_parser.add_argument(f'participant-{i+1}')

aprv_parser = reqparse.RequestParser()
aprv_parser.add_argument('token')

part_parser = reqparse.RequestParser()
part_parser.add_argument('sport')

api.add_resource(RegisterTeam, '/api/register_team')
api.add_resource(Events, '/api/events')
api.add_resource(Participants, '/api/participants')
api.add_resource(Approve, '/api/admin/approve_registration')

if __name__ == '__main__':
    flask_thread = threading.Thread(
        target=app.run, kwargs={
            'debug': False,
            'use_reloader': False,
            'port': 42069,
            'host': '0.0.0.0'
        }
    )
    flask_thread.start()
    bot.init()
