# Joseph 103 multiserver



import socket
import threading
import sys

def receive_messages(client_socket):
    """Handles receiving messages from the server."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"\n{message}\n> ", end="")
            else:
                print("Disconnected from server")
                client_socket.close()
                break
        except:
            print("Error receiving message")
            client_socket.close()
            break

def send_messages(client_socket):
    """Handles sending messages to the server."""
    while True:
        try:
            message = input("Me: ")
            if message:
                client_socket.send(message.encode('utf-8'))
        except:
            print("Error sending message")
            client_socket.close()
            break

def start_client():
    """Sets up the client to connect to the server and handle messaging."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))  # Connect to the server on localhost
    
    print("Connected to the server. You can start chatting now!")

    # Start threads to handle sending and receiving messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()

if __name__ == "__main__":
    start_client()

