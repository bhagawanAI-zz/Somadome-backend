from db import db

class DeviceModel(db.Model):
    __tablename__ ='devices'
    deviceid = db.Column(db.Integer, primary_key=True)
    devname =db.Column(db.String(20))
    currentstatus = db.Column(db.Boolean, default=True, nullable=False)
    # totaltime = db.Column(db.String(80), nullable=False)


    @classmethod
    def find_by_devname(cls, _username: str):
        return cls.query.filter_by(devname=_username).first()

    def json_data(self):
        return {
            "devname": self.devname,
        }

    def json(self):
        if self.currentstatus is True:
            return {
                "status" : "ON"
            }
        else:
            return {
                "status":"OFF"
            }

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()