import socket

def decompress(compressed):
    """Decompress a list of output ks to a string."""
    dict_size = 256
    dictionary = {i: chr(i) for i in range(dict_size)}

    w = result = dictionary[compressed.pop(0)]
    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result += entry

        dictionary[dict_size] = w + entry[0]
        dict_size += 1

        w = entry
    return result

def string_to_list(compressed_str):
    return list(map(int, compressed_str.split(',')))

def display_compressed(compressed):
    """Display the compressed message with normal letters for ASCII characters and numbers for others."""
    displayed_message = []
    for code in compressed:
        if code < 256:
            # Display the character for ASCII values
            displayed_message.append(chr(code))
        else:
            # Display the integer value for codes greater than 255
            displayed_message.append(str(code))
    return ' '.join(displayed_message)

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
        compressed_message_str = message.decode()

        # Convert received string back to list of integers
        compressed_message = string_to_list(compressed_message_str)

        # Decompress the received message
        decompressed_message = decompress(compressed_message)

        # Display compressed and decompressed message
        displayed_compressed = display_compressed(compressed_message)
        print(f"{s_name} (Compressed): {displayed_compressed}")
        print(f"{s_name} (Decompressed): {decompressed_message}")

        if compressed_message_str == "[e]":
            print("\n")
            break

        # Send the decompressed message back to the client
        s.sendto(decompressed_message.encode(), addr)

        reply = input("Me : ")
        s.sendto(reply.encode(), addr)
        if reply == "[e]":
            s.close()
            break
