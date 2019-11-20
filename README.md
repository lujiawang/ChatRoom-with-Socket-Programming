# ChatRoom-with-Socket-Programming
''''''''''''''''''''''''''''''''''''''''''''''''''''''
Topic: Chat Room
Author: Lujia Wang
Date: 11/18/2019

''''''''''''''''''''''''''''''''''''''''''''''''''''''

In this lab, I create a simple Chat Room which could display instant messages


server.py
	To run the server, simple type "python server.py" in cmd
	It will first prompt the port number to listen and print out the current IP address
	Then the server will be waiting to be connected

	The server side has 6 simple command after each message one of the client sent, which are:
		"USER" - the current talking user name
		"MESSAGE" - the most recent displayed message
		"COUNT" - number of users in the chat room
		"ADDR" - the current user's IP address
		"PORT" - the current user's port number
		"CLOSE" - shutdown the program

client.py
	To run client, type "python client.py" in cmd; it can be run multiple times for multiple clients to enter the chat room
	There will be window pop up asking for server's IP address, port number, user name, and the chat room's password 
		The password is invisible and can be modified through code
	After connect, another GUI will pop up contains two parts
		The box on the top ask for enter message with a submit button
		The area show instant messages
