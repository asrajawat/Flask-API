from flask import Flask
from flask_restful import Resource,Api
from flask_smorest import abort,Blueprint
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from flask_jwt_extended import jwt_required,get_jwt

blueprint = Blueprint('tagApi',__name__)
from db import db
from models.tabledb import tagModel,storeModel,itemModel,itemTagsModel
from schemas import plainTagsSchema,tagSchema,tagItemSchema

# Method	  Endpoint	               Description
# ✅ GET	    /store/{id}/tag	        Get a list of tags in a store.
# ✅ POST	/store/{id}/tag	        Create a new tag.
# ❌ POST	/item/{id}/tag/{id}	    Link an item in a store with a tag from the same store.
# ❌ DELETE	/item/{id}/tag/{id}	    Unlink a tag from an item.
# ✅ GET	    /tag/{id}	            Get information about a tag given its unique id.
# ❌ DELETE	/tag/{id}	            Delete a tag, which must have no associated items.


#to Get a list of tags in a store.
@blueprint.route("/store/<string:storeid>/tag/")
class TagsInStore(Resource):
    @jwt_required()
    @blueprint.response(200,tagSchema(many=True))
    def get(self,storeid):
        #optional check in jwt token . we can avoid it
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        store = storeModel.query.get_or_404(storeid)
        return store.tags.all()

    @jwt_required()
    @blueprint.arguments(tagSchema)
    @blueprint.response(201,tagSchema)
    def post(self,tag_data,storeid):
        #check if this tag already exists in same store
        if tagModel.query.filter_by(name= tag_data['name'],storeid=storeid).first():
            abort(400,message="A tag with this name already exists in the same store")
        tag = tagModel(**tag_data, storeid=storeid)
        try:
            db.session.add(tag)
            db.session.commit()

        except SQLAlchemyError as e:
            abort (500,message=str(e))
        
        return tag



#Get information about a tag given its unique id.
#DELETE	/tag/{id}	Delete a tag, which must have no associated items.
@blueprint.route("/tag/<string:tag_id>")
class tagInfo(Resource):
    @jwt_required()
    @blueprint.response(200,tagSchema)
    def get(self,tag_id):

        tag = tagModel.query.get_or_404(tag_id)
        return (tag)

    @jwt_required()
    @blueprint.response(202,description="Deletes a tag if no item is tagged with it.",example={"message": "Tag deleted."})
    @blueprint.alt_response(404, description="Tag not found.")
    @blueprint.alt_response(400,description="Returned if the tag is assigned to one or more items. In this case, the tag is not deleted.")
    def delete(self,tag_id):
        tag = tagModel.query.get_or_404(tag_id)

        if not tag.item:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag" + tag_id + " is deleted successfully"}
        
        else:

            abort(400,message="Could not delete tag. Make sure tag is not associated with any items, then try again.")




# POST	/item/{id}/tag/{id}	    Link an item in a store with a tag from the same store.
#DELETE	/item/{id}/tag/{id}	Unlink a tag from an item.
@blueprint.route("/item/<string:itemid>/tag/<string:tagid>")
class linkTagsToItem(Resource):
    @blueprint.response(201,tagSchema)
    def post(self,itemid,tagid):
        item = itemModel.query.get_or_404(itemid)
        tag = tagModel.query.get_or_404(tagid)

        if tag.storeid != item.storeid:
            abort(500,message = "cant link the tag to item as store id of tag & item is not same")
        else:
            item.tag.append(tag)
            try:
                db.session.add(item)
                db.session.commit()

            except SQLAlchemyError:
                abort(500,message = "an error occured")

            return tag
    
    @blueprint.response(201,tagItemSchema)
    def delete(self,itemid,tagid):
        item = itemModel.query.get_or_404(itemid)
        tag = tagModel.query.get_or_404(tagid)

        item.tag.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()

        except SQLAlchemyError:
            abort(500,message = "an error occured")

        return {"message": "item removed from tag", "itemid":itemid, "tagid":tagid}






    