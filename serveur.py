# coding: utf-8 
import socket
import threading
import kyasql
import os

class ClientThread(threading.Thread):
    def __init__(self, ip, port, clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port, ))
    def run(self):
        base="."    
        print("Connexion de %s %s" % (self.ip, self.port, ))
        r1 = self.clientsocket.recv(100000)
        r=r1.decode()
        if r == "1":
            while True:
                r = self.clientsocket.recv(100000)
                chaine = r.decode()
                chaine = kyasql.space(chaine)
                
                requete = kyasql.cut(chaine,"#")
                
                if requete[0].upper() == "CREATE":
                    create=kyasql.create(requete[2],requete[1],base)
                    self.clientsocket.send(create.encode())    
                if requete[0].upper() == "DROP":
                    drop = kyasql.drop(requete[1])
                    self.clientsocket.send(drop.encode())    
                if requete[0].upper() == "ALTER":
                    pass
                if requete[0].upper() == "INSERT":
                    if base != ".":
                        insert=kyasql.insert(requete[2],requete[3],base)
                        self.clientsocket.send(insert.encode()) 
                    else:
                        insert = "veuillez selectionner une base"
                        self.clientsocket.send(insert.encode())
                if requete[0].upper() == "ADDUSER":
                    kyasql.adduser(requete[1],requete[2])
                    resultat="Utilisateur créé"
                    self.clientsocket.send(resultat.encode()) 
                if requete[0].upper() == "SELECT":
                    if base != ".":
                        select = kyasql.select(requete[1],requete[3],base)
                        self.clientsocket.send(select.encode()) 
                    else:
                        select = "veuiller selectionner une base"
                        self.clientsocket.send(select.encode()) 
                
                if requete[0].upper() == "USE":
                    base = requete[1]
                    if os.path.exists(base):
                        use = base+" now selected";
                    else:
                        use = base+" don't exist";
                    self.clientsocket.send(use.encode()) 
                if requete[0].upper() == "DESCRIBE":
                    if base != ".":
                        desc = kyasql.describe(requete[1],base)
                        self.clientsocket.send(desc.encode()) 
                    else:
                        select = "veuiller selectionner une base"
                        self.clientsocket.send(select.encode()) 
                if requete[0].upper() == "SHOW":

                    if requete[1].upper() == "DATABASES":
                        pass
                    if requete[1].upper() == "TABLES":
                        if base != ".":
                            show = kyasql.showtable(base)
                            self.clientsocket.send(show.encode()) 
                        else:
                            show = "veuiller selectionner une base"
                            self.clientsocket.send(show.encode()) 
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("",8888))

while True:
    tcpsock.listen(10)
    print( "En écoute...")
    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()
