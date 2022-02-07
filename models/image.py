from db import db


class ImageModel(db.Model):
    __tablename__ = "image"
    
    imageId = db.Column(db.Integer, primary_key=True)
    relationId = db.Column(db.Integer)
    imageType = db.Column(db.String(16))
    url = db.Column(db.String(64))
    imgIndex = db.Column(db.Integer)
    # imageData = db.Column(db.Text, unique=True, nullable=False)