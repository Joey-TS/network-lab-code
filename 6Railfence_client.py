import socket

# Function to encrypt a message using the Rail Fence Cipher
def rail_fence_encrypt(message, key):
    # Create an empty list for the rails
    rail = [['\n' for _ in range(len(message))] for _ in range(key)]
    
    # Initialize variables for direction and row
    dir_down = False
    row, col = 0, 0
    
    # Fill the rail matrix
    for char in message:
        # Change direction when reaching the top or bottom rail
        if row == 0 or row == key - 1:
            dir_down = not dir_down
        
        # Put the character in the matrix
        rail[row][col] = char
        col += 1
        
        # Move up or down the rails
        if dir_down:
            row += 1
        else:
            row -= 1
    
    # Extract the characters row-wise to form the ciphertext
    encrypted_message = []
    for i in range(key):
        for j in range(len(message)):
            if rail[i][j] != '\n':
                encrypted_message.append(rail[i][j])
    
    return ''.join(encrypted_message)

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

# Define a key for the Rail Fence cipher
cipher_key = 3  # Number of rails for the encryption

while True:
    message = input("Me : ")
    if message == "[e]":
        s.sendto(message.encode(), (host, port))
        print("\n")
        break

    # Encrypt the message using the Rail Fence cipher
    encrypted_message = rail_fence_encrypt(message, cipher_key)
    s.sendto(encrypted_message.encode(), (host, port))
    
    data, addr = s.recvfrom(1024)
    print(s_name, ":", data.decode())

    if data.decode() == "[e]":
        print("\n")
        break

s.close()
