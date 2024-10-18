import socket

# Function to decrypt a Rail Fence Cipher message
def rail_fence_decrypt(ciphertext, key):
    # Create an empty rail matrix
    rail = [['\n' for _ in range(len(ciphertext))] for _ in range(key)]
    
    # Determine the positions to mark in the rail matrix
    dir_down = None
    row, col = 0, 0
    
    # Mark the positions where characters will be placed
    for i in range(len(ciphertext)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
        
        # Place a marker
        rail[row][col] = '*'
        col += 1
        
        # Move to the next row (up or down)
        if dir_down:
            row += 1
        else:
            row -= 1

    # Now fill the rail matrix with ciphertext characters
    index = 0
    for i in range(key):
        for j in range(len(ciphertext)):
            if rail[i][j] == '*' and index < len(ciphertext):
                rail[i][j] = ciphertext[index]
                index += 1
    
    # Read the matrix in a zigzag manner to reconstruct the plaintext
    result = []
    row, col = 0, 0
    for i in range(len(ciphertext)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
        
        # Extract the character and add it to the result
        if rail[row][col] != '\n':
            result.append(rail[row][col])
            col += 1
        
        # Move up or down the rails
        if dir_down:
            row += 1
        else:
            row -= 1
    
    return ''.join(result)

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

# Define a key for the Rail Fence cipher (same key as the client)
cipher_key = 3  # Number of rails for the decryption

while True:
    data, addr = s.recvfrom(1024)
    s_name = data.decode()
    print(s_name, "has connected to the chat room")
    s.sendto(name.encode(), addr)

    while True:
        message, addr = s.recvfrom(1024)
        message = message.decode()

        # Decrypt the received ciphertext
        decrypted_message = rail_fence_decrypt(message, cipher_key)

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
