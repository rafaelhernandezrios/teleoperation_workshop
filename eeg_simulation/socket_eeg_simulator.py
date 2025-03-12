import numpy as np
import socket
import time
import threading
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
import json

class SocketEEGSimulator:
    def __init__(self):
        # Parámetros de la señal EEG
        self.srate = 100  # Frecuencia de muestreo (Hz)
        self.n_channels = 8  # Número de canales
        self.buffer_size = 500  # Tamaño del buffer para visualización
        self.running = False
        self.server_running = False
        self.clients = []
        
        # Crear buffer circular para cada canal
        self.data_buffer = [deque(maxlen=self.buffer_size) for _ in range(self.n_channels)]
        
        # Configurar socket servidor
        self.setup_server()
        
        # Configurar GUI
        self.setup_gui()
        
    def setup_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('localhost', 5555))
        self.server_socket.listen(5)
        
        # Iniciar thread para aceptar conexiones
        self.server_thread = threading.Thread(target=self.accept_connections)
        self.server_thread.daemon = True
        self.server_running = True
        self.server_thread.start()
        
        print("Servidor socket iniciado en puerto 5555")
        
    def accept_connections(self):
        while self.server_running:
            try:
                client_socket, address = self.server_socket.accept()
                print(f"Cliente conectado desde {address}")
                self.clients.append(client_socket)
            except:
                break
        
    def generate_eeg_sample(self):
        # Generar componente de onda alfa (8-13 Hz)
        t = time.time()
        alpha = np.sin(2 * np.pi * 10 * t) * 10  # 10 Hz onda alfa
        
        # Generar ruido para cada canal
        noise = np.random.normal(0, 2, self.n_channels)
        
        # Combinar señal y ruido
        sample = noise + alpha
        return sample
        
    def stream_data(self):
        while self.running:
            sample = self.generate_eeg_sample()
            
            # Enviar muestra a través de socket a todos los clientes conectados
            if self.clients:
                # Convertir a lista y luego a JSON
                sample_list = sample.tolist()
                data_to_send = json.dumps({
                    'timestamp': time.time(),
                    'data': sample_list,
                    'channels': ['Fp1', 'Fp2', 'C3', 'C4', 'O1', 'O2', 'F7', 'F8']
                })
                
                # Enviar a todos los clientes
                disconnected_clients = []
                for client in self.clients:
                    try:
                        client.send((data_to_send + '\n').encode())
                    except:
                        disconnected_clients.append(client)
                
                # Eliminar clientes desconectados
                for client in disconnected_clients:
                    if client in self.clients:
                        self.clients.remove(client)
            
            # Actualizar buffer para visualización
            for i, value in enumerate(sample):
                self.data_buffer[i].append(value)
            
            # Actualizar gráfico cada 10 muestras
            if len(self.data_buffer[0]) % 10 == 0:
                self.update_plot()
            
            # Esperar para mantener la frecuencia de muestreo
            time.sleep(1.0/self.srate)
    
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Simulador EEG - Socket (Puerto 5555)")
        self.root.geometry("800x600")
        
        # Frame de control
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=5)
        
        # Botón de inicio/parada
        self.toggle_button = ttk.Button(control_frame, text="Iniciar", command=self.toggle_streaming)
        self.toggle_button.pack(side=tk.LEFT, padx=5)
        
        # Estado del stream
        self.status_label = ttk.Label(control_frame, text="Estado: Detenido")
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Clientes conectados
        self.clients_label = ttk.Label(control_frame, text="Clientes: 0")
        self.clients_label.pack(side=tk.LEFT, padx=5)
        
        # Configurar gráfico
        self.setup_plot()
        
        # Actualizar contador de clientes periódicamente
        self.update_client_count()
        
    def update_client_count(self):
        self.clients_label.config(text=f"Clientes: {len(self.clients)}")
        self.root.after(1000, self.update_client_count)
        
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
        
    def toggle_streaming(self):
        if not self.running:
            self.running = True
            self.toggle_button.config(text="Detener")
            self.status_label.config(text="Estado: Transmitiendo")
            self.stream_thread = threading.Thread(target=self.stream_data)
            self.stream_thread.daemon = True
            self.stream_thread.start()
        else:
            self.running = False
            self.toggle_button.config(text="Iniciar")
            self.status_label.config(text="Estado: Detenido")
    
    def on_closing(self):
        self.running = False
        self.server_running = False
        
        # Cerrar todas las conexiones
        for client in self.clients:
            try:
                client.close()
            except:
                pass
        
        try:
            self.server_socket.close()
        except:
            pass
            
        self.root.destroy()
    
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

if __name__ == "__main__":
    app = SocketEEGSimulator()
    app.run() 