from sqlalchemy import create_engine, Column, Integer, String, Time, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///lksh_sport.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

session = Session()


class Participant(Base):
    __tablename__ = 'participant'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    is_captain = Column(Boolean)
    team_id = Column(Integer, ForeignKey('team.id'))
    sport_id = Column(Integer, ForeignKey('sport.id'))

    team = relationship('Team', back_populates='participants')

    def __repr__(self):
        return f'<Participant(name=\"{self.name}\")>'


class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True)
    captain_id = Column(Integer, ForeignKey('participant.id'))
    sport_id = Column(Integer, ForeignKey('sport.id'))
    name = Column(String)

    sport = relationship('Sport', back_populates='teams')
    participants = relationship(
        'Participant', order_by=Participant.id, back_populates='team')
    events_left = relationship('Event', back_populates='team1')
    events_right = relationship('Event', back_populates='team2')

    def __repr__(self):
        return f'<Team(name={self.name})>'


class Sport(Base):
    __tablename__ = 'sport'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    rules = Column(String)

    teams = relationship('Team', back_populates='sport')
    events = relationship('Event', back_populates='sport')

    def __repr__(self):
        return f'<Sport(name={self.name})>'


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    team1_id = Column(Integer, ForeignKey('team.id'))
    team2_id = Column(Integer, ForeignKey('team.id'))
    time = Column(Time)
    sport_id = Column(Integer, ForeignKey('sport.id'))
    place = Column(String)

    team1 = relationship(
        'Team',
        back_populates='events_left',
        foreign_keys=[team1_id]
    )
    team2 = relationship(
        'Team',
        back_populates='events_right',
        foreign_keys=[team2_id]
    )
