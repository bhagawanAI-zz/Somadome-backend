from db import db


class Music(db.Model):
    __tablename__ = "music"

    name = db.Column(db.String(15),primary_key=True)
    time = db.Column(db.Integer)

    @classmethod
    def find_by_name(cls, musicname: str):
        return cls.query.filter_by(name=musicname).first()