import os.path 
import json as simplejson
import shutil
#Vérification syntaxe des requêtes
def verification(requete):
	maRequete = requete.split(" ")
	global check
	if len(maRequete)>=3:
		if maRequete[0]!="create" and maRequete[0]!="alter" and maRequete[0]!="adduser" and maRequete[0]!="use" and maRequete[0]!="select" and maRequete[0]!="insert" and maRequete[0]!="update" and maRequete[0]!="show" and maRequete[0]!="describe" and maRequete[0]!="delete":
			print("Cette commande n'est pas reconnue par notre système")
			check=False
		elif maRequete[0] == "create" or maRequete[0]=="alter":
			if maRequete[1]!="table" and maRequete[1] != "user" and maRequete[1] != "database" :
				print("Veuillez revoir le deuxieme mot saisi : la syntaxe est incorrecte")
				check=False
		elif maRequete[0]=="update":
			if len(maRequete)<6:
				print("La commande UPDATE est incomplète ou invalide")
				check=False
			elif maRequete[2]!="set" or maRequete[4]!= "=": 
				print("La syntaxe de la commande UPDATE n'est pas respectée")
				check=False
		elif maRequete[0]=="delete":
			if len(maRequete)!=3 and len(maRequete)!=5:
				print("La commande DELETE est incomplète ou invalide")
				check=False
			if len(maRequete)==3:
				if maRequete[1]!="from":
					print("La syntaxe de la commande DELETE n'est pas respectée")
					check=False
			if len(maRequete)==5:
				if maRequete[1]!="from" or maRequete[3]!="where":
					print("La syntaxe de la commande DELETE n'est pas respectée")
					check=False
		elif maRequete[0]=="insert":
			if len(maRequete)!=3:
				print("La commande INSERT est incomplète ou invalide")
				check=False
			elif maRequete[1]!="into": 
					print("La syntaxe de la commande INSERT n'est pas respectée")
					check=False
		elif maRequete[0]=="select":
			if len(maRequete)!=4:
				print("La commande SELECT est incomplète ou invalide")
				check=False
			elif maRequete[2]!= "from":
				print("La syntaxe de la commande SELECT n'est pas respectée")
				check=False
		elif maRequete[0]=="adduser":
			if len(maRequete)!=3:
				rint("La syntaxe de la commande adduser n'est pas respectée")
				check=False

	elif maRequete[0]!="show" and maRequete[0]!="describe" and maRequete[0]!="select" and maRequete[0]!="use" and maRequete[0]!="drop":
		print("Requête invalide ou incomplète")
		check=False

#Vérification identifiants authentification
def auth(user,password):
	dic=dict()
	dico=dict()
	dico["user"] = user
	dico["password"] = password
	
	with open("users.json",'r') as f :
		dic=simplejson.load(f)
	tab =[]
	tab = dic["users"]
	for i in range (len(tab)):
		if tab[i] == dico :
			return "OK"
	return "REESSAYER SVP"

#Verification Syntaxe Authentification
def veriSynAuth(chaine):
	if len(chaine) !=5:
		return "0"
	elif chaine[0]!="kyasql":
		return "0"
	elif chaine[1]!="-u" or chaine[3]!="-p":
		return "0"
	return "1"

#Commande create
def create(name,type,base):
	if type.upper() == "DATABASE" :
		path = name
		if os.path.exists(path):
			return "database not created"
		else:
			os.mkdir(name)
			return "database created successfully"
	if type.upper() == "USER":
		f=open(name+".json","w")

	if type.upper() == "TABLE":
		path = name+".json"
		if os.path.exists(base+"/"+path):
			return "Table not created"
		else:
			f=open(base+"/"+path,"w")
			f.write("")
			f.close()
			return "Table created successfully"

#Commande drop
def drop(chaine):
	path = chaine
	if os.path.exists(path):
		shutil.rmtree(chaine)
		return "database droped successfully"
	else:
		return "database not droped"

#Commande insert
def insert(base,o,bd):
	attr=[]
	donnee=[]
	chaine=''
	attr,donnee = getData(o)
	tab={}
	for x in range(0,len(attr)):
		tab[attr[x]] = donnee[x]
	path = base+".json"
	if os.path.exists(bd+"/"+path):
		with open(bd+"/"+path,"a+") as g:
			g.seek(0,0)
			if g.read()=='':
				simplejson.dump(tab,g,indent=4)
			else:	
				g.write(",\n")
				simplejson.dump(tab,g,indent=4)
		g.close()
		return "insertion successfull"
	else:
		return "insertion not succesfull"

#Commande select
def select(element,base,bd):
	path = base+".json"
	print("element: "+element)
	if os.path.exists(bd+"/"+path):
		with open(bd+"/"+path,"a+") as f:
			f.seek(0,0)
			k=f.read()
		r="[\n"+k+"\n]"
		m=simplejson.loads(r)
		ch = ""
		element1 = element.split(",")
		print(element1,len(element1))
		attr,donnee = getjsondata(m)
		attr1 = []
		donnee1 = []
		if element1[0] == "*":
			attr1 =attr
			donnee1 = donnee
		else:
			t =[]
			for e in element1:
				attr1.append(e) 
			t = []
			for i in range(0,len(attr1)):
				for x in range(0,len(attr)):
					if attr1[i] == attr[x]:
						t.append(x)
			mod =0
			while mod != len(donnee):
				for j in range(0,len(t)):
					for k in range(mod,mod+len(attr)):
						if t[j]+mod == k:
							donnee1.append(donnee[k])
				mod+=len(attr)
		for chaine in attr1:
			ch+="#"+chaine
		ch+="|"
		for chaine1 in donnee1:
			ch+="#"+chaine1
		print(ch)
		n=simplejson.dumps(m,indent=4)
		return ch
	else:
		return "table not exist"

#Commande space
def space(chaine):
	chaine1=""
	j=0
	for i in range(0,len(chaine)):
		if chaine[i] == " ": 
			if chaine[i-1] == " " or chaine[i-1] == "," or chaine[i-1] == "=" or chaine[i+1] == "," or chaine[i+1] == "=" or chaine[i+1] == "(" or i==0:
				pass
			else:
				chaine1+="#" 
		else:
			if chaine[i] !="(":
				chaine1+=chaine[i]
		if chaine[i] == "(":
				chaine1 += "#("	
	return chaine1

#Commande getData
def getData(chaine):
	donnee = chaine.split("(")
	#print(donnee)
	donnee = donnee[1].split(")")
	donnee = donnee[0].split(",")
	tab=[]
	for a in donnee:
		tab.append(a)
	tab_donnee=[]
	tab_attr=[]	
	for b in tab:
		c = b.split("=")
		tab_attr.append(c[0])
		tab_donnee.append(c[1])
	return tab_attr,tab_donnee

#Commande getjsondata
def getjsondata(tab):
	attr = []
	donnee = []
	for chaine in tab:
		for cle in chaine.keys():
			if cle in attr:
				pass
			else:
				attr.append(cle)
		for val in chaine.values():
			donnee.append(val)
	print(attr)
	print(donnee)
	return attr,donnee

#Commande describe
def describe(table,bd):
	path = table+".json"
	
	if os.path.exists(bd+"/"+path):
		with open(bd+"/"+path,"a+") as f:
			f.seek(0,0)
			k=f.read()
		r="[\n"+k+"\n]"
		m=simplejson.loads(r)
		ch = ""
		attr,donnee = getjsondata(m)
		for chaine in attr:
			ch+="#"+chaine
		return ch

#Commande showtable
def showtable(base):
	dossier = os.listdir(base)
	ch = ""
	for chaine in dossier:
		ch+="#"+chaine
	return ch	 

#Commandes auxiliaires
def TriNumber(number):
    return number.sort()
def TriNumberinverse():
    return number.sort(reverse=True)
    
def ChaineOrdreCroissante (chaine):
	ch = sorted(chaine)
	return ch
def ChaineOrdreDecroissant(chaine):
	ch = sorted (chaine,reverse=True)
	return ch
def cut(chaine,key):
	return chaine.split(key)


#Fonctions ajout utilisateur/suppression utilisateur
def adduser(user,password):
	dico=dict()
	dic=dict()
	with open("users.json",'r') as f :
		dico=simplejson.load(f)
	dic["user"] = user
	dic["password"] = password
	dico["users"].append(dic)
	with open("users.json",'w') as g :	
		simplejson.dump(dico,g,indent=4)
	f.close()

def deluser(user):
	dico=dict()
	with open("userssave.json",'r') as f :
		dico=simplejson.load(f)
	for x in list(dico):
		if user==x:
			del dico[user]
			with open("userssave.json",'w') as g :	
				simplejson.dump(dico,g,indent=4)



