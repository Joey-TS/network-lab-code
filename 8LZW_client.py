import socket

def compress(uncompressed):
    """Compress a string to a list of output symbols."""
    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}

    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    if w:
        result.append(dictionary[w])
    return result

def list_to_string(compressed_list):
    return ','.join(map(str, compressed_list))

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
    if message == "[e]":
        s.sendto(message.encode(), (host, port))
        print("\n")
        break

    # Compress the message before sending
    compressed_message = compress(message)
    compressed_message_str = list_to_string(compressed_message)
    s.sendto(compressed_message_str.encode(), (host, port))
    
    # Receive decompressed message from server
    decompressed_message, addr = s.recvfrom(1024)
    print(s_name, " (Decompressed):", decompressed_message.decode())

    if decompressed_message.decode() == "[e]":
        print("\n")
        break

s.close()

