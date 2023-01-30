from flask import Flask
from flask_restful import Resource,Api
from flask_smorest import abort  # will add some documentation with error code

app = Flask(__name__)

api = Api(app) #api rapper to connect to resource

puppies = []#[{'name':'Rufus'},{'name':'Frankie'}]

class Puppynames(Resource):  #inherit resource to use resource classes - get,post,put etc
    def get(self,name):
        for pup in puppies:
            if pup['name'] == name:
                return pup
        abort (404, message = "puppy not found")

    def post(self,name):
        pup = {'name':name}
        if pup in puppies:
            return "{self.name} already  exists",201
        else:
            puppies.append(pup)
            return pup,201

    def delete(self,name):
        pup = {'name':self.name}
        puppies.remove(pup)
        return {'status':'Deleted {self.name} successfully'}

class Puppylist(Resource):
    def get(self):

        return {'puppies':puppies}

api.add_resource(Puppylist,'/puppieslist')
api.add_resource(Puppynames,'/puppy/<string:name>')

if __name__=='__main__':
    app.run(debug=True)
