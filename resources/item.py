from flask import Flask
from flask_restful import Resource,Api
from flask_smorest import abort,Blueprint
from db import db
from sqlalchemy.exc import IntegrityError,SQLAlchemyError

from schemas import itemSchema,plainItemSchema

blueprint = Blueprint('itemApi', __name__)

from models.tabledb import itemModel 

@blueprint.route('/item/<string:toyid>')
class itemnames(Resource):  #inherit resource to use resource classes - get,post,put etc
    #@blueprint.arguments(getpuppy)   #will validate the arguements through schema & pass it to the function automatically
    @blueprint.response(200,itemSchema)
    def get(self,toyid):
        item = itemModel.query.get_or_404(toyid)  #get_or_404 will either find the item or will automatically abort with 404 code
        return item

    @blueprint.arguments(itemSchema)
    @blueprint.response(201,itemSchema)
    def put(self,toy_data,toyid):
        item = itemModel.query.get(toyid)
        if item:
            item.name= toy_data['name']
            item.storeid = toy_data['storeid']
        
        else:
            item = itemModel(id = toyid, **toy_data)
        
        db.session.add(item)
        db.session.commit()

        return item


    def delete(self,toyid):
        item = itemModel.query.get_or_404(toyid)
        db.session.delete(item)
        db.session.commit()
        return "item deleted successfully"

@blueprint.route('/itemdata')
class toylist(Resource):
    @blueprint.response(200,itemSchema(many=True))
    def get(self):
        return itemModel.query.all()

    @blueprint.arguments(itemSchema)
    @blueprint.response(201,itemSchema)
    def post(self,toy_data):
        item = itemModel(**toy_data)
        try:
            db.session.add(item)
            db.session.commit()

        except IntegrityError:
            abort(400, "Toy already exists")

        except SQLAlchemyError:
            abort(500,"Error occured")    

        return item

