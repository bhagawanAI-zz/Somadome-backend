from db import db


class LocationListModel(db.Model):
    __tablename__ = "locationlist"

    id = db.Column(db.Integer, primary_key=True)
    businessName = db.Column(db.String(225))
    businessAddress = db.Column(db.String(225))
    website = db.Column(db.String(128))
    phoneNumber = db.Column(db.String(20))
    bookingLink = db.Column(db.String(225))
    photoLink = db.Column(db.String(500))
    comments = db.Column(db.String(225), default =None)
    latitude = db.Column(db.String(20))
    longitude = db.Column(db.String(20))

    @property
    def serialize(self):
        return {
            "id": self.id,
            "businessName": self.businessName,
            "businessAddress": self.businessAddress,
            "website": self.website,
            "phoneNumber": self.phoneNumber,
            "bookingLink": self.bookingLink,
            "photoLink": self.photoLink,
            "comments": self.comments,
            "latitude": self.latitude,
            "longitude": self.longitude
        }