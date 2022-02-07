from resources.Session import Session
from resources.device import DeviceRegister, DeviceStatus
from resources.reset_password import ResetPassword, ForgotPassword, ResetTokenValidator
from resources.user import UserRegister, UserLogin, UserLogout, User, TokenRefresh


def initialize_routes(api):
    api.add_resource(UserRegister, "/register")
    api.add_resource(DeviceRegister, "/DeviceRegister")
    api.add_resource(DeviceStatus, "/DeviceStatus")
    api.add_resource(User, "/user/profile")
    api.add_resource(UserLogin, "/login")
    api.add_resource(TokenRefresh, "/refresh")
    api.add_resource(UserLogout, "/logout")
    api.add_resource(ForgotPassword, "/forgot_password")
    api.add_resource(ResetTokenValidator, "/reset_link")
    api.add_resource(ResetPassword, "/reset_password")
    api.add_resource(Session, "/session")