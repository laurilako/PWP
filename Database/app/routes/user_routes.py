from flask import jsonify, request, g
from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from app.schemas.users import RegisterUser
from app.models.models import User
import datetime

# from app.db.users import users, user_self
# from app.services.user_services import UserService
# from app.helpers.auth_helpers import validate_token

user_bp = Blueprint("user", __name__, url_prefix="/users")

# def get_user_service():
#     if 'user_service' not in g:
#         g.user_service = UserService()
#     return g.user_service

@user_bp.route("/", methods=["GET"])
class Users(MethodView):
    def get(self):
        return jsonify({"message": "PLACEHOLDER"}), 200
    
@user_bp.route("/signup", methods=["POST"])
class Register(MethodView):
    def post(self):
        try: 
            # get data from request
            data = request.json
            # validate data
            register_schema = RegisterUser()
            validated_data = register_schema.load(data)
            # check if confirm password matches password
            if validated_data["password"] != validated_data["confirm_password"]:
                return jsonify({"message": "Passwords do not match"}), 400
            
            # check if user already exists
            existing_user = User.objects(username=validated_data["username"]).first()
            if existing_user:
                return jsonify({"message": "User already exists"}), 400

            # check if email already exists
            existing_email = User.objects(email=validated_data["email"]).first()
            if existing_email:
                return jsonify({"message": "Email already exists"}), 400
            
            # create user object
            user = User(
                username=validated_data["username"],
                email=validated_data["email"],
                password=validated_data["password"]
            )
            # hash password and save user object to database
            User.hash_password(user)
            user.save()

            return jsonify({"message": "User created successfully"}), 201
        except Exception as e:
            print(e)
            return jsonify({"message": "Error while creating user"}), 400
    

@user_bp.route("/login", methods=["POST"])
class Login(MethodView):
    def post(self):
        # get data from request
        data = request.json
        # check if user exists
        user = User.objects(username=data["username"]).first()
        
        # check if user exists and password is correct
        if user and user.check_password(data["password"]):
            # 7 day jwt token
            expires = datetime.timedelta(days=7)
            access_token = create_access_token(identity=user.username, expires_delta=expires)
            # return token to client
            return jsonify({"message": "Login successful", "token": access_token}), 200
        return jsonify({"message": "Invalid username or password"}), 400
    
# @user_bp.route("/<string:username>", methods=["GET", "PUT", "DELETE"])
# class User(MethodView):
#     def get(self, username):
#         user_service = get_user_service()
#         #user = user_service.get_user_by_username(username)
#         user = user_self
#         if user:
#             return jsonify({"message": "User found", "user": user}), 200
#         return jsonify({"message": "User not found"}), 404

#     def put(self, username):
#         user_service = get_user_service()
#         #Still need to validate this
#         api_key = request.headers.get("X-API-KEY", None)
#         #user = user_service.get_user_by_username(username)
#         user = user_self
#         data = request.json
#         # We should check here that the user is authorized to post changes to profile
#         if user and data and api_key:
#             # Update user profile data now
#             #user_service.update_user(username, data)
#             return jsonify({"message": "Update successful"}), 200
#         return jsonify({"message": "Missing data"}), 400

#     def delete(self, username):
#         user_service = get_user_service()
#         #user = user_service.get_user_by_username
#         user = user_self
#         # Check that client is authorized to do this operation.
#         # Use boolean value for now. Still need to validate this API key.
#         api_key = request.headers.get("X-API-KEY", None)
#         if user and api_key:
#             #deleted = user_service.delete_user(username)
#             deleted = True
#             if deleted:
#                 return jsonify({'message': f"User {username} has been deleted"}), 200
#         return jsonify({'message': "Something failed"}), 400