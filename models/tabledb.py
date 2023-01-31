#VERY IMPORTANT TO PUT DB HERE AS THE SAME NEEDS TO BE IMPORTED IN APP.PY
from db import db

class storeModel(db.Model):
    __tablename__ = 'store'
    name = db.Column(db.String(80), unique = True)
    id = db.Column(db.Integer,primary_key=True)
    
    #one to many relationship with item
    #we passed toyModel as that is the name of another class with which relationship needs to be there
    items = db.relationship('itemModel', back_populates='store',lazy ='dynamic', cascade="all,delete" )
    #The cascade="all,delete" argument in the relationship() call for the StoreModel.items attribute specifies that when 
    # a store is deleted, all of its related items should also be deleted.
    #one to many relationship with tags
    tags = db.relationship('tagModel',back_populates="stores",lazy = 'dynamic',cascade= "all,delete") #in back_populates we pass 
                                                                                                    #relationship name from another class

class itemModel(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90))
    description = db.Column(db.String())
    # We use puppy.id because __tablename__='puppy'
    storeid = db.Column(db.Integer,db.ForeignKey('store.id'))
    store = db.relationship('storeModel',back_populates = 'items')
    tag = db.relationship('tagModel',back_populates='item',secondary="itemtags") # in seconday we passed second table to look into the id

class tagModel(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer,primary_key= True)
    name = db.Column(db.String(90),unique= True)
    storeid =db.Column(db.Integer,db.ForeignKey('store.id'))
    stores = db.relationship("storeModel", back_populates="tags")

    item = db.relationship('itemModel',back_populates='tag',secondary="itemtags")

class itemTagsModel(db.Model):
    __tablename__ = "itemtags"
    id = db.Column(db.Integer,primary_key=True)
    item_id= db.Column(db.Integer,db.ForeignKey('item.id'))
    tag_id= db.Column(db.Integer,db.ForeignKey('tag.id'))

class userModel(db.Model):
    __tablename__= "users"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(),unique= True, nullable=False )
    password = db.Column(db.String(256), nullable = False)
