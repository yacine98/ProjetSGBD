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
        r = self.clientsocket.recv(100000)
        info_connect = r.decode()
        info_connect = kyasql.space(info_connect)     
        requete = kyasql.cut(info_connect,"#")   
        if requete[0].upper() == "KYASQL":
            if requete[1].upper() == "-U":
                user = requete[2]
                if requete[3].upper() == "-P": 
                    password = requete[4]
                    auth = kyasql.auth(user,password)
                    self.clientsocket.send(auth.encode())
        b=auth
        if b == "1":
            while True:
                r = self.clientsocket.recv(100000)
                chaine = r.decode()
                chaine = kyasql.space(chaine)
                #print(chaine)
                requete = kyasql.cut(chaine,"#")
                #print(requete)
                if requete[0].upper() == "CREATE":
                    create=kyasql.create(requete[2],requete[1],base)
                    self.clientsocket.send(create.encode())    
                    #print("ok")      
                    #if requete[1].upper() == "Table" or requete[1] == "U":
                    #   pass
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
                if requete[0].upper() == "UPDATE":
                    pass
                if requete[0].upper() == "DELETE":
                    pass
                if requete[0].upper() == "SELECT":
                    if base != ".":
                        select = kyasql.select(requete[1],requete[3],base)
                        self.clientsocket.send(select.encode()) 
                    else:
                        select = "veuiller selectionner une base"
                        self.clientsocket.send(select.encode()) 
                if requete[0].upper() == "ADDUSER":
                    pass
                if requete[0].upper() == "DELUSER":
                    pass
                if requete[0].upper() == "QUIT":
                    pass
                if requete[0].upper() == "START":
                    pass
                if requete[0].upper() == "COMMIT":
                    pass
                if requete[0].upper() == "ROLLBACK":
                    pass
                if requete[0].upper() == "USE":
                    base = requete[1]
                    use = base+" now selected";
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
