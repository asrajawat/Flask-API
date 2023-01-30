from marshmallow import Schema,fields
#The marshmallow1 library is used to define what data fields we want, and then we can pass incoming data through the validator.

class plainItemSchema(Schema):
    name = fields.Str(required= True)
    id = fields.Int(dump_only= True)  #only while returning the response
    storeid = fields.Int(required=True)

class plainStoreSchema(Schema):
    name = fields.Str(required= True)
    id = fields.Int(dump_only= True)  #only while returning the response

class plainTagsSchema(Schema):
    name = fields.Str(required= True)
    id = fields.Int(dump_only= True)  #only while returning the response

class itemSchema(plainItemSchema):    
    store = fields.Nested(plainStoreSchema(), dump_only= True) #store object for relationship
    tag = fields.Nested(plainTagsSchema(), dump_only= True)


class storeSchema(plainStoreSchema):    
    items = fields.Nested(plainItemSchema(), dump_only= True) #item object for relationship
    tags = fields.Nested(plainTagsSchema(),dump_only= True)

class storeUpdateSchema(Schema):
    name = fields.Str(required= True)

class tagSchema(plainTagsSchema):
    storeid = fields.Int(load_only=True) 
    store = fields.Nested(plainStoreSchema(),dump_only=True)
    item = fields.Nested(plainItemSchema(),dump_only=True)

class tagItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(itemSchema)
    tag = fields.Nested(tagSchema)

class userSchema(Schema):
    id = fields.Int(dump_only= True)
    username = fields.Str(required = True)
    password = fields.Str(required= True, load_only= True) #load_only = true means it wont be visible 