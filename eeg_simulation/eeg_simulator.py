import numpy as np
from pylsl import StreamInfo, StreamOutlet
import time
import threading
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque

class EEGSimulator:
    def __init__(self):
        # Parámetros de la señal EEG
        self.srate = 100  # Frecuencia de muestreo (Hz)
        self.n_channels = 8  # Número de canales
        self.buffer_size = 500  # Tamaño del buffer para visualización
        self.running = False
        
        # Crear buffer circular para cada canal
        self.data_buffer = [deque(maxlen=self.buffer_size) for _ in range(self.n_channels)]
        
        # Configurar LSL Stream
        self.setup_lsl()
        
        # Configurar GUI
        self.setup_gui()
        
    def setup_lsl(self):
        # Crear info del stream LSL
        self.info = StreamInfo(
            name='SimulatedEEG',
            type='EEG',
            channel_count=self.n_channels,
            nominal_srate=self.srate,
            channel_format='float32',
            source_id='SimEEG001'
        )
        
        # Añadir metadatos de los canales
        channels = self.info.desc().append_child("channels")
        channel_names = ['Fp1', 'Fp2', 'C3', 'C4', 'O1', 'O2', 'F7', 'F8']
        for c in channel_names:
            channels.append_child("channel")\
                   .append_child_value("label", c)\
                   .append_child_value("type", "EEG")\
                   .append_child_value("unit", "microvolts")
        
        # Crear outlet
        self.outlet = StreamOutlet(self.info)
        
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
            
            # Enviar muestra a través de LSL
            self.outlet.push_sample(sample)
            
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
        self.root.title("Simulador EEG - LSL")
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
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = EEGSimulator()
    app.run() 