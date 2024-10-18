# Joseph 103 evenodd



import socket

print("\nWelcome to Chat Room\n")
print("Initialising....\n")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = socket.gethostname()
ip = socket.gethostbyname(host)
port = 1234
s.bind((host, port))
print(host, "(", ip, ")\n")
name = input("Enter your name: ")

print("\nWaiting for incoming connections...\n")

while True:
    data, addr = s.recvfrom(1024)
    s_name = data.decode()
    print(s_name, "has connected to the chat room")
    s.sendto(name.encode(), addr)

    while True:
        message, addr = s.recvfrom(1024)
        message = message.decode()
        print(s_name, ":", message)
        if message == "[e]":
            print("\n")
            break
        elif (int(message)%2==0):
        	reply="The number is even\n"
        	print("The number has been processed as even\n")
        else:
        	reply="The number is odd\n"
        	print("The number has been processed as odd\n")

        s.sendto(reply.encode(), addr)
        if reply == "[e]":
            s.close()
            break




OUTPUT:

SERVER:
Welcome to Chat Room

Initialising....

csadmin-OptiPlex-3020 ( 127.0.1.1 )

Enter your name: Joseph

Waiting for incoming connections...

Joshua has connected to the chat room
Joshua : 1
The number has been processed as odd

Joshua : 2
The number has been processed as even

Joshua : 223
The number has been processed as odd

Joshua : 554
The number has been processed as even


CLIENT:
Welcome to Chat Room

Initialising....

csadmin-OptiPlex-3020 ( 127.0.1.1 )

Enter server address: 127.0.1.1

Enter your name: Joshua

Trying to connect to  csadmin-OptiPlex-3020 ( 1234 )

Joseph has joined the chat room
Enter [e] to exit chat room

Enter nubers to check if even or odd


Me : 1 
Joseph : The number is odd

Me : 2
Joseph : The number is even

Me : 223
Joseph : The number is odd

Me : 554
Joseph : The number is even


