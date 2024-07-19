from sql_alchemy import databank

class SiteModel(databank.Model):
    __tablename__ = 'sites'

    site_id = databank.Column(databank.Integer, primary_key = True)
    url = databank.Column(databank.String(80))
    hotels = databank.relationship('HotelModel')


    def __init__(self,url):
        self.url = url


    def json(self):
        return {
            'site_id' : self.site_id,
            'url' : self.url,
            'hotels' : [hotel.json() for hotel in self.hotels]
        }

    @classmethod
    def find_site(cls, url):
        site = cls.query.filter_by(url=url).first()
        if site:
            return site   
        return None
    
    @classmethod
    def find_by_id(cls, site_id):
        site = cls.query.filter_by(site_id=site_id).first()
        if site:
            return site   
        return None
    

    def save_site(self):
        databank.session.add(self)
        databank.session.commit()
    
    def delete_site (self):
        [hotels.delete_hotel() for hotels in self.hotels]
        databank.session.delete(self)
        databank.session.commit()
    