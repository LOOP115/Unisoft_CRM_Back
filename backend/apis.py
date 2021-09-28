from flask_restful import Resource, reqparse
import requests
from backend import api, db
from backend.models import User

put_args = reqparse.RequestParser()
put_args.add_argument("someData", type=str, help="Put some data", required=True)
put_args.add_argument("exampleData", type=int, help="int data")


class Test(Resource):
    def get(self, name):
        return {"data": "this name is " + name}

    def post(self, name):
        return {"data": "this is post api"}

    def put(self, name):
        args = put_args.parse_args()
        return {name:args}, 201

api.add_resource(Test, "/test/<string:name>")