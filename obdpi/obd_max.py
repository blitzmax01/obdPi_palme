import obd
import threading
import time


class OBDReader:
    def __init__(self, callback):
        # Versucht, eine OBD-Verbindung herzustellen
        self.commands = {}
        self.connection = obd.Async()  # Asynchrone OBD-Verbindung
        self.callback = callback
        self.running = False  # Steuert, ob der Leser läuft

    def find_supported_pids_for_mode(self, mode=1):
        """
        Prüft verfügbare PIDs für ein bestimmtes Steuergerät bzw. Mode.
        Standardmäßig wird Mode 1 (Motorsteuergerät) verwendet.
        """
        # Überprüfen, ob eine OBD-Verbindung vorhanden ist
        if self.connection.status() == obd.OBDStatus.NOT_CONNECTED:
            print("OBD-II Dongle nicht verbunden!")
            return

        # Erstellt eine Liste der PIDs im gewählten Modus
        available_commands = obd.commands[mode]  # Befehl für den Modus abrufen
        supported_commands = []

        # Unterstützte PIDs durchgehen und prüfen
        for command in available_commands:
            if command in self.connection.supported_commands:
                supported_commands.append(command)

        # Speichere die gefundenen PIDs in self.commands
        self.commands = {cmd.name: cmd for cmd in supported_commands}

        # Zeige die verfügbaren PIDs an
        print(f"Verfügbare PIDs für Modus {mode}:")
        for name, cmd in self.commands.items():
            print(f"{name}: {cmd}")

    def start_reading(self):
        # Überprüft, ob die Verbindung erfolgreich hergestellt wurde
        if self.connection.status() == obd.OBDStatus.NOT_CONNECTED:
            print("OBD-II Dongle nicht verbunden!")
            return

        self.running = True

        # Abfragen, die wir benötigen
        self.commands = {
            "Watertemp": obd.commands.COOLANT_TEMP,
            "Oiltemp": obd.commands.OIL_TEMP,
            "RPM": obd.commands.RPM,
            "Speed": obd.commands.SPEED,
            "Boost": obd.commands.BAROMETRIC_PRESSURE,
            "Battery": obd.commands.CONTROL_MODULE_VOLTAGE,
            "MAF": obd.commands.MAF,
            "FuelPressure": obd.commands.FUEL_PRESSURE,
        }

        # Asynchrone Abfragen für jedes Kommando starten
        for name, command in self.commands.items():
            self.connection.watch(
                command, callback=self.obd_callback(name)
            )  # Listener für jedes Kommando setzen

        self.connection.start()  # Beginnt mit dem asynchronen Lesen der OBD-Daten

    def obd_callback(self, name):
        # Diese Funktion wird für jedes OBD-Kommando aufgerufen und sendet die Daten an die GUI
        def _callback(response):
            if response.value is not None:
                value = response.value.to("°C") if "Temp" in name else response.value
                self.callback(
                    name, str(value)
                )  # Daten an die Callback-Funktion (GUI) übergeben

        return _callback

    def stop_reading(self):
        # Stoppt die OBD-Verbindung und das Lesen
        self.connection.stop()
        self.running = False

    def run(self):
        while self.running:
            # Stelle sicher, dass die Verbindung noch aktiv ist
            if self.connection.status() == obd.OBDStatus.NOT_CONNECTED:
                print("Verbindung verloren!")
                self.stop_reading()
            time.sleep(1)


def update_vehicle_data(name, value):
    print(f"{name}: {value}")


def main():
    obd_reader = OBDReader(update_vehicle_data)

    # Starte den OBD-Leser in einem separaten Thread
    obd_thread = threading.Thread(target=obd_reader.run)
    obd_thread.daemon = True  # Daemon-Thread, damit er automatisch beendet wird
    obd_thread.start()

    # Verfügbare PIDs suchen
    obd_reader.find_supported_pids_for_mode(1)  # Motor
    obd_reader.find_supported_pids_for_mode(2)  # Getriebe

    # Starte die Überwachung der gefundenen OBD-II PIDs
    obd_reader.start_reading()

    try:
        while True:
            time.sleep(1)  # Haupt-Thread läuft weiter, während OBD asynchron arbeitet
    except KeyboardInterrupt:
        # Aufräumen und beenden, wenn das Programm mit STRG+C gestoppt wird
        obd_reader.stop_reading()


if __name__ == "__main__":
    main()
