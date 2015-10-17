import socket
import threading
import time
import winsound
from msvcrt import getch
import os
clear = lambda: os.system('cls')

def getTerminalSize():
	import os
	env = os.environ
	def ioctl_GWINSZ(fd):
		try:
			import fcntl, termios, struct, os
			cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,
		'1234'))
		except:
			return
		return cr
	cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
	if not cr:
		try:
			fd = os.open(os.ctermid(), os.O_RDONLY)
			cr = ioctl_GWINSZ(fd)
			os.close(fd)
		except:
			pass
	if not cr:
		cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

	### Use get(key[, default]) instead of a try/catch
	#try:
	#    cr = (env['LINES'], env['COLUMNS'])
	#except:
	#    cr = (25, 80)
	return int(cr[1]), int(cr[0])

width, height = getTerminalSize()
bar = ""
for x in range(width - 16):
	bar += "="

typing = ""
def getmessage():
	global typing
	typing = ""
	global bar
	global chatlog
	while True:
		print(bar)
		print(">>:", typing)
		data = getch().decode()
		if data == "\r":
			return typing
		elif data == "\x08":
			remessage = ""
			c = 0
			length = len(typing) - 1
			for x in typing:
				if c == length:
					break
				else:
					c += 1
					remessage += x
			typing = remessage
		else:
			typing += data
		clear()
		for x in chatlog:
			print(x)

def listen(Client):
	global bar
	global chatlog
	while True:
		data = Client.recv(1024).decode()
		winsound.Beep(1500, 100)
		chatlog.append(data)
		clear()
		for x in chatlog:
			print(x)
		print(bar)
		print(">>:", typing)

Client = socket.socket()
ip = input("Server IP:")
port = 5000
nick = input("Nick:")
nick = nick.encode()
chatlog = []
Client.connect((ip, port))
Client.send(nick)
time.sleep(0.1)
listening = threading.Thread(target=listen, args=(Client,))
listening.start()
while True:
	message = getmessage()
	message = message.encode()
	Client.send(message)
