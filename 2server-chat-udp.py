# Joseph 103



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

        reply = input("Me : ")
        s.sendto(reply.encode(), addr)
        if reply == "[e]":
            s.close()
            break



OUTPUT


SERVER:
Welcome to Chat Room

Initialising....

csadmin-OptiPlex-3020 ( 127.0.1.1 )

Enter your name: Joseph

Waiting for incoming connections...

Joshua has connected to the chat room
Joshua : Hi
Me : Hello
Joshua : How are you right now?
Me : I am doing well



CLIENT:

Welcome to Chat Room

Initialising....

csadmin-OptiPlex-3020 ( 127.0.1.1 )

Enter server address: 127.0.1.1

Enter your name: Joshua

Trying to connect to  127.0.1.1 ( 1234 )

Joseph has joined the chat room
Enter [e] to exit chat room

Me : Hi
Joseph : Hello
Me : How are you right now?
Joseph : I am doing well
Me : 
