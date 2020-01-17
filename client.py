# coding: utf-8
import socket
import kyasql
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("", 8888))
check=True
authentifier = True
def verification(requete):
	maRequete = requete.split(" ")
	global check
	if len(maRequete)>=3:
		if maRequete[0]!="create" and maRequete[0]!="alter" and maRequete[0]!="use" and maRequete[0]!="drop" and maRequete[0]!="select" and maRequete[0]!="insert" and maRequete[0]!="update" and maRequete[0]!="show" and maRequete[0]!="describe" and maRequete[0]!="delete":
			print("Cette commande n'est pas reconnue par notre système")
			check=False
		elif maRequete[0] == "create" or maRequete[0]=="drop" or maRequete[0]=="alter":
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

	elif maRequete[0]!="show" and maRequete[0]!="describe" and maRequete[0]!="select" and maRequete[0]!="use":
		print("Requête invalide ou incomplète")
		check=False
chaine = input(">>") # utilisez raw_input() pour les anciennes versions python
maChaine = chaine.split(" ")

if len(maChaine) !=5:
	print("Requête d'authentification invalide ou incomplete")
	authentifier=False
elif maChaine[0]!="kyasql":
	print("Requête d'authentification invalide")
	authentifier=False
elif maChaine[1]!="-u" or maChaine[3]!="-p":
	print("La commande d'authentification ne respecte pas la syntaxe")
	authentifier=False

if authentifier==True:
	s.send(chaine.encode())
	auth = s.recv(100000)
else:
	auth.decode()=="0"

if auth.decode() == "1":
	while True:
		requete = input("kyasql>>")
		verification(requete)
		if check==True:
			s.send(requete.encode())
			ch = s.recv(100000)
			r = requete.split(" ")
			if r[0].upper() == "SELECT" :
				ch1 = ch.decode() 
			
				if ch1 == "Veuillez selectionner une base":
					print(ch1)
				else: 
					attr = ch1.split("|")[0]
					donnee = ch1.split("|")[1]
					attr1 = attr.split("#")
					donnee1 = donnee.split("#")
					attr2 = []
					donnee2 =[]
					for x in range(1,len(attr1)):
						attr2.append(attr1[x])
					for x in range(1,len(donnee1)):
						donnee2.append(donnee1[x])
				
					mod = 0
					for x in range(0,len(attr2)):
						print("{:^15s}".format("_______________"),end='')
					print('')
					for x in range(0,len(attr2)):
						print("{:^15s}".format(attr2[x]),end='')
						if x!= len(attr2) -1:
							print("|",end='')
					print('')
					for x in range(0,len(attr2)):
						print("{:^15s}".format("_______________"),end='')
					print('')
					while(mod != len(donnee2)):
						for x in range(mod,mod+len(attr2)):
							print("{:^15s}".format(donnee2[x]),end='')
							if x != mod+len(attr2) -1:
								print("|",end='')
						mod+=len(attr2)
						print('')
					for x in range(0,len(attr2)):
						print("{:^15s}".format("_______________"),end='')
					print('')	
			if r[0].upper() == "DESCRIBE":
				ch1 = ch.decode()
				if ch1 == "Veuiller selectionner une base":
					print(ch1)
				else:
					#print(ch1)
					attr2 = ch1.split("#")
					for x in range(1,len(attr2)):
						print("{:^15s}".format("_______________"),end='')
					print('')
					for x in range(1,len(attr2)):
						print("{:^15s}".format(attr2[x]),end='')
						if x!= len(attr2) -1:
							print("|",end='')
					print('')
					for x in range(1,len(attr2)):
						print("{:^15s}".format("_______________"),end='')
					print('')		
			if r[0].upper() == "SHOW":
				ch1 = ch.decode()
				print(ch1)
				if ch1 == "Veuillez selectionner une base":
					print(ch1)
				else:
					dossier = ch1.split("#")
					print("{:^15s}".format("________________"),end='')
					print("")

					print("{:^15s}".format("Tables"),end='')
					print("|")
					print("{:^15s}".format("________________"),end='')
					print('')
					for x in range(1,len(dossier)):
						print("{:^15s}|".format(dossier[x]))	
			else:
				print(ch.decode())
