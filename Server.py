#server
import socket
import threading

def sendall(data):
	global clients
	for x in clients:
		x.send(data)

def client(conn, addr, nick,):
	global clients
	while True:
		try:
			data = conn.recv(1024).decode()
		except socket.error as e:
			print(e)
			nick += " Disconnected"
			nick = nick.encode()
			sendall(nick)
			clients.remove(conn)
			break
		data = nick + " || " + data
		data = data.encode()
		sendall(data)
#-----------------------------
clients = []
Server = socket.socket()
ip = "192.168.1.254"
port = 5000
Server.bind((ip, port))
#-----------------------------
print("Server Running!")
print("IP:", ip)
print("Port:", port)
while True:
	Server.listen(5)
	conn, addr = Server.accept()
	clients.append(conn)
	nick = conn.recv(1024).decode()
	print(nick, "Connected!")
	data = nick + " Connected!"
	data = data.encode()
	sendall(data)
	c = threading.Thread(target=client,args=(conn, addr, nick))
	c.start()




