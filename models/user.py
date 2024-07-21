from flask import request, url_for
from sql_alchemy import databank
from requests import post


MAILGUN_DOMAIN = 'sandboxb0d3e02541804e9c8a0e54f8298fba35.mailgun.org'
MAILGUN_API_KEY = 'pubkey-a7cd52f294cde579807b719dc3db28e6'
FROM_TITLE ='no-replay'
FROM_EMAIL ='no-replay@restapi.com'


class UserModel(databank.Model):
    __tablename__ = 'users'

    user_id = databank.Column(databank.Integer, primary_key = True)
    login = databank.Column(databank.String(40), nullable=False, unique= True)
    password = databank.Column(databank.String(40), nullable=False)
    email = databank.Column(databank.String(80), nullable=False, unique= True)
    actived = databank.Column(databank.Boolean, default=False)

    def __init__(self, login, password, email, actived):
        self.login = login
        self.password = password
        self.email = email
        self.actived = actived


    def json(self):
        return {
            'user_id' : self.user_id,
            'login' : self.login,
            'email' : self.email,
            'actived' : self.actived
        }


    def send_confirmation_email(self):

        link = request.url_root[:-1] + url_for('userconfirm', user_id=self.user_id)
        return post('https://api.mailgun.net/v3/{}/messages'.format(MAILGUN_DOMAIN),
                    auth= ('api', MAILGUN_API_KEY),
                    data= {'from': '{} <{}>'.format(FROM_TITLE, FROM_EMAIL),
                          'to' : self.email,
                          'subject' : 'Register Confirmation',
                          'text':'Confirm your e-mail in the next link: {}'.format(link),
                          'html' :'<html><p>\
                           Confirm your e-mail in the next link: <a href="{}">CONFIRM EMAIL</a>\
                           </p></html>'.format(link)
                           }
                    )
                

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user   
        return None
    
    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login = login).first()
        if user:
            return user   
        return None
    

    def save_user(self):
        databank.session.add(self)
        databank.session.commit()
        

    def delete_user(self):
        databank.session.delete(self)
        databank.session.commit()
    