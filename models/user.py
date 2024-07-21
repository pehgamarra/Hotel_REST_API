from sql_alchemy import databank

class UserModel(databank.Model):
    __tablename__ = 'users'

    user_id = databank.Column(databank.Integer, primary_key = True)
    login = databank.Column(databank.String(40))
    password = databank.Column(databank.String(40))
    actived = databank.Column(databank.Boolean, default=False)

    def __init__(self, login, password, actived):
        self.login = login
        self.password = password
        self.actived = actived


    def json(self):
        return {
            'user_id' : self.user_id,
            'login' : self.login,
            'actived' : self.actived
        }


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
    