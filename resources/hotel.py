from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3


def normalize_path_params(city = None,
                          star_min = 0,
                          star_max = 5,
                          daily_min = 0,
                          daily_max = 10000,
                          limit = 0,
                          offset = 0, **data) :
    if city:
        return {
            'star_min':star_min,
            'star_max':star_max,
            'daily_min':daily_min,
            'daily_max':daily_max,
            'city' : city,
            'limit':limit,
            'offset':offset}
    return {
            'star_min':star_min,
            'star_max':star_max,
            'daily_min':daily_min,
            'daily_max':daily_max,
            'limit':limit,
            'offset':offset
            }


path_params = reqparse.RequestParser()
path_params.add_argument('city', type=str)
path_params.add_argument('star_min', type=float)
path_params.add_argument('star_max', type=float)
path_params.add_argument('daily_min', type=float)
path_params.add_argument('daily_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


class Hotels(Resource):

    def get(self):

        data = path_params.parse_args()
        valid_data ={key:data[key] for keys in data if data[key] is not None}
        return {'hotels' : [hotel.json() for hotel in HotelModel.query.all()]}
    

class Hotel(Resource):
    args = reqparse.RequestParser()
    args.add_argument('name', type=str, required=True, help="The field 'nome' cannot be left blank"),
    args.add_argument('star', type=float, required=True, help="The field 'star' cannot be left blank"),
    args.add_argument('daily', type=float, required=True, help="The field 'daily' cannot be left blank"),
    args.add_argument('city', type=str, required=True, help="The field 'city' cannot be left blank")


    def get(self, hotel_id):   
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message' : 'Hotel not found.'}, 404
    
    
    @jwt_required()
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message" : "Hotel id'{}'already exists.".format(hotel_id)}, 400 #bad
        
        data = Hotel.args.parse_args()
        hotel_object = HotelModel(hotel_id, **data)
        try:
            hotel_object.save_hotel()
        except:
            return {'message' : 'An internal error ocurred trying to save hotel.'}, 500
        return hotel_object.json()


    @jwt_required()
    def put(self, hotel_id): 
        data = Hotel.args.parse_args()
        hotel_find = HotelModel.find_hotel(hotel_id)
        if hotel_find:
            hotel_find.update_hotel(**data)
            hotel_find.save_hotel()
            return hotel_find.json(), 200
        
        hotel_object = HotelModel(hotel_id, **data)
        try:
            hotel_object.save_hotel()
        except:
            return {'message' : 'An internal error ocurred trying to save hotel.'}, 500
        return hotel_object.json(), 201
    

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message' : 'An error ocurred trying to delete hotel.'},500    
            return {'message' : 'Hotel deleted.'},200
        return {'message' : 'Hotel not found.'},404