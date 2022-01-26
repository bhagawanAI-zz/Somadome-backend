
from flask_restful import reqparse,Resource
from marshmallow import ValidationError

from models.devicemodel import DeviceModel

parser = reqparse.RequestParser()

class DeviceRegister(Resource):
    parser.add_argument('devname', type=str)

    def post(self):
        try:
            # root_args = root_parser.parse_args()
            args = parser.parse_args()
        except ValidationError as err:
            return err.messages, 400
        if DeviceModel.find_by_devname(args['devname']):
            return {"message": "Device already registered"}, 400

        device = DeviceModel(**args)
        device.save_to_db()

        return device.json_data(), 201

class DeviceStatus(Resource):
    parser.add_argument('devname', type=str)
    def get(self):
        args = parser.parse_args()
        device = DeviceModel.find_by_devname(args['devname'])
        if not device:
            return {"message": "Device not registered"}, 404

        return device.json(), 200

