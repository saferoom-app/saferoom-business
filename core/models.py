from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Table
from database import Base
from sqlalchemy.orm import relationship
import json
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
import safeglobals
from datetime import date
from dateutil.relativedelta import relativedelta
import uuid
import datetime
import rncryptor
import base64

relationship_table = Table('users_to_services',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'),nullable=False),
    Column('service_id', Integer, ForeignKey('services.id'),nullable=False)
)

class Organization(Base):
    __tablename__ = 'orgs'
    id = Column(Integer, primary_key=True)
    name = Column(String(256),index=True)
    administrators = relationship('Administrator', backref='orgs',lazy='dynamic')
    users = relationship('CommonUser', backref='users',lazy='dynamic')
    plan_id = Column(Integer, ForeignKey('plans.id'))
    plan = relationship('Plan')
    expires_in = Column(DateTime)
    evaluate_to = Column(DateTime)
    order_id = Column(Integer)

    def __init__(self,name=None):
    	self.name = name

    def __repr__(self):
    	return '<Org %r, Administrators: %r>' % (self.name)

    @staticmethod
    def list():
    	return Organization.query.all()

    @staticmethod
    def get(id):
        return Organization.query.filter_by(id=id).first()

    def set_expiration_values(self,plan):
        if (plan == safeglobals.plan_free ):
            self.expires_in =  date.today() + relativedelta(months=+1)
        else:
            self.expires_in = date.today() + relativedelta(months=+12)
        self.evaluate_to = date.today() + relativedelta(months=+1)

    def set_premium(self,plan):
        self.premium = (plan == safeglobals.plan_premium)


class Administrator(Base):
    __tablename__ = 'administrators'
    id = Column(Integer, primary_key=True)
    cid = Column(Integer, ForeignKey('orgs.id'))
    name = Column(String(256),index=True)
    email = Column(String(64),index=True,unique=True)
    session_key = Column(String(32),unique=True)
    password_hash = Column(String(128))
    org = relationship('Organization')


    def __init__(self,name=None,email=None):
    	self.name = name
    	self.email = email

    def __repr__(self):
    	return '<Administrator name=%r, email=%r' % (self.name,self.email)

    def hash_password(self, password):
    	self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_session_key(self):
        self.session_key = str(uuid.uuid4())


class CommonUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    cid = Column(Integer, ForeignKey('orgs.id'))
    name = Column(String(256),index=True)
    email = Column(String(64),unique=True)
    password_hash = Column(String(128))
    created = Column(DateTime,default=datetime.datetime.utcnow)
    token = relationship("Token",uselist=False,backref='user')
    services = relationship("Service",secondary=relationship_table, backref='services')
    org = relationship("Organization")


    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=3600):
        s = Serializer(safeglobals.secret_key, expires_in=expiration)
        return s.dumps({'id': self.id})

    def encrypt_user_id(self,key):
        cryptor = rncryptor.RNCryptor()
        encrypted_string = cryptor.encrypt(str(self.id),key)
        return base64.b64encode(encrypted_string)

    @staticmethod
    def decrypt_user_id(encrypted_id,key):
        cryptor = rncryptor.RNCryptor()
        return cryptor.decrypt(base64.b64decode(encrypted_id),key)

    def __init__(self,name=None,email=None):
		self.name = name
		self.email = email

class Token(Base):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('users.id'))
    token = Column(String(128),unique=True)

    def __init__(self,token=None):
        self.token = token

    def __repr__(self):
        return '<Token %r>' % (self.token)

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(safeglobals.secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return False    # valid token, but expired
        except BadSignature:
            return False    # invalid token
        return True

class Plan(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True)
    name = Column(String(64),index=True)
    premium = Column(Boolean)

    def __init__(self,name,premium):
        self.name = name
        self.premium = premium

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True)
    name = Column(String(32),index=True)

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return "<Service %r>" % (self.name)


