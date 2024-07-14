from flask_restful import Resource, reqparse
from blacklist import BLACKLIST
from models.user import UserModel
from secrets import compare_digest
from flask_jwt_extended import create_access_token, jwt_required, get_jwt



args = reqparse.RequestParser()
args.add_argument ('login', type=str, required=True, help="The field 'login' cannot be left blank"),
args.add_argument ('password', type=str, required=True, help="The field 'password' cannot be left blank")

class User(Resource):
    #/user/{user_id}

    def get(self, user_id):   
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message' : 'User not found.'}, 404
    
    
    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message' : 'An error ocurred trying to delete User.'},500    
            return {'message' : 'User deleted.'},200
        return {'message' : 'User not found.'},404


class UserRegister(Resource):
    # /registration
    
    def post(self):
        data = args.parse_args()

        if UserModel.find_by_login(data['login']):
            return {'message': "The login '{}' already existis.".format(data['login'])}
        
        user = UserModel(login=data['login'], password=data['password'])
        user.save_user()
        return {'message': 'User created successfully!'},201

class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = args.parse_args()

        user = UserModel.find_by_login(data['login'])

        if user and compare_digest(user.password, data['password']):
            access_token = create_access_token(identity=user.user_id)
            return {'access_token':access_token}, 200
        return {'message' : 'The username or password is incorret.'}, 401


class UserLogout(Resource):

   @jwt_required()
   def post(self):
       jwt_id = get_jwt()['jti'] #JWT Token Identifier
       BLACKLIST.add(jwt_id)
       return {'message' : 'Logged out successfully!'},200