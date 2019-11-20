import socket
import time
import select
import threading
import os

'''
Topic: Chat Room
Author: Lujia Wang
Date: 11/18/2019

'''


HEADERSIZE = 10
PORT = int(input("Enter the port number: "))

#Create socket
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #ipv6 and TCP
server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP = socket.gethostbyname(socket.gethostname())
print("The IP address is: ", IP)


server_sock.bind((IP, PORT))
server_sock.listen() 


sockets_list = [server_sock]

clients = {}


def receive(client_sock):
	try:
		message_header = client_sock.recv(HEADERSIZE)

		if not len(message_header):
			return false

		message_length = int(message_header.decode("utf-8").strip())
		return {"header": message_header, "data": client_sock.recv(message_length)}

	except:
		return False
			


commands = ["USER","MESSAGE", "COUNT", "ADDR", "PORT", "CLOSE"]
lcommands = [commands[0].casefold(), commands[1].casefold(),commands[2].casefold(),commands[3].casefold(), commands[4].casefold(), commands[5].casefold()]

cuser = ""
cmsg = ""
caddr = ""
cport = 0


def handleCommand(command):
	global server_sock
	if command == commands[0]:
		print("current user: ", cuser)
		handleCommand(input("\nCommand:"))
	elif command == commands[1]:
		print("current message: ", cmsg)
		handleCommand(input("\nCommand:"))
	elif command == commands[2]:
		print("number of user:", len(clients))
		handleCommand(input("\nCommand:"))
	elif command == commands[3]:
		print("current user's address: ",caddr)		
		handleCommand(input("\nCommand:"))
	elif command == commands[4]:
		print("current user's port: ", cport)
		handleCommand(input("\nCommand:"))
	elif command == commands[5]:
		os._exit(0)
	elif command.casefold() in  lcommands:
		print("UPPER CASE COMMAND: ", command)
		print("\t", command.upper())
		handleCommand(input("\nCommand:"))
	else:
		print("Invalid command: ", command)
		print("Commands: ")
		for cmd in commands:
			print("\t", cmd)
		handleCommand(input("\nCommand:"))


def recvSocket():
	global cuser, cmsg, caddr, cport
	while True:
		read_socks, _, exception_socks = select.select(sockets_list, [], sockets_list)


		for notified_sock in read_socks:
			if notified_sock == server_sock:
				client_sock, client_address = server_sock.accept()

				#Server interact with client.py
				user = receive(client_sock)
				if user is False:
					continue

				sockets_list.append(client_sock)

				clients[client_sock] = user
				#end

				t = time.asctime(time.localtime(time.time()))
				print(f"\nMy server at the time <{t}> is listening from address {client_address[0]}, Port {client_address[1]}, username {user['data'].decode('utf-8')}",)
				caddr = client_address[0]
				cport = client_address[1]
		
			else:
				message = receive(notified_sock)
				if message is False:
					print(f"Closed connection from {clients[notified_sock]['data'].decode('utf-8')}")
					sockets_list.remove(notified_sock)
					del clients[notified_sock]
					continue
				
				user = clients[notified_sock]
				#print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")
				cuser = user['data'].decode('utf-8')
				cmsg = message['data'].decode('utf-8')

				# message information
				for client_sock in clients:
					if client_sock != notified_sock:
						client_sock.send(user['header'] + user['data'] + message['header'] + message['data'])	
						

		for notified_sock in exception_socks:
			sockets_list.remove(notified_sock)
			del clients[notified_sock]


socket_thread = threading.Thread(target = recvSocket)
socket_thread.start()

command_thread = threading.Thread(target = handleCommand, args = (input("Command:"),))
command_thread.start()

