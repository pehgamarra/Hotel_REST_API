from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hotels = [
    {
        'hotel_id' : 'alpha',
        'name': 'Alpha Hotel',
        'star' : 4.3,
        'daily' : 420.34,
        'city' : 'Rio de Janeiro'
    }, 
    {
        'hotel_id' : 'bravo',
        'name': 'Bravo Hotel',
        'star' : 4.4,
        'daily' : 380.90,
        'city' : 'Las Vegas'
    }, 
    {
        'hotel_id' : 'charlie',
        'name': 'Charlie Hotel',
        'star' : 3.9,
        'daily' : 320.20,
        'city' : 'Miami'
    }, 
]

class Hotels(Resource):

    def get(self):
        return {'hotels' : [hotel.json() for hotel in HotelModel.query.all()]}
    


class Hotel(Resource):
    args = reqparse.RequestParser()
    args.add_argument('name'),
    args.add_argument('star'),
    args.add_argument('daily'),
    args.add_argument('city')


    def get(self, hotel_id):   
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message' : 'Hotel not found.'}, 404
    
    
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message" : "Hotel id'{}'already exists.".format(hotel_id)}, 400 #bad
        
        data = Hotel.args.parse_args()
        hotel_object = HotelModel(hotel_id, **data)
        hotel_object.save_hotel()
        return hotel_object.json()

    def put(self, hotel_id): 
        data = Hotel.args.parse_args()
        hotel_find = HotelModel.find_hotel(hotel_id)
        if hotel_find:
            hotel_find.update_hotel(**data)
            hotel_find.save_hotel()
            return hotel_find.json(), 200
        
        hotel_object = HotelModel(hotel_id, **data)
        hotel_object.save_hotel()
        return hotel_object.json(), 201
    

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            hotel.delete_hotel()
            return {'message' : 'Hotel deleted.'},200
        return {'message' : 'Hotel not found.'},404