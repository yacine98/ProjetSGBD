from flask import Flask, request ,jsonify
from flask_restplus import Api, Resource
from flask_restful import  reqparse
import kyasqlf


app = Flask(__name__)
api = Api(app=app, version='0.1', title='PROJET DE BASE DE DONNEES AVANCEES', description='SGBD', validate=True)

ns_auth= api.namespace('AUTHENTIFY',description="AUTHENTIFICATION")
ns_creation = api.namespace('CREATE',description="CREATION USERS,BASES,TABLES")
ns_insertion = api.namespace('INSERT',description="INSERTION DANS TABLES")
ns_selection = api.namespace('SELECT',description="SELECTION DANS TABLES")
ns_drop = api.namespace('DROP',description="SUPPRESSION DANS BASES")
ns_describe = api.namespace('DESCRIBE',description="DESCRIPTION DE TABLES")
ns_showtable = api.namespace('SHOWTABLE',description="MONTRE LES TABLES DE LA BASE")
ns_deluser = api.namespace('DELUSER',description="Supprime un utilisateur")



@ns_auth.route("/api/authentification/<string:user>/<string:password>")
class auth(Resource):
        def get(self,user,password):
       		'''Get Authentify'''
        	return kyasqlf.auth(user,password) 

@ns_creation.route("/api/createdatabase/<string:namebase>/<string:type>/<string:base>")
class CreateDatabase(Resource):
	def post(self,namebase,type,base):
		'''Creer une base de donnees'''
		return kyasqlf.create(namebase,type,base)

@ns_creation.route("/api/createtable/<string:nametable>/<string:type>/<string:namebase>")
class CreateTable(Resource):
        def post(self,nametable,type,namebase):
        	'''Creer une table'''
        	return kyasqlf.create(nametable,type,namebase)

@ns_creation.route("/api/adduser/<string:nameuser>/<string:password_user>")
class adduser(Resource):
        def post(self,nameuser,password_user):
        	'''Ajouter un utilisateur'''
        	return kyasqlf.adduser(nameuser,password_user)

@ns_insertion.route("/api/insert_into_user/<string:nametable>/<string:o>/<string:bd>")
class insert_into_table(Resource):
        
        def put(self,nametable,o,bd):
       		'''Insert dans table'''
        	return kyasqlf.insert(nametable,o,bd) 


@ns_selection.route("/api/selection_table/<string:nametable>/<string:o>/<string:namebase>")
class selecttiondetable(Resource):
        
        def get(self,nametable,o,namebase):
       		'''Selection de table'''
        	return kyasqlf.select(nametable,o,namebase) 

@ns_describe.route("/api/describe_table/<string:nametable>/<string:namebase>")
class describe_table(Resource):
        def get(self,nametable,namebase):
       		'''Describe table'''
        	return kyasqlf.describe(nametable,namebase) 


@ns_drop.route("/api/drop_database/<string:namebase>")
class drop_database(Resource):
	def delete(self,namebase):
		'''deleted database'''
		return kyasqlf.drop(namebase)


@ns_showtable.route("/api/montre_la_table/<string:namebase>")
class showtable(Resource):
        def get(self,namebase):
       		'''Montre la table'''
        	return kyasqlf.showtable(namebase) 

@ns_deluser.route("/api/montre_la_table/<string:user>")
class deluser(Resource):
        def delete(self,user):
       		'''Supprime l'utilisateur'''
        	return kyasqlf.deluser(user) 






app.run(port= 8889,debug=True, host= 'localhost')



