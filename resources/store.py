from flask import Flask
from flask_restful import Resource,Api
from flask_smorest import abort,Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError 
from models.tabledb import itemModel,storeModel
from db import db

from schemas import plainStoreSchema,plainItemSchema,storeSchema,itemSchema,storeUpdateSchema #if you want to use schema validation

blueprint = Blueprint("storeApi",__name__)

#puppies = []#[{'name':'Rufus'},{'name':'Frankie'}]  #db should be imported instead of static list

@blueprint.route('/store/<string:id>')
class storenames(Resource):  #inherit resource to use resource classes - get,post,put etc
    #@blueprint.arguments(plainPuppySchema)   #will validate the arguements through schema & pass it to the function automatically
    @blueprint.response(200,storeSchema)
    def get(self,id):
        store = storeModel.query.get_or_404(id)  #get_or_404 will either find the item or will automatically abort with 404 code
        return store

    @blueprint.arguments(storeUpdateSchema)
    @blueprint.response(201,storeSchema)
    def put(self,puppy_data,id):      #schema will pass the data to first arguement that is puppy_data
        try:
            store = storeModel.query.get(id)
            if store:
                store.name= puppy_data['name']
            
            else:
                store = storeModel(id = id, **puppy_data)
            
            db.session.add(store)
            db.session.commit()

            return store
        
        except SQLAlchemyError:
            abort(500, "error occured")



    def delete(self,id):
        store = storeModel.query.get_or_404(id)
        db.session.delete(store)
        db.session.commit()
        return "store with id {id} has been deleted"


@blueprint.route('/storedata')
class Puppylist(Resource):
    @blueprint.response(200,storeSchema(many=True))
    def get(self):
        return storeModel.query.all()
        

    @blueprint.arguments(storeSchema)
    @blueprint.response(201,storeSchema)
    def post(self,pupyy_data):
        store = storeModel(**pupyy_data)  #passing key value pair of incoming data to puppymodel

        try:
            db.session.add(store)
            db.session.commit()
        
        except IntegrityError:   #for violating databse integrity sunch as unique name etc
            abort(400,"Puppy with this name already exists")

        except SQLAlchemyError:
            abort(500,"An error accured while create puppy data")

        return store

