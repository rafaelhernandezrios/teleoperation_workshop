import numpy as np
from pylsl import StreamInlet, resolve_stream
import time
import threading
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque

class EEGReceiver:
    def __init__(self):
        # Parámetros de visualización
        self.n_channels = 8  # Número de canales esperados
        self.buffer_size = 500  # Tamaño del buffer para visualización
        self.running = False
        
        # Crear buffer circular para cada canal
        self.data_buffer = [deque(maxlen=self.buffer_size) for _ in range(self.n_channels)]
        
        # Configurar GUI
        self.setup_gui()
        
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Receptor EEG - LSL")
        self.root.geometry("800x600")
        
        # Frame de control
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=5)
        
        # Botón de inicio/parada
        self.toggle_button = ttk.Button(control_frame, text="Conectar", command=self.toggle_receiving)
        self.toggle_button.pack(side=tk.LEFT, padx=5)
        
        # Estado del stream
        self.status_label = ttk.Label(control_frame, text="Estado: Desconectado")
        self.status_label.pack(side=tk.LEFT, padx=5)
        
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
        # Buscar stream EEG
        print("Buscando stream LSL 'SimulatedEEG'...")
        streams = resolve_stream('name', 'SimulatedEEG')
        
        if not streams:
            print("No se encontró el stream LSL")
            self.status_label.config(text="Estado: Stream no encontrado")
            return
            
        # Crear inlet
        inlet = StreamInlet(streams[0])
        print(f"Stream LSL encontrado: {streams[0].name()}")
        self.status_label.config(text=f"Estado: Conectado a {streams[0].name()}")
        
        # Recibir datos
        while self.running:
            try:
                # Recibir muestra
                sample, timestamp = inlet.pull_sample(timeout=1.0)
                
                if sample:
                    # Actualizar buffer para visualización
                    for i, value in enumerate(sample):
                        if i < self.n_channels:  # Asegurarse de no exceder el número de canales
                            self.data_buffer[i].append(value)
                    
                    # Actualizar gráfico cada 10 muestras
                    if len(self.data_buffer[0]) % 10 == 0:
                        self.update_plot()
                
            except Exception as e:
                print(f"Error al recibir datos: {e}")
                break
        
        print("Recepción de datos detenida")
        
    def toggle_receiving(self):
        if not self.running:
            self.running = True
            self.toggle_button.config(text="Desconectar")
            self.status_label.config(text="Estado: Conectando...")
            self.receive_thread = threading.Thread(target=self.receive_data)
            self.receive_thread.daemon = True
            self.receive_thread.start()
        else:
            self.running = False
            self.toggle_button.config(text="Conectar")
            self.status_label.config(text="Estado: Desconectado")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = EEGReceiver()
    app.run() 