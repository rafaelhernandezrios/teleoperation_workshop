# Workshop 3 - Teleoperation

This project implements a teleoperation system that enables communication between devices using different protocols (sockets and LSL - Lab Streaming Layer) and connection with Arduino for hardware control.

## Project Structure

The project is organized into the following folders:

- `socket_communication/`: Basic socket communication implementation
- `lsl_communication/`: Lab Streaming Layer communication implementation
- `arduino_control/`: Arduino control interface implementations
- `eeg_simulation/`: EEG signal simulation and visualization tools

## Description

This project contains several scripts that implement different communication methods for teleoperation:

1. **Socket Communication** (`socket_communication/`):
   - `master.py` and `student.py`: Basic implementation of bidirectional communication using sockets.

2. **Arduino Control** (`arduino_control/`):
   - `arduino_master.py` and `arduino_student.py`: Socket communication with Arduino control interface.

3. **LSL Communication** (`lsl_communication/`):
   - `lsl_master.py` and `lsl_student.py`: Communication using LSL with Arduino control interface.
   - `producer.py` and `consumer.py`: Basic implementation of communication using LSL.

4. **EEG Simulation** (`eeg_simulation/`):
   - `eeg_simulator.py` and `eeg_receiver.py`: Generate and visualize simulated EEG signals through LSL.
   - `socket_eeg_simulator.py` and `socket_eeg_receiver.py`: Generate and visualize simulated EEG signals through sockets.

## Requirements

To run these scripts, you will need:

- Python 3.7 or higher
- Libraries listed in `requirements.txt`
- Arduino (optional, for hardware control)

## Installation

### Setting up a Virtual Environment

It's recommended to use a virtual environment to avoid conflicts with other Python packages:

#### On Windows:

1. Clone this repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   ```
   venv\Scripts\activate
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Socket Communication

1. Start the server (master):
   ```
   python socket_communication/master.py
   ```
2. Start the client (student):
   ```
   python socket_communication/student.py
   ```
3. You can now exchange messages between both programs.

### Arduino Control with Sockets

1. Start the Arduino server:
   ```
   python arduino_control/arduino_master.py
   ```
2. Select the COM port and baudrate to connect with Arduino
3. Start the client:
   ```
   python arduino_control/arduino_student.py
   ```
4. Connect to the server and send commands that will be forwarded to Arduino.

### LSL Communication

1. Start the LSL server:
   ```
   python lsl_communication/lsl_master.py
   ```
2. Select the COM port and baudrate to connect with Arduino
3. Start the LSL client:
   ```
   python lsl_communication/lsl_student.py
   ```
4. Send commands that will be forwarded to Arduino.

### EEG Simulation with LSL

1. Start the EEG simulator:
   ```
   python eeg_simulation/eeg_simulator.py
   ```
2. Start the EEG receiver:
   ```
   python eeg_simulation/eeg_receiver.py
   ```
3. Click "Start" in the simulator and "Connect" in the receiver to visualize the EEG signals.

### EEG Simulation with Sockets

1. Start the EEG simulator:
   ```
   python eeg_simulation/socket_eeg_simulator.py
   ```
2. Start the EEG receiver:
   ```
   python eeg_simulation/socket_eeg_receiver.py
   ```
3. Enter connection details in the receiver (default: localhost:5555)
4. Click "Start" in the simulator and "Connect" in the receiver to visualize the EEG signals.

## Notes

- For Arduino communication, make sure the device is connected and programmed to receive commands via serial port.
- LSL scripts require the `pylsl` library which might be more difficult to install on some systems. Check the official LSL documentation for more details.
- To deactivate the virtual environment when you're done, simply type `deactivate` in your terminal.

## License

This project is open source and available under the terms of the MIT license. 