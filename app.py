import base64
import os
from flask import Flask, jsonify, request
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from werkzeug.utils import secure_filename
from automate_methods import create_presigned_url
from blacklist import BLACKLIST
from db import db
from ma import ma
from models.image import Img


app = Flask(__name__)
db.init_app(app)
ma.init_app(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "support@smarttrak.co"
app.config['MAIL_PASSWORD'] = base64.b64decode("TXVtbXNAMTk5NQ==").decode("utf-8")
uri = os.getenv("DATABASE_URL", 'sqlite:///data.db')  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklist feature
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # allow blacklisting for access and refresh tokens
app.secret_key = "somadome"  # could do app.config['JWT_SECRET_KEY'] if we prefer
mail = Mail(app)

from resources.routes import initialize_routes
api = Api(app)
jwt = JWTManager(app)


# @app.before_first_request
# def create_tables():
#     db.create_all()


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_headers, jwt_payload):
    return jwt_payload['jti'] in BLACKLIST


@jwt.revoked_token_loader
def revoked_token_callback(jwt_headers, jwt_payload):
    return jsonify({
        'description': 'the token has been revoked.',
        'error': 'token revoked'
    }), 401


# @app.route('/upload', methods=['POST'])
# def upload():
#     entityType = request.args.get('entityType')
#     entityId = request.args.get('entityId')
#     replace = bool(request.args.get('replace'))
#     index = request.args.get('index')
#     imageData = request.files['imageData']
#     if not imageData:
#         return 'No pic uploaded!', 400
#
#     filename = secure_filename(imageData.filename)
#     mimetype = imageData.mimetype
#     if not filename or not mimetype:
#         return 'Bad upload!', 400
#
#     img = Img(entityType=entityType, entityId=entityId, replace=replace, index=index, imageData=imageData.read())
#     db.session.add(img)
#     db.session.commit()
#
#     return 'Img Uploaded!', 200


@app.route("/music/", methods=['get'])
def musicis():
    musictype = request.args.get('musictype')
    objectname = musictype + ".mp3"
    return create_presigned_url('somadome-music', objectname)


@app.route("/device")
def deviceupdate():
    status = request.args.get('status')

initialize_routes(api)

# if __name__ == "__main__":
#     from db import db
#
#     db.init_app(app)
#     ma.init_app(app)
#     app.run(port=5000, debug=True)
