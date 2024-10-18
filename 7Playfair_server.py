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

# Function to find the position of a letter in the matrix
def find_position(letter, matrix):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == letter:
                return row, col
    return None

# Function to decrypt a pair of letters (digraph)
def decrypt_digraph(digraph, matrix):
    row1, col1 = find_position(digraph[0], matrix)
    row2, col2 = find_position(digraph[1], matrix)

    if row1 == row2:
        # Same row, shift left
        return matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
    elif col1 == col2:
        # Same column, shift up
        return matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
    else:
        # Rectangle swap
        return matrix[row1][col2] + matrix[row2][col1]

# Function to decrypt the entire message using Playfair Cipher
def decrypt_message(ciphertext, key):
    matrix = generate_key_matrix(key)
    plaintext = ""
    # Process each digraph (2 characters at a time)
    for i in range(0, len(ciphertext), 2):
        digraph = ciphertext[i:i+2]
        plaintext += decrypt_digraph(digraph, matrix)
    return plaintext

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

# Define a key for the Playfair cipher
cipher_key = "KEYWORD"  # Same key used by the client

while True:
    data, addr = s.recvfrom(1024)
    s_name = data.decode()
    print(s_name, "has connected to the chat room")
    s.sendto(name.encode(), addr)

    while True:
        message, addr = s.recvfrom(1024)
        message = message.decode()

        # Decrypt the received ciphertext
        decrypted_message = decrypt_message(message, cipher_key)

        # Display the received ciphertext and the decrypted message
        print(f"{s_name} (ciphertext): {message}")
        print(f"{s_name} (plaintext): {decrypted_message}")

        if message == "[e]":
            print("\n")
            break

        reply = input("Me : ")
        s.sendto(reply.encode(), addr)
        if reply == "[e]":
            s.close()
            break
