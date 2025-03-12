import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            # Recibir mensaje del maestro / Receive message from master
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"\nMensaje del maestro / Message from master: {message}")
        except:
            break
    
    print("Conexión cerrada")
    print("Connection closed")
    client_socket.close()

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect(('localhost', 5555))
        print("Conectado al servidor")
        print("Connected to server")
        
        # Iniciar thread para recibir mensajes / Start thread for receiving messages
        receive_thread = threading.Thread(target=receive_messages, args=(client,))
        receive_thread.start()
        
        while True:
            # Enviar mensaje al maestro / Send message to master
            message = input("\nEscribe tu mensaje (write your message): ")
            if message.lower() == 'exit':
                break
            client.send(message.encode('utf-8'))
            
    except ConnectionRefusedError:
        print("No se pudo conectar al servidor. Asegúrate de que el servidor esté en ejecución.")
        print("Could not connect to server. Make sure the server is running.")
    except:
        print("Error en la conexión")
        print("Connection error")
    finally:
        client.close()

if __name__ == "__main__":
    start_client() 