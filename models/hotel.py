from sql_alchemy import databank

class HotelModel(databank.Model):
    __tablename__ = 'hotels'

    hotel_id = databank.Column(databank.String, primary_key = True)
    name = databank.Column(databank.String(80))
    star = databank.Column(databank.Float(precision=1))
    daily = databank.Column(databank.Float(precision=2))
    city = databank.Column(databank.String(40))

    def __init__(self, hotel_id, name, star, daily, city):
        self.hotel_id = hotel_id
        self.name = name
        self.star = star
        self.daily = daily
        self.city = city   


    def json(self):
        return {
            'hotel_id' : self.hotel_id,
            'name' : self.name,
            'star' : self.star,
            'daily' : self.daily,
            'city' : self.city
        }

    @classmethod
    def find_hotel(cls, hotel_id):
        hotel = cls.query.filter_by(hotel_id=hotel_id).first() # = SELECT * FROM hotels WHERE hotel_id = $hotel_id limit_1
        if hotel:
            return hotel   
        return None
    

    def save_hotel(self):
        databank.session.add(self)
        databank.session.commit()
    
    def update_hotel(self, name, star, daily, city):
        self.name = name
        self.star = star
        self.daily = daily
        self.city = city

    def delete_hotel (self):
        databank.session.delete(self)
        databank.session.commit()
    