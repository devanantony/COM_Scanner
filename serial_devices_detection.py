import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports
import re

def detect_usb_serial_ports():
    ports = serial.tools.list_ports.comports()
    usb_ports = []

    for port in ports:
        if 'USB' in port.description or 'usb' in port.device.lower():
            vid = pid = mi = None
            if port.vid is not None and port.pid is not None:
                vid = f"{port.vid:04X}"
                pid = f"{port.pid:04X}"

            mi_match = re.search(r'MI_([0-9A-Fa-f]{2})', port.hwid)
            if mi_match:
                mi = mi_match.group(1)

            usb_ports.append({
                'device': port.device,
                'description': port.description,
                'hwid': port.hwid,
                'vendor_id': vid,
                'product_id': pid,
                'interface_number': mi,
                'raw': str(port)
            })
    return usb_ports


# -------------------------- UI CODE --------------------------

def start_scan():
    text_output.configure(state="normal")
    text_output.delete("1.0", tk.END)

    usb_serial_ports = detect_usb_serial_ports()
    text_output.insert(tk.END, f"Number of USB Serial Devices Detected: {len(usb_serial_ports)}\n\n")

    for port in usb_serial_ports:
        text_output.insert(tk.END, f"Device: {port['device']}\n")
        text_output.insert(tk.END, f"  Description: {port['description']}\n")
        text_output.insert(tk.END, f"  HWID: {port['hwid']}\n")
        text_output.insert(tk.END, f"  Vendor ID: {port['vendor_id']}\n")
        text_output.insert(tk.END, f"  Product ID: {port['product_id']}\n")
        text_output.insert(tk.END, f"  Interface Number (MI): {port['interface_number']}\n")
        text_output.insert(tk.END, f"  Raw Info: {port['raw']}\n\n")

    text_output.configure(state="disabled")

# -------------------------- MAIN WINDOW --------------------------

root = tk.Tk()
root.title("USB Serial Scanner")
root.geometry("700x600")
root.configure(bg="#1e1e1e")

style = ttk.Style()
style.theme_use("clam")

# Modern button style
style.configure(
    "Modern.TButton",
    font=("Segoe UI", 12),
    padding=10,
    relief="flat",
    background="#3a86ff",
    foreground="white"
)
style.map(
    "Modern.TButton",
    background=[("active", "#1f5fc4")]
)

title_label = tk.Label(
    root,
    text="USB Serial Port Scanner",
    font=("Segoe UI", 18, "bold"),
    fg="white",
    bg="#1e1e1e",
    pady=10
)
title_label.pack()

scan_button = ttk.Button(
    root,
    text="Start Scan",
    command=start_scan,
    style="Modern.TButton"
)
scan_button.pack(pady=10)

# Scrollable text output
frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(fill="both", expand=True, padx=15, pady=10)

text_output = tk.Text(
    frame,
    font=("Consolas", 11),
    bg="#2d2d2d",
    fg="#dcdcdc",
    relief="flat",
    wrap="word"
)
text_output.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(frame, command=text_output.yview)
scrollbar.pack(side="right", fill="y")
text_output['yscrollcommand'] = scrollbar.set

text_output.configure(state="disabled")

root.mainloop()
