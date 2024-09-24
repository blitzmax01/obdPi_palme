import threading
import tkinter as tk
from tkinter import ttk
import random

from obdpi.obd_max import OBDReader


class FahrzeugdatenGUI:
    def __init__(self, root):
        self.obd_reader = None
        self.root = root
        self.root.title("Fahrzeugdaten-Anzeige")
        self.root.geometry("800x400")  # Fenstergröße setzen (800x400)
        self.root.resizable(False, False)  # Keine Größenänderung zulassen

        # Daten initialisieren (Beispielwerte für Seite 1)
        self.fahrzeugdaten = {
            "Watertemp": "90°C",
            "Oiltemp": "80°C",
            "RPM": "3000 U/min",
            "Speed": "100 km/h",
            "Boost": "1.2 bar",
            "Battery": "13.8V",
            "MAF": "5 g/s",
            "FuelPressure": "3.5 bar",
        }

        # Daten für Seite 2
        self.fahrzeugdaten_seite_2 = {
            "Motorlast": "75%",
            "Lambdawert": "0.98",
            "Ansauglufttemperatur": "25°C",
            "Saugrohrdruck": "0.95 bar",
            "Abgastemperatur": "400°C",
            "Fahrzeit": "1h 25min",
            "Kraftstoffverbrauch": "8.5 L/100km",
            "CO2-Ausstoß": "120 g/km",
        }

        # OBD-Leser initialisieren und starten
        self.obd_reader = OBDReader(self.update_value)
        self.start_obd_reader()

        # Styles für die Boxen
        style = ttk.Style()
        style.configure("TFrame", background="lightgray")
        style.configure(
            "TLabel", background="lightgray", font=("Arial", 18)
        )  # Größere Schriftart

        # Hauptframe für alle Seiten erstellen
        container = tk.Frame(self.root)
        container.pack(fill="both", expand=True)

        # Frames für die zwei Seiten erstellen
        self.frame_seite_1 = tk.Frame(container)
        self.frame_seite_2 = tk.Frame(container)

        for frame in (self.frame_seite_1, self.frame_seite_2):
            frame.grid(row=0, column=0, sticky="nsew")

        # Boxen-Layout für Seite 1 (4x2 Grid, große Boxen)
        self.boxen_seite_1 = []  # Liste, um später auf die Boxen zugreifen zu können
        for i, (name, wert) in enumerate(self.fahrzeugdaten.items()):
            frame = ttk.Frame(
                self.frame_seite_1, padding=20, relief="ridge", style="TFrame"
            )  # Mehr Padding
            frame.grid(
                row=i // 4, column=i % 4, sticky="nsew", padx=10, pady=10
            )  # Mehr Platz zwischen Boxen

            label_name = ttk.Label(frame, text=name, style="TLabel", anchor="center")
            label_name.pack(pady=5)

            label_wert = ttk.Label(frame, text=wert, style="TLabel", anchor="center")
            label_wert.pack(pady=5)

            self.boxen_seite_1.append((label_name, label_wert))

        # Boxen-Layout für Seite 2 (4x2 Grid, große Boxen)
        self.boxen_seite_2 = []  # Liste für Seite 2
        for i, (name, wert) in enumerate(self.fahrzeugdaten_seite_2.items()):
            frame = ttk.Frame(
                self.frame_seite_2, padding=20, relief="ridge", style="TFrame"
            )
            frame.grid(row=i // 4, column=i % 4, sticky="nsew", padx=10, pady=10)

            label_name = ttk.Label(frame, text=name, style="TLabel", anchor="center")
            label_name.pack(pady=5)

            label_wert = ttk.Label(frame, text=wert, style="TLabel", anchor="center")
            label_wert.pack(pady=5)

            self.boxen_seite_2.append((label_name, label_wert))

        # Buttons zum Wechseln der Seiten auf beiden Seiten hinzufügen
        button_seite_1 = tk.Button(
            self.frame_seite_1,
            text="Page 2",
            command=lambda: self.show_frame(self.frame_seite_2),
            height=2,
            width=20,
            bg="lightblue",
            font=("Arial", 16),
        )
        button_seite_1.grid(row=2, column=1, pady=20, columnspan=2)

        button_seite_2 = tk.Button(
            self.frame_seite_2,
            text="Page 1",
            command=lambda: self.show_frame(self.frame_seite_1),
            height=2,
            width=20,
            bg="lightblue",
            font=("Arial", 16),
        )
        button_seite_2.grid(row=2, column=1, pady=20, columnspan=2)

        # Starte mit Seite 1
        self.show_frame(self.frame_seite_1)

    # Funktion zum Umschalten zwischen Seiten
    def show_frame(self, frame):
        frame.tkraise()

    def update_value(self, name, value):
        # Diese Methode wird vom OBDReader aufgerufen, um Werte in der GUI zu aktualisieren
        for box, (key, label) in zip(self.boxen_seite_1, self.fahrzeugdaten.items()):
            if key == name:
                box[1].config(text=value)
                self.fahrzeugdaten[key] = value

    def start_obd_reader(self):
        # Starte den OBD-Leser in einem separaten Thread
        obd_thread = threading.Thread(target=self.obd_reader.run)
        obd_thread.daemon = True  # Daemon-Thread, damit er automatisch beendet wird
        obd_thread.start()

    def on_close(self):
        # Beendet den OBD-Leser, wenn das Fenster geschlossen wird
        self.obd_reader.stop_reading()
        self.root.destroy()


def main():
    root = tk.Tk()
    gui = FahrzeugdatenGUI(root)
    root.protocol("WM_DELETE_WINDOW", gui.on_close)  # Aufräumen beim Schließen
    root.mainloop()


# Hauptprogramm
if __name__ == "__main__":
    main()
