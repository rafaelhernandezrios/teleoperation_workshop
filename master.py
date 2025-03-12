import socket
import threading

def handle_client(client_socket, address):
    print(f"Conexión establecida con {address}")
    print(f"Connection established with {address}")
    
    while True:
        try:
            # Recibir mensaje del estudiante / Receive message from student
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
                
            print(f"\nMensaje del estudiante / Message from student: {message}")
            
            # Enviar respuesta / Send response
            response = input("\nEscribe tu mensaje (write your message): ")
            client_socket.send(response.encode('utf-8'))
            
        except:
            break
    
    client_socket.close()
    print(f"Conexión cerrada con {address}")
    print(f"Connection closed with {address}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5555))
    server.listen(1)
    
    print("Servidor iniciado, esperando conexiones...")
    print("Server started, waiting for connections...")
    
    while True:
        client_socket, address = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
        client_handler.start()

if __name__ == "__main__":
    start_server() 