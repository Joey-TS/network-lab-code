# Joseph 103



import socket

print("\nWelcome to Chat Room\n")
print("Initialising....\n")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
shost = socket.gethostname()
ip = socket.gethostbyname(shost)
print(shost, "(", ip, ")\n")

host = input("Enter server address: ")
port = 1234
name = input("\nEnter your name: ")
print("\nTrying to connect to ", host, "(", port, ")\n")

s.sendto(name.encode(), (host, port))
s_name, addr = s.recvfrom(1024)
s_name = s_name.decode()
print(s_name, "has joined the chat room\nEnter [e] to exit chat room\n")

while True:
    message = input("Me : ")
    s.sendto(message.encode(), (host, port))
    if message == "[e]":
        print("\n")
        break

    data, addr = s.recvfrom(1024)
    print(s_name, ":", data.decode())

    if data.decode() == "[e]":
        print("\n")
        break

s.close()

