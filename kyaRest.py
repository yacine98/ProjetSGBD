from flask import Flask, request
from flask_restplus import Api, Resource
from flask_restful import  reqparse
from kyasql import *

app = Flask(__name__)
api = Api(app=app, version='0.1', title='Projet Sgbd Api', description='', validate=True)

ns_kyasql = api.namespace('kyasql',description="SGBD")

users = [
	{
	"name": "Adja",
	"age": 25,
	"occupation": "Etudiante"
	},

	{
	"name": "Khady",
	"age": 21,
	"occupation": "Etudiante"
	},
	{
	"name": "Yacine",
	"age": 21,
	"occupation": "Etudiante"
	}
]

@ns_kyasql.route("/")
class BasesList(Resource):
	def get(self):
		return users
	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument("name")
		parser.add_argument("age")
		parser.add_argument("occupation")
		args = parser.parse_args()

		for user in users:
			if( args["name"]== user["name"]):
				return "User with name {} already exists".format( args["name"])

		user = {
			"name": args["name"],
			"age": args["age"],
			"occupation": args["occupation"]
		}
		users.append(user)
		return user, 201
@ns_kyasql.route("/<string:title>")
class Base(Resource):
	def put(self, title):
		parser = reqparse.RequestParser()
		parser.add_argument("age")
		parser.add_argument("occupation")
		args = parser.parse_args()

		for user in users:
			if(title == user["name"]):
				user["age"] = args["age"]
				user["occupation"] = args["occupation"]
				return user, 200

		user = {
			"name": title,
			"age": args["age"],
			"occupation": args["occupation"]
		}
		users.append(user)
		return user, 201
	def delete(self, title):
		global users
		users =[ user for user in users if user["name"] != title]
		return "{} is deleted.".format(title), 200




app.run(port= 8889, host= 'localhost')


