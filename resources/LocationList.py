from flask import jsonify
from flask_restful import Resource

from models.LocationList import LocationListModel


class LocationList(Resource):

    def get(self):
        locls = LocationListModel.query.all()
        return jsonify([i.serialize for i in locls])
