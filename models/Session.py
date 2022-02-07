import json
from datetime import datetime
import pandas as pd
from flask import jsonify
from sqlalchemy import DateTime, CLOB

from db import db


class SessionModel(db.Model):
    __tablename__ = "session"

    sessionId = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'))
    # reservationId = db.Column(db.Integer)
    # contentId = db.Column(db.Integer)
    # domeId = db.Column(db.Integer)
    starttime = db.Column(db.DateTime, default=datetime.utcnow())
    endtime = db.Column(db.DateTime, default=datetime.utcnow())
    completed = db.Column(db.Boolean, default=False, nullable=False)
    interrupts = db.Column(db.Integer)
    domeRating = db.Column(db.Integer)
    domeFeedback = db.Column(CLOB)
    contentRating = db.Column(db.Integer)
    contentFeedback = db.Column(CLOB)

    @classmethod
    def find_by_id(cls, id: int):
        return cls.query.filter_by(userid=id).all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def serialize(cls, g):
        return {
            "date": g.starttime
        }

    @classmethod
    def get_date(cls, o1):
        df = pd.DataFrame({'full_date': pd.date_range(o1.starttime, periods=1)})
        df['date'] = df['full_date'].dt.date
        print(df['date'])
        return df['date']

    @classmethod
    def get_time(cls, o1):
        df = pd.DataFrame({'full_date': pd.date_range(o1.starttime, periods=1)})
        df['time'] = df['full_date'].dt.time
        print(df['time'])
        return df['time']