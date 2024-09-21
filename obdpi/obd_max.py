import obd
import threading
import time


class OBDReader:
    def __init__(self, callback):
        # Versucht, eine OBD-Verbindung herzustellen
        self.commands = None
        self.connection = obd.Async()  # Asynchrone OBD-Verbindung
        self.callback = (
            callback  # Diese Funktion wird aufgerufen, um Daten an die GUI zu senden
        )
        self.running = False  # Steuert, ob der Leser läuft

    def start_reading(self):
        # Überprüft, ob die Verbindung erfolgreich hergestellt wurde
        if self.connection.status() == obd.OBDStatus.NOT_CONNECTED:
            print("OBD-II Dongle nicht verbunden!")
            return

        self.running = True

        # Abfragen, die wir benötigen
        self.commands = {
            "Wassertemperatur": obd.commands.COOLANT_TEMP,
            "Öltemperatur": obd.commands.OIL_TEMP,
            "Drehzahl": obd.commands.RPM,
            "Geschwindigkeit": obd.commands.SPEED,
            "Ladedruck": obd.commands.BAROMETRIC_PRESSURE,
            "Batteriespannung": obd.commands.CONTROL_MODULE_VOLTAGE,
            "Luftmassenmesser": obd.commands.MAF,
            "Kraftstoffdruck": obd.commands.FUEL_PRESSURE,
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
                self.callback(name, str(value))  # Daten an GUI übergeben

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
