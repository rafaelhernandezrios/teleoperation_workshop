import numpy as np
import socket
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
import json

class SocketEEGReceiver:
    def __init__(self):
        # Parámetros de visualización
        self.n_channels = 8  # Número de canales esperados
        self.buffer_size = 500  # Tamaño del buffer para visualización
        self.running = False
        self.connected = False
        self.socket = None
        
        # Crear buffer circular para cada canal
        self.data_buffer = [deque(maxlen=self.buffer_size) for _ in range(self.n_channels)]
        
        # Configurar GUI
        self.setup_gui()
        
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Receptor EEG - Socket")
        self.root.geometry("800x600")
        
        # Frame de conexión
        connection_frame = ttk.LabelFrame(self.root, text="Conexión")
        connection_frame.pack(pady=5, padx=10, fill="x")
        
        # IP y puerto
        ttk.Label(connection_frame, text="IP:").grid(row=0, column=0, padx=5, pady=5)
        self.ip_var = tk.StringVar(value="localhost")
        ttk.Entry(connection_frame, textvariable=self.ip_var, width=15).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(connection_frame, text="Puerto:").grid(row=0, column=2, padx=5, pady=5)
        self.port_var = tk.StringVar(value="5555")
        ttk.Entry(connection_frame, textvariable=self.port_var, width=6).grid(row=0, column=3, padx=5, pady=5)
        
        # Botón de conexión
        self.connect_button = ttk.Button(connection_frame, text="Conectar", command=self.toggle_connection)
        self.connect_button.grid(row=0, column=4, padx=5, pady=5)
        
        # Estado de la conexión
        self.status_label = ttk.Label(connection_frame, text="Estado: Desconectado")
        self.status_label.grid(row=0, column=5, padx=5, pady=5)
        
        # Configurar gráfico
        self.setup_plot()
        
    def setup_plot(self):
        self.fig, self.axes = plt.subplots(self.n_channels, 1, figsize=(10, 8), sharex=True)
        self.fig.tight_layout(pad=3.0)
        
        # Crear canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Configurar subplots
        channel_names = ['Fp1', 'Fp2', 'C3', 'C4', 'O1', 'O2', 'F7', 'F8']
        for ax, name in zip(self.axes, channel_names):
            ax.set_ylabel(name)
            ax.grid(True)
        
        self.axes[-1].set_xlabel('Muestras')
        
    def update_plot(self):
        for i, ax in enumerate(self.axes):
            ax.clear()
            ax.plot(list(self.data_buffer[i]))
            ax.set_ylabel(f'Canal {i+1}')
            ax.grid(True)
        
        self.axes[-1].set_xlabel('Muestras')
        self.canvas.draw()
        
    def receive_data(self):
        buffer = ""
        while self.running and self.connected:
            try:
                # Recibir datos
                data = self.socket.recv(4096).decode('utf-8')
                if not data:
                    break
                
                # Añadir al buffer y procesar líneas completas
                buffer += data
                lines = buffer.split('\n')
                
                # Procesar todas las líneas completas
                for i in range(len(lines) - 1):
                    try:
                        # Parsear JSON
                        json_data = json.loads(lines[i])
                        
                        # Extraer datos
                        sample = json_data['data']
                        
                        # Actualizar buffer para visualización
                        for i, value in enumerate(sample):
                            if i < self.n_channels:
                                self.data_buffer[i].append(value)
                        
                        # Actualizar gráfico cada 10 muestras
                        if len(self.data_buffer[0]) % 10 == 0:
                            self.update_plot()
                    except json.JSONDecodeError:
                        print(f"Error decodificando JSON: {lines[i]}")
                    except Exception as e:
                        print(f"Error procesando datos: {e}")
                
                # Guardar la última línea incompleta
                buffer = lines[-1]
                
            except Exception as e:
                print(f"Error de conexión: {e}")
                self.disconnect()
                break
        
    def connect(self):
        try:
            ip = self.ip_var.get()
            port = int(self.port_var.get())
            
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((ip, port))
            
            self.connected = True
            self.running = True
            
            # Iniciar thread para recibir datos
            self.receive_thread = threading.Thread(target=self.receive_data)
            self.receive_thread.daemon = True
            self.receive_thread.start()
            
            self.status_label.config(text=f"Estado: Conectado a {ip}:{port}")
            self.connect_button.config(text="Desconectar")
            
        except Exception as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar: {e}")
    
    def disconnect(self):
        self.running = False
        self.connected = False
        
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            
        self.status_label.config(text="Estado: Desconectado")
        self.connect_button.config(text="Conectar")
    
    def toggle_connection(self):
        if not self.connected:
            self.connect()
        else:
            self.disconnect()
    
    def on_closing(self):
        self.disconnect()
        self.root.destroy()
    
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

if __name__ == "__main__":
    app = SocketEEGReceiver()
    app.run() 