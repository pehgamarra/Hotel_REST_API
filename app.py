from flask import Flask
from flask_restful import Api
from resources.hotel import Hotels, Hotel
from resources.user import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

@app.before_request
def bankcreate():
    databank.create_all()

api.add_resource(Hotels, '/hotels')
api.add_resource(Hotel, '/hotels/<string:hotel_id>')
api.add_resource(User, '/user/<int:user_id>')

if __name__ == '__main__':
    from sql_alchemy import databank
    databank.init_app(app)
    app.run(debug=True)

# run into http://127.0.0.1:5000/hotels on postman
