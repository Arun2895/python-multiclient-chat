# server.py
import socket
import threading

# --- Configuration ---
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 55555        # Port to listen on (non-privileged ports are > 1023)

# --- Global Lists ---
clients = []
nicknames = []

# --- Function Definitions ---

def broadcast(message):
    """Sends a message to all connected clients."""
    for client in clients:
        try:
            client.send(message)
        except:
            # Handle broken connections
            remove_client(client)

def handle_client(client):
    """Handles a single client connection in its own thread."""
    while True:
        try:
            # Receive message from client
            message = client.recv(1024)
            if not message:
                remove_client(client)
                break
            
            # Broadcast the received message
            broadcast(message)
            
        except (ConnectionResetError, ConnectionAbortedError):
            remove_client(client)
            break
        except Exception as e:
            print(f"An error occurred with client {client}: {e}")
            remove_client(client)
            break

def remove_client(client):
    """Removes a client from the global lists."""
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        client.close()
        
        nickname = nicknames[index]
        nicknames.remove(nickname)
        
        broadcast(f'{nickname} has left the chat.'.encode('utf-8'))
        print(f'{nickname} has disconnected.')

def receive_connections():
    """Main function to set up the server and accept new connections."""
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    
    print(f"Server is listening on {HOST}:{PORT}...")
    
    while True:
        try:
            client, address = server.accept()
            print(f"New connection from {str(address)}")
            
            # Ask the newly connected client for their nickname
            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            
            # Add the new client and their nickname
            nicknames.append(nickname)
            clients.append(client)
            
            print(f"Nickname for {address} is {nickname}")
            broadcast(f"{nickname} has joined the chat!".encode('utf-8'))
            
            client.send("Connected to the server!".encode('utf-8'))
            
            # Start the client handling thread
            thread = threading.Thread(target=handle_client, args=(client,))
            thread.start()
            
        except Exception as e:
            print(f"An error occurred while accepting connections: {e}")

# --- Main Execution ---
if __name__ == "__main__":
    receive_connections()
