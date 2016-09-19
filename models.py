from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship
import json
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

class Organization(Base):
    __tablename__ = 'orgs'
    id = Column(Integer, primary_key=True)
    name = Column(String(256),index=True)
    administrators = relationship('Administrator', backref='orgs',lazy='dynamic')
    users = relationship('CommonUser', backref='users',lazy='dynamic')

    def __init__(self,name=None):
    	self.name = name

    def __repr__(self):
    	return '<User %r>' % (self.name)

    @staticmethod
    def list():
    	return Organization.query.all()


class Administrator(Base):
    __tablename__ = 'administrators'
    id = Column(Integer, primary_key=True)
    cid = Column(Integer, ForeignKey('orgs.id'))
    name = Column(String(256),index=True)
    email = Column(String(64),index=True,unique=True)
    password_hash = Column(String(128))

    def __init__(self,name=None,email=None):
    	self.name = name
    	self.email = email

    def __repr__(self):
    	return '<Administrator name=%r, email=%r' % (self.name,self.email)

    def hash_password(self, password):
    	self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


class CommonUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    cid = Column(Integer, ForeignKey('orgs.id'))
    name = Column(String(256),index=True)
    email = Column(String(64),unique=True)
    password_hash = Column(String(128))
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=3600):
        s = Serializer("somekey", expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
        	data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user

	def __init__(self,name=None,email=None):
		self.name = name
		self.email = email		