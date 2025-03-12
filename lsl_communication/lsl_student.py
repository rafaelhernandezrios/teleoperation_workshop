import tkinter as tk
from tkinter import ttk, messagebox
from pylsl import StreamOutlet, StreamInfo
import threading

class ArduinoStudent:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Student LSL - Envío de Comandos")
        self.root.geometry("400x300")
        
        # Configurar el stream LSL
        self.setup_lsl()
        
        # Configurar la interfaz gráfica
        self.setup_gui()
        
    def setup_lsl(self):
        # Crear un nuevo stream LSL
        info = StreamInfo(
            name='ArduinoCommands3',
            type='Commands',
            channel_count=1,
            nominal_srate=0,  # Irregular sample rate
            channel_format='string',
            source_id='ArduinoStudentID'
        )
        
        # Crear el outlet
        self.outlet = StreamOutlet(info)
        print("Stream LSL 'ArduinoCommands' creado")
        
    def setup_gui(self):
        # Frame para estado de LSL
        frame_estado = ttk.LabelFrame(self.root, text="Estado LSL")
        frame_estado.pack(pady=10, padx=10, fill="both")
        
        # Etiqueta de estado
        self.lbl_estado = ttk.Label(frame_estado, text="Stream LSL activo: ArduinoCommands")
        self.lbl_estado.pack(pady=5)
        
        # Frame para enviar comandos
        frame_comando = ttk.LabelFrame(self.root, text="Enviar Comando")
        frame_comando.pack(pady=10, padx=10, fill="both")
        
        # Entrada de comando
        self.entrada_comando = tk.Entry(frame_comando, width=30)
        self.entrada_comando.pack(pady=5)
        
        # Botón para enviar comando
        self.btn_enviar = ttk.Button(frame_comando, text="Enviar", command=self.enviar_comando)
        self.btn_enviar.pack(pady=5)
        
        # Área de mensajes
        frame_mensajes = ttk.LabelFrame(self.root, text="Registro de Mensajes")
        frame_mensajes.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.mensaje_log = tk.Text(frame_mensajes, height=8)
        self.mensaje_log.pack(pady=5, padx=5, fill="both", expand=True)
    
    def enviar_comando(self):
        comando = self.entrada_comando.get().strip()
        if comando:
            try:
                # Enviar el comando a través de LSL
                self.outlet.push_sample([comando])
                self.log_message(f"Comando enviado: {comando}")
                self.entrada_comando.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Error", f"Error al enviar el comando: {e}")
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