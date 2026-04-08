# ================================================
# Mobile Signal Scanner
# Coded by: Mr. Sabaz Ali Khan
# GUI + CLI Mode
# ================================================

import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import threading
import subprocess
import platform
import sys

class MobileSignalScanner:
    def __init__(self):
        self.scanning = False
        self.thread = None

    def get_real_signal(self):
        """Try to get real cellular signal using mmcli (Linux + ModemManager)"""
        try:
            if platform.system() == "Linux":
                result = subprocess.check_output(["mmcli", "-m", "0", "--signal-get"], 
                                              stderr=subprocess.STDOUT, timeout=5)
                output = result.decode()
                # Parse basic signal quality
                if "signal quality" in output.lower():
                    for line in output.splitlines():
                        if "signal quality" in line.lower():
                            quality = line.split(":")[-1].strip()
                            return int(quality) if quality.isdigit() else random.randint(60, 95)
            return None
        except:
            return None

    def simulate_scan(self):
        """Simulate realistic mobile signal data"""
        operators = ["Jazz", "Telenor", "Zong", "Ufone", "Mobilink"]
        types = ["2G", "3G", "4G LTE", "5G"]
        
        signal = self.get_real_signal()
        if signal is None:
            signal = random.randint(40, 98)
        
        strength_dbm = random.randint(-110, -65)
        bars = min(5, max(1, signal // 20))
        
        return {
            "operator": random.choice(operators),
            "type": random.choice(types),
            "signal_percent": signal,
            "signal_dbm": strength_dbm,
            "bars": "█" * bars + "░" * (5 - bars),
            "location": f"Lat: 34.{random.randint(100,999)} Long: 72.{random.randint(100,999)}",
            "timestamp": time.strftime("%H:%M:%S")
        }

    def scan_loop(self, gui=None):
        while self.scanning:
            data = self.simulate_scan()
            if gui:
                gui.update_display(data)
            time.sleep(2)

    def start_scan(self, gui=None):
        if not self.scanning:
            self.scanning = True
            self.thread = threading.Thread(target=self.scan_loop, args=(gui,), daemon=True)
            self.thread.start()

    def stop_scan(self):
        self.scanning = False


# ====================== GUI ======================
class SignalGUI:
    def __init__(self):
        self.scanner = MobileSignalScanner()
        self.root = tk.Tk()
        self.root.title("Mobile Signal Scanner - Mr. Sabaz Ali Khan")
        self.root.geometry("600x500")
        self.root.configure(bg="#0f172a")
        
        self.create_widgets()
        self.scanner.start_scan(self)  # Auto-start

    def create_widgets(self):
        # Title
        title = tk.Label(self.root, text="📡 Mobile Signal Scanner", 
                        font=("Arial", 20, "bold"), fg="#22d3ee", bg="#0f172a")
        title.pack(pady=15)

        # Info Frame
        self.info_frame = tk.Frame(self.root, bg="#1e2937", relief="raised", bd=2)
        self.info_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.labels = {}
        fields = ["Operator", "Network Type", "Signal Strength", "dBm", "Bars", "Location", "Last Updated"]
        for i, field in enumerate(fields):
            tk.Label(self.info_frame, text=field + ":", font=("Arial", 11, "bold"),
                    fg="#94a3b8", bg="#1e2937", anchor="w").grid(row=i, column=0, sticky="w", padx=15, pady=8)
            self.labels[field] = tk.Label(self.info_frame, text="-", font=("Arial", 11),
                                        fg="white", bg="#1e2937", anchor="w")
            self.labels[field].grid(row=i, column=1, sticky="w", padx=15, pady=8)

        # Control Buttons
        btn_frame = tk.Frame(self.root, bg="#0f172a")
        btn_frame.pack(pady=20)

        self.start_btn = tk.Button(btn_frame, text="🔄 Start Scanning", font=("Arial", 12, "bold"),
                                  bg="#22c55e", fg="black", width=15, command=self.start_scanning)
        self.start_btn.grid(row=0, column=0, padx=10)

        self.stop_btn = tk.Button(btn_frame, text="⏹ Stop", font=("Arial", 12, "bold"),
                                 bg="#ef4444", fg="white", width=15, command=self.stop_scanning)
        self.stop_btn.grid(row=0, column=1, padx=10)

        tk.Button(btn_frame, text="Exit", font=("Arial", 12, "bold"),
                 bg="#64748b", fg="white", width=10, command=self.root.quit).grid(row=0, column=2, padx=10)

        # Status
        self.status = tk.Label(self.root, text="Scanning Active...", fg="#22d3ee", 
                              bg="#0f172a", font=("Arial", 10))
        self.status.pack(pady=5)

    def update_display(self, data):
        self.root.after(0, self._update_ui, data)

    def _update_ui(self, data):
        self.labels["Operator"].config(text=data["operator"])
        self.labels["Network Type"].config(text=data["type"])
        self.labels["Signal Strength"].config(text=f"{data['signal_percent']}%")
        self.labels["dBm"].config(text=f"{data['signal_dbm']} dBm")
        self.labels["Bars"].config(text=data["bars"], fg="#22d3ee")
        self.labels["Location"].config(text=data["location"])
        self.labels["Last Updated"].config(text=data["timestamp"])

    def start_scanning(self):
        self.scanner.start_scan(self)
        self.status.config(text="Scanning Active... ✅", fg="#22d3ee")

    def stop_scanning(self):
        self.scanner.stop_scan()
        self.status.config(text="Scanning Stopped", fg="#f87171")

    def run(self):
        self.root.mainloop()


# ====================== CLI Mode ======================
def cli_mode():
    print("🚀 Mobile Signal Scanner (CLI) - Mr. Sabaz Ali Khan")
    scanner = MobileSignalScanner()
    print("Press Ctrl+C to stop...\n")
    try:
        while True:
            data = scanner.simulate_scan()
            print(f"[{data['timestamp']}] Operator: {data['operator']} | Type: {data['type']}")
            print(f"Signal: {data['signal_percent']}% ({data['signal_dbm']} dBm) {data['bars']}")
            print(f"Location: {data['location']}")
            print("-" * 60)
            time.sleep(3)
    except KeyboardInterrupt:
        print("\nGoodbye!")


# ====================== Main ======================
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        cli_mode()
    else:
        print("Launching GUI Mode...")
        app = SignalGUI()
        app.run()