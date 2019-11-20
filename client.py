import socket
import select
import errno
import sys
import tkinter as tk 

'''
Topic: Chat Room
Author: Lujia Wang
Date: 11/18/2019

'''


def call_result():  
    global IP, PORT, usernamestr, password
    IP = ip.get()
    PORT = int(port.get())
    usernamestr = un.get()
    if pw.get() != "a":
    	label = tk.Label(root, text = "Incorrect password").grid(row=4, column=3)
    else:
    	password = pw.get()
    	root.destroy()	
    return


def call_submit():
	global message, message_header, entry
	message = msg.get().encode("utf-8")
	#my message
	Chatlog.insert(tk.END, usernamestr +" > "+ message.decode("utf-8")+"\n")

	if message:
		message_header = f"{len(message):<{HEADERSIZE}}".encode("utf-8")
		client_sock.send(message_header + message)

	entry.delete(0, tk.END)


def receiveMsg():
	global client_sock, username_header, username_len, username, message_header, message_len, message
	try:
		while True:
			#receive
			username_header = client_sock.recv(HEADERSIZE)
			print("recv")
			if not len(username_header):
				print("connection closed by the server")
				sys.exit()

			username_len = int(username_header.decode("utf-8").strip())
			username = client_sock.recv(username_len).decode("utf-8")

			message_header = client_sock.recv(HEADERSIZE)
			message_len = int(message_header.decode("utf-8".strip()))
			message = client_sock.recv(message_len).decode("utf-8")

			#others' message
			Chatlog.insert(tk.END, username+" > "+message+"\n")


	except IOError as e:
		if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
			print('IO Error',str(e))
			sys.exit()

	except Exception as e:
		print('Exception Error', str(e))
		sys.exit()
	#print("success")
	main.after(500, receiveMsg) # refreshing every second


#connection   
root = tk.Tk()  
root.geometry('400x200')  
root.title('Connection')  

ip = tk.StringVar()  
port = tk.StringVar()  
un = tk.StringVar()
pw = tk.StringVar()
  
labelNum1 = tk.Label(root, text="Server IP").grid(row=1, column=0)  
labelNum2 = tk.Label(root, text="Server port").grid(row=2, column=0)  
labelNum3 = tk.Label(root, text="Username").grid(row=3, column=0)  
labelNum4 = tk.Label(root, text="Password").grid(row=4, column=0)  
  
entryNum1 = tk.Entry(root, textvariable=ip).grid(row=1, column=2)  
entryNum2 = tk.Entry(root, textvariable=port).grid(row=2, column=2)  
entryNum3 = tk.Entry(root, textvariable=un).grid(row=3, column=2) 
entryNum4 = tk.Entry(root, textvariable=pw, show="*").grid(row=4, column=2) 
 
buttonCal = tk.Button(root, text="Submit", command=call_result).grid(row=5, column=0)  
  
root.mainloop()  


#connection

HEADERSIZE = 10

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect((IP, PORT))
client_sock.setblocking(False)

username = usernamestr.encode('utf-8')

username_header = f"{len(username):<{HEADERSIZE}}".encode("utf-8")
client_sock.send(username_header + username)


main = tk.Tk()
main.geometry('400x800')
main.title("Chat Room")

msg = tk.StringVar()
label = tk.Label(main, text=usernamestr+">")
entry = tk.Entry(main, textvariable=msg)
buttonSub = tk.Button(main, text="Submit", command=call_submit)

Chatlog = tk.Text(main, font="Arial")

label.place(x=6,y=50)
entry.place(x=30,y=50,width=300)
buttonSub.place(x=350,y=50)
Chatlog.place(x=6,y=150)


main.after(0,receiveMsg)
main.mainloop()
