import socket

# Define host and port
HOST = '127.0.0.53'  # Localhost
PORT = 1024        # Port to listen on (non-privileged ports are > 1023)

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # Bind the socket to the address and port
    server_socket.bind((HOST, PORT))
    
    # Listen for incoming connections
    server_socket.listen()
    print(f"Server is listening on {HOST}:{PORT}")
    
    # Accept connections from client
    client_socket, client_address = server_socket.accept()
    
    with client_socket:
        print(f"Connected by {client_address}")
        
        while True:
            # Receive data from client
            data = client_socket.recv(1024)
            if not data:
                break  # No more data from client, exit loop
            
            # Process received data (here, just printing it)
            print(f"Received from client: {data.decode()}")
            
            # Send response back to client (echo)
            client_socket.sendall(data)
