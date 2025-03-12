import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import ttk, messagebox
import socket
import threading

# Variables globales
arduino = None  # Objeto para la conexión serial
client_socket = None  # Socket del cliente conectado

# Función para detectar los puertos disponibles
def detectar_puertos():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

# Función para conectar con Arduino
def conectar_arduino():
    global arduino
    port = puerto_var.get()
    baudrate = baudrate_var.get()

    if port and baudrate:
        try:
            arduino = serial.Serial(port, int(baudrate), timeout=1)
            messagebox.showinfo("Conexión", f"Conectado a {port} con {baudrate} baud.")
        except serial.SerialException:
            messagebox.showerror("Error", "No se pudo conectar al puerto seleccionado.")
    else:
        messagebox.showwarning("Advertencia", "Seleccione un puerto y un baudrate.")

# Función para manejar mensajes del cliente
def handle_client(sock, address):
    global client_socket, arduino
    client_socket = sock
    print(f"Cliente conectado desde {address}")
    
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if not message:
                break
            
            # Mostrar el mensaje recibido en la interfaz
            mensaje_recibido.insert(tk.END, f"Mensaje recibido: {message}\n")
            mensaje_recibido.see(tk.END)
            
            # Si Arduino está conectado, enviar el mensaje
            if arduino and arduino.is_open:
                arduino.write((message + "\n").encode())
                mensaje_recibido.insert(tk.END, f"Enviado a Arduino: {message}\n")
                mensaje_recibido.see(tk.END)
            
        except:
            break
    
    sock.close()
    client_socket = None
    print(f"Cliente desconectado: {address}")

# Función para iniciar el servidor socket
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('192.168.0.47', 8000))
    server.listen(1)
    print("Servidor iniciado en puerto 5555")
    
    while True:
        client_sock, address = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_sock, address))
        client_handler.start()

# Crear ventana principal
root = tk.Tk()
root.title("Master - Control Arduino")
root.geometry("600x400")

# Frame para seleccionar puerto y baudrate
frame_conexion = ttk.LabelFrame(root, text="Conexión Serial")
frame_conexion.pack(pady=10, padx=10, fill="both")

# Puerto COM
ttk.Label(frame_conexion, text="Puerto:").grid(row=0, column=0, padx=5, pady=5)
puerto_var = tk.StringVar()
puerto_dropdown = ttk.Combobox(frame_conexion, textvariable=puerto_var, values=detectar_puertos(), state="readonly")
puerto_dropdown.grid(row=0, column=1, padx=5, pady=5)

# Botón para actualizar puertos
ttk.Button(frame_conexion, text="Actualizar", command=lambda: puerto_dropdown.config(values=detectar_puertos())).grid(row=0, column=2, padx=5, pady=5)

# Baudrate
ttk.Label(frame_conexion, text="Baudrate:").grid(row=1, column=0, padx=5, pady=5)
baudrate_var = tk.StringVar(value="9600")
baudrate_dropdown = ttk.Combobox(frame_conexion, textvariable=baudrate_var, values=["9600", "115200", "57600", "38400"], state="readonly")
baudrate_dropdown.grid(row=1, column=1, padx=5, pady=5)

# Botón para conectar
ttk.Button(frame_conexion, text="Conectar", command=conectar_arduino).grid(row=1, column=2, padx=5, pady=5)

# Frame para mostrar mensajes recibidos
frame_mensajes = ttk.LabelFrame(root, text="Mensajes Recibidos")
frame_mensajes.pack(pady=10, padx=10, fill="both", expand=True)

# Área de texto para mostrar mensajes
mensaje_recibido = tk.Text(frame_mensajes, height=10)
mensaje_recibido.pack(pady=5, padx=5, fill="both", expand=True)

# Scrollbar para el área de texto
scrollbar = ttk.Scrollbar(frame_mensajes, command=mensaje_recibido.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
mensaje_recibido.config(yscrollcommand=scrollbar.set)

# Iniciar el servidor en un hilo separado
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

# Ejecutar la interfaz
root.mainloop() 