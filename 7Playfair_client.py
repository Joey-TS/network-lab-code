import socket

# Function to generate the Playfair cipher key matrix
def generate_key_matrix(key):
    key = key.replace("J", "I")  # Standard Playfair Cipher replaces J with I
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    matrix = []
    used_chars = set()

    # Add key to the matrix, skipping duplicate letters
    for char in key.upper():
        if char not in used_chars and char in alphabet:
            matrix.append(char)
            used_chars.add(char)

    # Add remaining letters of the alphabet
    for char in alphabet:
        if char not in used_chars:
            matrix.append(char)

    # Reshape into 5x5 matrix
    return [matrix[i:i+5] for i in range(0, len(matrix), 5)]

# Function to split message into digraphs
def split_into_digraphs(message):
    digraphs = []
    message = message.replace(" ", "").upper().replace("J", "I")
    i = 0
    while i < len(message):
        digraph = message[i]
        if i + 1 < len(message) and message[i] != message[i + 1]:
            digraph += message[i + 1]
            i += 2
        else:
            digraph += 'X'  # Padding with 'X' for repeated letters
            i += 1
        digraphs.append(digraph)
    return digraphs

# Function to find the position of a letter in the matrix
def find_position(letter, matrix):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == letter:
                return row, col
    return None

# Function to encrypt a pair of letters (digraph)
def encrypt_digraph(digraph, matrix):
    row1, col1 = find_position(digraph[0], matrix)
    row2, col2 = find_position(digraph[1], matrix)

    if row1 == row2:
        # Same row, shift right
        return matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
    elif col1 == col2:
        # Same column, shift down
        return matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
    else:
        # Rectangle swap
        return matrix[row1][col2] + matrix[row2][col1]

# Function to encrypt the entire message using Playfair Cipher
def encrypt_message(message, key):
    matrix = generate_key_matrix(key)
    digraphs = split_into_digraphs(message)
    ciphertext = ""
    for digraph in digraphs:
        ciphertext += encrypt_digraph(digraph, matrix)
    return ciphertext

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

# Define a key for the Playfair cipher
cipher_key = "KEYWORD"  # You can modify this key

while True:
    message = input("Me : ")
    if message == "[e]":
        s.sendto(message.encode(), (host, port))
        print("\n")
        break

    # Encrypt the message before sending
    encrypted_message = encrypt_message(message, cipher_key)
    s.sendto(encrypted_message.encode(), (host, port))
    
    data, addr = s.recvfrom(1024)
    print(s_name, ":", data.decode())

    if data.decode() == "[e]":
        print("\n")
        break

s.close()
