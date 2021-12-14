from datetime import datetime
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp
from marshmallow import ValidationError
from blacklist import BLACKLIST
from models.user import UserModel

USER_ALREADY_EXISTS = "A user with that username already exists."
USER_EMAIL_EXISTS = "A user with this email already exists."
CREATED_SUCCESSFULLY = "User created successfully."
USER_NOT_FOUND = "User not found."
USER_DELETED = "User deleted."
INVALID_CREDENTIALS = "Invalid credentials!"
USER_LOGGED_OUT = "User <id={user_id}> successfully logged out."

root_parser = reqparse.RequestParser()
nested_one_parser = reqparse.RequestParser()
root_parser.add_argument('params', type=dict, required=True, help='this field cannot be blank')
root_parser.add_argument('jsonrpc', type=str, required=True, help='this field cannot be blank')
root_parser.add_argument('method', type=str, required=True, help='this field cannot be blank')
root_parser.add_argument('id', type=int, required=True, help='this field cannot be blank')
nested_one_parser.add_argument('username', type=str, location=('params',))
nested_one_parser.add_argument('password', type=str, location=('params',))
nested_one_parser.add_argument('email', type=str, location=('params',))
nested_one_parser.add_argument('pwResetRequired', type=bool, location=('params',))
nested_one_parser.add_argument('displayName', type=str, location=('params',))
nested_one_parser.add_argument('headline', type=str, location=('params',))
nested_one_parser.add_argument('firstName', type=str, location=('params',))
nested_one_parser.add_argument('middleInitial', type=str, location=('params',))
nested_one_parser.add_argument('lastName', type=str, location=('params',))
nested_one_parser.add_argument('suffix', type=str, location=('params',))
nested_one_parser.add_argument('phone', type=str, location=('params',))
nested_one_parser.add_argument('address1', type=str, location=('params',))
nested_one_parser.add_argument('address2', type=str, location=('params',))
nested_one_parser.add_argument('city', type=str, location=('params',))
nested_one_parser.add_argument('state', type=str, location=('params',))
nested_one_parser.add_argument('zip', type=int, location=('params',))
nested_one_parser.add_argument('birthDate', type=lambda x: datetime.strptime(x, '%B %d, %Y'), location=('params',))


class UserRegister(Resource):

    def post(self):
        try:
            root_args = root_parser.parse_args()
            nested_one_args = nested_one_parser.parse_args(req=root_args)

        except ValidationError as err:
            return err.messages, 400

        if UserModel.find_by_username(nested_one_args['username']):
            return {"message": USER_ALREADY_EXISTS}, 400

        if UserModel.find_by_email(nested_one_args['email']):
            return {"message": USER_EMAIL_EXISTS}, 400

        user = UserModel(**nested_one_args)
        user.save_to_db()

        return user.json_data(root_args['id']), 201


class User(Resource):
    @classmethod
    # @jwt_required()
    def get(cls, user_name: str):
        user = UserModel.find_by_username(user_name)
        if not user:
            return {"message": USER_NOT_FOUND}, 404

        return user.json(), 200

    @classmethod
    def delete(cls, user_name: str):
        user = UserModel.find_by_username(user_name)
        if not user:
            return {"message": USER_NOT_FOUND}, 404

        user.delete_from_db()
        return {"message": USER_DELETED}, 200


class UserLogin(Resource):

    @classmethod
    def post(cls):
        # get data from parser
        root_args = root_parser.parse_args()
        nested_one_args = nested_one_parser.parse_args(req=root_args)
        # find user in database
        user = UserModel.find_by_username(nested_one_args['username'])
        # check password
        if user:
            if safe_str_cmp(user.password, nested_one_args['password']):
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(user.id)
                return {
                           'access_token': access_token,
                           'refresh_token': refresh_token
                       }, 200
            else:
                return {'message': 'Password does not match'}, 401
        return {'message': 'No such user'}, 400


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLACKLIST.add(jti)
        return {'message': 'successfully logged out'}, 200

#
# class UserLogin(Resource):
#     @classmethod
#     def post(cls):
#         try:
#             user_json = request.get_json()
#             user_data = user_schema.load(user_json)
#         except ValidationError as err:
#             return err.messages, 400
#
#         user = UserModel.find_by_username(user_data.username)
#
#         if user and safe_str_cmp(user_data.password, user.password):
#             access_token = create_access_token(identity=user.id, fresh=True)
#             refresh_token = create_refresh_token(user.id)
#             return {"access_token": access_token, "refresh_token": refresh_token}, 200
#
#         return {"message": INVALID_CREDENTIALS}, 401
#

# class UserLogout(Resource):
#    @classmethod
#    @jwt_required()
#    def post(cls):
# jti = get_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
#        user_id = get_jwt_identity()
# BLOCKLIST.add(jti)
#        return {"message": USER_LOGGED_OUT.format(user_id)}, 200


# class TokenRefresh(Resource):
#    @classmethod
#    @jwt_required(refresh=True)
#    def post(cls):
#        current_user = get_jwt_identity()
#        new_token = create_access_token(identity=current_user, fresh=False)
#        return {"access_token": new_token}, 200
