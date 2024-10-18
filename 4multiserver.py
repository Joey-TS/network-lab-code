# Joseph 103 multiserver



import socket
import threading

# List to keep track of connected clients
clients = []

def handle_client(client_socket):
    """Handles communication with a single client."""
    while True:
        try:
            # Receive message from the client
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                # Broadcast message to all other clients
                broadcast(message, client_socket)
            else:
                # Remove client if the connection is closed
                clients.remove(client_socket)
                client_socket.close()
                break
        except:
            # Handle any exceptions
            clients.remove(client_socket)
            client_socket.close()
            break

def broadcast(message, client_socket):
    """Broadcasts a message to all clients except the sender."""
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                # Handle exception if sending fails
                clients.remove(client)
                client.close()

def start_server():
    """Sets up the server to accept incoming client connections."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))  # Bind to port 12345
    server_socket.listen(5)
    print("Server is listening on port 12345...")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"New connection from {addr}")
        clients.append(client_socket)
        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_server()




OUTPUT

SERVER:

Server is listening on port 12345...
New connection from ('127.0.0.1', 59740)
New connection from ('127.0.0.1', 44908)


CLIENT 1:
Connected to the server. You can start chatting now!
Me: Hi
Me: Hello
> Where are you right now?
Me: I am at my house
> 


Client 2:
Connected to the server. You can start chatting now!
Me: Hi
> Hello
Me: Where are you right now?
> I am at my house
Me: 


