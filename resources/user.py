from flask_restful import Resource, reqparse
from models.user import UserModel



class User(Resource):
    #/user/{user_id}

    def get(self, user_id):   
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message' : 'User not found.'}, 404
    
    
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
        args = reqparse.RequestParser()
        args.add_argument ('login', type=str, required=True, help="The field 'login' cannot be left blank"),
        args.add_argument ('password', type=str, required=True, help="The field 'password' cannot be left blank")
        data = args.parse_args()

        if UserModel.find_by_login(data['login']):
            return {'message': "The login '{}' already existis.".format(data['login'])}
        
        user = UserModel(login=data['login'], password=data['password'])
        user.save_user()
        return {'message': 'User created successfully!'},201
