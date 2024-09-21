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
            "Wassertemperatur": "90°C",
            "Öltemperatur": "80°C",
            "Drehzahl": "3000 U/min",
            "Geschwindigkeit": "100 km/h",
            "Ladedruck": "1.2 bar",
            "Batteriespannung": "13.8V",
            "Luftmassenmesser": "5 g/s",
            "Kraftstoffdruck": "3.5 bar",
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
            text="Zu Seite 2 wechseln",
            command=lambda: self.show_frame(self.frame_seite_2),
            height=2,
            width=20,
            bg="lightblue",
            font=("Arial", 16),
        )
        button_seite_1.grid(row=2, column=1, pady=20, columnspan=2)

        button_seite_2 = tk.Button(
            self.frame_seite_2,
            text="Zu Seite 1 wechseln",
            command=lambda: self.show_frame(self.frame_seite_1),
            height=2,
            width=20,
            bg="lightblue",
            font=("Arial", 16),
        )
        button_seite_2.grid(row=2, column=1, pady=20, columnspan=2)

        # Starte mit Seite 1
        self.show_frame(self.frame_seite_1)

        # Update-Funktion regelmäßig aufrufen
        self.update_values()

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

    def update_values(self):
        # Simuliere oder lese Daten hier z.B. von einem OBD-II Dongle
        self.fahrzeugdaten["Wassertemperatur"] = f"{random.randint(80, 100)}°C"
        self.fahrzeugdaten["Öltemperatur"] = f"{random.randint(70, 90)}°C"
        self.fahrzeugdaten["Drehzahl"] = f"{random.randint(1000, 5000)} U/min"
        self.fahrzeugdaten["Geschwindigkeit"] = f"{random.randint(0, 220)} km/h"
        self.fahrzeugdaten["Ladedruck"] = f"{random.uniform(0.5, 2.0):.1f} bar"
        self.fahrzeugdaten["Batteriespannung"] = f"{random.uniform(12.5, 14.5):.1f}V"
        self.fahrzeugdaten["Luftmassenmesser"] = f"{random.uniform(4, 7):.1f} g/s"
        self.fahrzeugdaten["Kraftstoffdruck"] = f"{random.uniform(2.5, 4.0):.1f} bar"

        # Optional: Update der Werte für Seite 2
        self.fahrzeugdaten_seite_2["Motorlast"] = f"{random.randint(50, 100)}%"
        self.fahrzeugdaten_seite_2["Lambdawert"] = f"{random.uniform(0.85, 1.05):.2f}"
        self.fahrzeugdaten_seite_2["Ansauglufttemperatur"] = (
            f"{random.randint(20, 35)}°C"
        )
        self.fahrzeugdaten_seite_2["Saugrohrdruck"] = (
            f"{random.uniform(0.8, 1.2):.2f} bar"
        )
        self.fahrzeugdaten_seite_2["Abgastemperatur"] = f"{random.randint(300, 500)}°C"
        self.fahrzeugdaten_seite_2["Fahrzeit"] = "1h 25min"  # Beispielwert
        self.fahrzeugdaten_seite_2["Kraftstoffverbrauch"] = (
            f"{random.uniform(6.0, 10.0):.1f} L/100km"
        )
        self.fahrzeugdaten_seite_2["CO2-Ausstoß"] = f"{random.randint(100, 150)} g/km"

        # Aktualisieren der Werte in den Labels auf Seite 1
        for box, (key, label) in zip(self.boxen_seite_1, self.fahrzeugdaten.items()):
            box[1].config(text=self.fahrzeugdaten[key])

        # Aktualisieren der Werte in den Labels auf Seite 2
        for box, (key, label) in zip(
            self.boxen_seite_2, self.fahrzeugdaten_seite_2.items()
        ):
            box[1].config(text=self.fahrzeugdaten_seite_2[key])

        # Timer für erneutes Update (hier z.B. alle 1000ms = 1 Sekunde)
        # self.root.after(1000, self.update_values)

    def start_obd_reader(self):
        # Starte den OBD-Leser in einem separaten Thread
        obd_thread = threading.Thread(target=self.obd_reader.run)
        obd_thread.daemon = True  # Daemon-Thread, damit er automatisch beendet wird
        obd_thread.start()

    def on_close(self):
        # Beendet den OBD-Leser, wenn das Fenster geschlossen wird
        self.obd_reader.stop_reading()
        self.root.destroy()


# Hauptprogramm
if __name__ == "__main__":
    root = tk.Tk()
    gui = FahrzeugdatenGUI(root)
    root.protocol("WM_DELETE_WINDOW", gui.on_close)  # Aufräumen beim Schließen
    root.mainloop()
