import tkinter as tk
from tkinter import ttk, messagebox
import socket
import threading

class ArduinoStudent:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Student - Envío de Comandos")
        self.root.geometry("400x300")
        
        self.socket = None
        self.connected = False
        
        self.setup_gui()
        
    def setup_gui(self):
        # Frame de conexión
        frame_conexion = ttk.LabelFrame(self.root, text="Conexión al Master")
        frame_conexion.pack(pady=10, padx=10, fill="both")
        
        # Botón de conexión
        self.btn_conectar = ttk.Button(frame_conexion, text="Conectar al Master", command=self.toggle_connection)
        self.btn_conectar.pack(pady=5)
        
        # Frame para enviar comandos
        frame_comando = ttk.LabelFrame(self.root, text="Enviar Comando")
        frame_comando.pack(pady=10, padx=10, fill="both")
        
        # Entrada de comando
        self.entrada_comando = tk.Entry(frame_comando, width=30)
        self.entrada_comando.pack(pady=5)
        
        # Botón para enviar comando
        self.btn_enviar = ttk.Button(frame_comando, text="Enviar", command=self.enviar_comando)
        self.btn_enviar.pack(pady=5)
        self.btn_enviar.config(state="disabled")
        
        # Área de mensajes
        frame_mensajes = ttk.LabelFrame(self.root, text="Registro de Mensajes")
        frame_mensajes.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.mensaje_log = tk.Text(frame_mensajes, height=8)
        self.mensaje_log.pack(pady=5, padx=5, fill="both", expand=True)
        
    def toggle_connection(self):
        if not self.connected:
            try:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect(('192.168.0.47', 5555))
                self.connected = True
                self.btn_conectar.config(text="Desconectar")
                self.btn_enviar.config(state="normal")
                self.log_message("Conectado al master")
            except ConnectionRefusedError:
                messagebox.showerror("Error", "No se pudo conectar al master. Asegúrese de que esté en ejecución.")
            except:
                messagebox.showerror("Error", "Error al conectar con el master")
        else:
            try:
                self.socket.close()
            finally:
                self.connected = False
                self.btn_conectar.config(text="Conectar al Master")
                self.btn_enviar.config(state="disabled")
                self.log_message("Desconectado del master")
    
    def enviar_comando(self):
        if not self.connected:
            messagebox.showwarning("Advertencia", "No hay conexión con el master")
            return
            
        comando = self.entrada_comando.get().strip()
        if comando:
            try:
                self.socket.send(comando.encode())
                self.log_message(f"Comando enviado: {comando}")
                self.entrada_comando.delete(0, tk.END)
            except:
                messagebox.showerror("Error", "Error al enviar el comando")
                self.toggle_connection()  # Desconectar en caso de error
        else:
            messagebox.showwarning("Advertencia", "Ingrese un comando")
    
    def log_message(self, message):
        self.mensaje_log.insert(tk.END, f"{message}\n")
        self.mensaje_log.see(tk.END)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ArduinoStudent()
    app.run() 