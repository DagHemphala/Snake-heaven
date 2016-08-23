import socket, select, pickle
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 9000))
server.listen(5)

clients = []
playerlist = []
snake_pos_x = []
snake_pos_y = []
score = []

hit = False
while True:
    Connections, wlist, xlist = select.select([server], [], [], 0.05)

    for Connection in Connections:
        client, Informations = Connection.accept()
        clients.append(client)

    clientsList = []
    try:
        clientsList, wlist, xlist = select.select(clients, [], [], 0.05)
    except select.error:
        pass
    else:
        for clientInList in clientsList:
            data = clientInList.recv(1024)
            data = pickle.loads(data)
            data = data.split(b'=')
            
            if data[0] == b"playername":                
                playerlist.append(data[1])
                score.append(b'0')
                print(str(data[1].decode("utf-8")) + " Connected!")
                data = b'Welcome ' + data[1]
                data = pickle.dumps(data)
                clientInList.send(data)
                if len(playerlist) == 1:
                    print("host")
                    data_host = b"1"
                    data_host = pickle.dumps(data_host)
                    clientInList.send(data_host)
                else:
                    data_host = pickle.dumps(bytes(str(len(playerlist)), "utf-8"))
                    clientInList.send(data_host)
                    
            if data[0] == b'connected':
                data = b'playername=',playerlist
                data = pickle.dumps(data)
                clientInList.send(data)
            elif data[0] == b'startgame':
                print("Starting Game!")
                for clientInList2 in clientsList:
                    data = b'startgame'
                    data = pickle.dumps(data)
                    clientInList2.send(data)
        
            #elif data[0] == b'snake_pos':
            #    snake_pos_x = data[0]
            #    snake_pos_y = data[0]
            #    for clientInList2 in clientsList:
            #        data = b'startgame'
            #        data = pickle.dumps(data)
            #        clientInList2.send(data)

            if data[0] == b'generate_pos':
                apple_pos_x = random.randrange(0, 960-15)
                apple_pos_y = random.randrange(0, 640-15)
                data = pickle.dumps(b"test")
                clientInList2.send(data)
                hit = True
            
            
            if data[0] == b'hitapple':
                if hit:
                    print("hit")
                    
                    for clientInList2 in clientsList:
                        
                        data = b'applepos' ,apple_pos_x, apple_pos_y
                        data = pickle.dumps(data)
                        clientInList2.send(data)
                else:
                    data = pickle.dumps(b"test")
                    clientInList2.send(data)

            elif data[0] == b'score':
                i = int(data[2].decode("utf-8"))-1
                score[i] = data[1]
                for clientInList2 in clientsList:
                    data = b'score' , score
                    data = pickle.dumps(data)
                    clientInList2.send(data)


            
                
                    
            
            
                
        

clientInList.close()
server.close()
