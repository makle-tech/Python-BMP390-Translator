import tkinter as tk
from tkinter import ttk
import serial
import threading

class SerialDataApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window setup
        self.title('Serial Data Display')
        self.geometry('400x200')
        self.iconbitmap('icon.ico')  # Ensure 'icon.ico' is in the same directory

        # Initialize serial data variables
        self.temperature = tk.StringVar(value='--°C')
        self.pressure = tk.StringVar(value='-- hPa')
        self.altitude = tk.StringVar(value='-- m')

        # UI setup
        self.create_widgets()

        # Serial thread control
        self.serial_thread = None
        self.running = False

    def create_widgets(self):
        # Data labels
        ttk.Label(self, text="Temperature:").grid(row=0, column=0, sticky="e", padx=10, pady=10)
        ttk.Label(self, textvariable=self.temperature).grid(row=0, column=1, sticky="w")

        ttk.Label(self, text="Pressure:").grid(row=1, column=0, sticky="e", padx=10, pady=10)
        ttk.Label(self, textvariable=self.pressure).grid(row=1, column=1, sticky="w")

        ttk.Label(self, text="Altitude:").grid(row=2, column=0, sticky="e", padx=10, pady=10)
        ttk.Label(self, textvariable=self.altitude).grid(row=2, column=1, sticky="w")

        # Start and stop buttons
        ttk.Button(self, text="Start", command=self.start_serial_reading).grid(row=3, column=0, pady=20)
        ttk.Button(self, text="Stop", command=self.stop_serial_reading).grid(row=3, column=1, pady=20)

    def start_serial_reading(self):
        self.running = True
        self.serial_thread = threading.Thread(target=self.read_from_serial)
        self.serial_thread.start()

    def stop_serial_reading(self):
        self.running = False
        if self.serial_thread is not None:
            self.serial_thread.join()

    def read_from_serial(self):
        try:
            ser = serial.Serial('COM13', 115200, timeout=1)
            while self.running:
                line = ser.readline().decode('utf-8').strip()
                self.parse_and_update(line)
        except serial.SerialException as e:
            print(f"Serial error: {e}")
        finally:
            if 'ser' in locals():
                ser.close()

    def parse_and_update(self, line):
        if "Temperature:" in line:
            parts = line.split("Temperature:")[1].split(" *")[0].strip()
            self.temperature.set(parts + "°C")
        elif "Pressure:" in line:
            parts = line.split("Pressure:")[1].split(" h")[0].strip()
            self.pressure.set(parts + " hPa")
        elif "Altitude:" in line:
            parts = line.split("Altitude:")[1].split(" m")[0].strip()
            self.altitude.set(parts + " m")

# Run the application
if __name__ == "__main__":
    app = SerialDataApp()
    app.mainloop()
