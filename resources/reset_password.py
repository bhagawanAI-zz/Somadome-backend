from flask import request, render_template
from flask_restful import Resource
import datetime
from flask_jwt_extended import create_access_token, decode_token
from services.mail_service import send_email

from models.user import UserModel


class ForgotPassword(Resource):
    def post(self):
        url = request.host_url + 'reset_password/'
        try:
            body = request.get_json()
            email = body.get('email')
            if not email:
                return "Please provide email"

            user = UserModel.find_by_email(email)
            if not user:
                return "Email does not exist"

            expires = datetime.timedelta(hours=24)
            reset_token = create_access_token(str(user.userid), expires_delta=expires)

            send_email('[Movie-bag] Reset Your Password',
                       sender='evilcallsdad95@gmail.com',
                       recipients=[user.email],
                       text_body=render_template('email/reset_password.txt',
                                                 url=url + reset_token),
                       html_body=render_template('email/reset_password.html',
                                                 url=url + reset_token))
            return {"message": "Email sent to registered mail id"}
        except Exception as e:
            raise e


class ResetTokenValidator(Resource):
    def post(self):
        url = request.host_url + 'reset_link/'
        try:
            body = request.get_json()
            reset_token = body.get('reset_token')
            # password = body.get('password')

            if not reset_token:  # or not password:
                return "token not found"

            user_id = decode_token(reset_token)['sub']

            user = UserModel.find_by_id(user_id)
            email_id = user.email

            if user:
                return {"user_id": user_id,
                        "email_id": email_id,
                        "status": "Authenticated"
                        }
        except Exception as e:
            raise e


class ResetPassword(Resource):
    def post(self):
        try:
            body = request.get_json()
            password = body.get('password')
            user_id = body.get('user_id')
            if not password:
                return "please provide updated password"
            user = UserModel.find_by_id(user_id)
            user.password = password
            user.save_to_db()
            send_email('[Movie-bag] Password reset successful',
                       sender='evilcallsdad95@gmail.com',
                       recipients=[user.email],
                       text_body='Password reset was successful',
                       html_body='<p>Password reset was successful</p>')
            return "Password Reset successful"

        except Exception as e:
            raise e
