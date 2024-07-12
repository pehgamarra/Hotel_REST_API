from flask_restful import Resource, reqparse

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
        return {'hotels' : hotels}
    

class Hotel(Resource):
    args = reqparse.RequestParser()
    args.add_argument('name'),
    args.add_argument('star'),
    args.add_argument('daily'),
    args.add_argument('city')


    def find_hotel(hotel_id):
        for hotel in hotels:
            if hotel ['hotel_id'] == hotel_id:
                return hotel
        return None

    def get(self, hotel_id):   
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel
        return {'message' : 'Hotel not found.'}, 404
    
    
    def post(self, hotel_id):

        data = Hotel.args.parse_args()

        new_hotel = { 'hotel_id' : hotel_id, **data}

        hotels.append(new_hotel)
        return new_hotel, 200
    

    def put(self, hotel_id):
        
        data = Hotel.args.parse_args()
        new_hotel = { 'hotel_id' : hotel_id, **data}

        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            hotel.update(new_hotel)
            return new_hotel, 200
        hotels.append(new_hotel)
        return new_hotel, 201


    def delete(self, hotel_id):
        global hotels
        hotels = [hotel for hotel in hotels if hotel['hotel_id'] != hotel_id]
        return {'message' : 'Hotel deleted.'}