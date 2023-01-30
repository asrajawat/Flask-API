from flask import Flask
from flask_restful import Resource,Api
from flask_smorest import abort,Blueprint
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token

blueprint = Blueprint("userApi",__name__)

from db import db
from models.tabledb import tagModel,storeModel,itemModel,itemTagsModel,userModel
from schemas import plainTagsSchema,tagSchema,tagItemSchema,userSchema

@blueprint.route("/register")
class UserRegister(Resource):
    @blueprint.arguments(userSchema)
    def post(self, user_data):
        if userModel.query.filter(userModel.username == user_data['username']).first():
            abort(404,message ="User with this username already exists")
        else:
            user = userModel(username = user_data['username'],password=pbkdf2_sha256.hash(user_data['password']))
            db.session.add(user)
            db.session.commit()
            return {"Message":user_data['username']+" has been registered successfully."},201
        
@blueprint.route("/login")
class UserLogin(Resource):
    @blueprint.arguments(userSchema)
    def get(self,user_data):
        user = userModel.query.filter(userModel.username ==user_data['username']).first()
        if user and pbkdf2_sha256.verify(user_data['password'],user.password):
            access_token = create_access_token(identity=user.id)

            return{"Token":access_token},200
        
        else:
            abort(401,message="invalid credentials")