# import json

from flask import jsonify
from flask_restful import Resource, reqparse
# import pandas as pd
from marshmallow import ValidationError

from models.Session import SessionModel
from models.user import UserModel

parser = reqparse.RequestParser()


class Session(Resource):
    parser.add_argument('userid', type=int)
    # parser.add_argument('reservationId', type=int)
    # parser.add_argument('contentId', type=int)
    # parser.add_argument('domeId', type=int)
    parser.add_argument('completed', type=bool)
    parser.add_argument('interrupts', type=int)
    parser.add_argument('domeRating', type=int)
    parser.add_argument('domeFeedback', type=str)
    parser.add_argument('contentRating', type=int)
    parser.add_argument('contentFeedback', type=str)

    def post(self):
        try:
            args = parser.parse_args()
        except ValidationError as err:
            return err.messages, 400

        if UserModel.find_by_id(args['userid']):
            session = SessionModel(**args)
            session.save_to_db()

    def get(self):
        args = parser.parse_args()
        ls=[]
        if UserModel.find_by_id(args['userid']):
            # print(args['userid'])
            # print(SessionModel.find_by_id(args['userid']))
            # session_history = [x for x in SessionModel.find_by_id(args['userid'])]
            session_history = SessionModel.find_by_id(args['userid'])
            for i in session_history:
                ls.append(SessionModel.serialize(i))
            return jsonify({"data": ls})
            # return session_history

        # df['time'] = df['full_date'].dt.time





#         "username" : g.username,
#         "firstName" : g.firstName,
#         "lastName" : g.lastName,
#         "password" : g.password,
#         "email" : g.email
#     }

