from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from models.site import SiteModel
from resources.filters import not_city_search, with_city_search, normalize_path_params
from flask_jwt_extended import jwt_required
import sqlite3


path_params = reqparse.RequestParser()
path_params.add_argument('city', type=str, location='args')
path_params.add_argument('star_min', type=float, location='args')
path_params.add_argument('star_max', type=float, location='args')
path_params.add_argument('daily_min', type=float, location='args')
path_params.add_argument('daily_max', type=float, location='args')
path_params.add_argument('limit', type=int, location='args')
path_params.add_argument('offset', type=int, location='args')



class Hotels(Resource):

    def get(self):
        connection = sqlite3.connect('instance/databank.db')
        cursor = connection.cursor()

        data = path_params.parse_args()
        valid_data = {key:data[key] for key in data if data[key] is not None}
        parameters = normalize_path_params(**valid_data)

        if not parameters.get('city'):
            tupla = tuple([parameters[key] for key in parameters])
            result = cursor.execute(not_city_search, tupla)
        else :
            tupla = tuple([parameters[key] for key in parameters])
            result = cursor.execute(with_city_search, tupla)

        hotels = []
        for line in result:
            hotels.append({
            'hotel_id' : line[0],
            'name' : line[1],
            'star' : line[2],
            'daily' : line[3],
            'city' : line[4],
            'site_id' : line[5]
            })
        
        connection.close
        print(data)
        return {'hotels' : hotels}
    

class Hotel(Resource):
    args = reqparse.RequestParser()
    args.add_argument('name', type=str, required=True, help="The field 'nome' cannot be left blank"),
    args.add_argument('star', type=float, required=True, help="The field 'star' cannot be left blank"),
    args.add_argument('daily', type=float, required=True, help="The field 'daily' cannot be left blank"),
    args.add_argument('city', type=str, required=True, help="The field 'city' cannot be left blank")
    args.add_argument('site_id', type=int, required=True, help="Every hotel needs to be linked with a site")


    def get(self, hotel_id):   
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message' : 'Hotel not found.'}, 404
    
    
    @jwt_required()
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message" : "Hotel id'{}'already exists.".format(hotel_id)}, 400
        
        data = Hotel.args.parse_args()
        hotel_object = HotelModel(hotel_id, **data)
        
        if not SiteModel.find_by_id(data['site_id']):
            return {'message' : 'The hotel must be associated to a valid site id'}, 400
        try:
            hotel_object.save_hotel()
        except Exception:
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
        except Exception:
            return {'message' : 'An internal error ocurred trying to save hotel.'}, 500
        return hotel_object.json(), 201
    

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
        except Exception:
                return {'message' : 'An error ocurred trying to delete hotel.'},500    
            return {'message' : 'Hotel deleted.'},200
        return {'message' : 'Hotel not found.'},404