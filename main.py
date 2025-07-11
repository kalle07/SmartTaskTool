import wx
import sys
import threading
import queue
import time
import os
from gui import MainFrame
from tray import start_tray_monitoring, shutdown_requested
from hardware import detect_hardware

# main.py

def start_gui_and_get_selection(hardware_info, result_queue):
    class App(wx.App):
        def OnInit(self):
            self.frame = MainFrame(None, hardware_info=hardware_info, result_queue=result_queue)
            self.frame.Show()
            return True

    app = App(False)
    app.MainLoop()


def save_exe_dir_to_meipass():
    try:
        # Ermittlung des MEIPASS-Pfads (nur wenn als .exe via PyInstaller gestartet)
        if hasattr(sys, '_MEIPASS'):
            meipass_dir = sys._MEIPASS
        else:
            print("[WARN] Kein MEIPASS gefunden (nicht als EXE gestartet). Überspringe Speichern.")
            return

        # Pfad zur laufenden .exe
        if getattr(sys, 'frozen', False):
            #exe_dir = os.path.dirname(sys.executable)
            exe_path = sys.executable  # <- vollständiger Pfad zur exe inkl. Dateiname
        else:
            #exe_dir = os.path.dirname(os.path.abspath(__file__))
            exe_path = os.path.abspath(__file__)  # <- vollständiger Pfad zur .py Datei

        # Zieldatei im MEIPASS-Verzeichnis
        output_file = os.path.join(meipass_dir, "startdir.txt")

        with open(output_file, "w", encoding="utf-8") as f:
            #f.write(f"Startverzeichnis: {exe_dir}\n")
            f.write(f"{exe_path}\n")

        print(f"[INFO] Startverzeichnis und Startdatei gespeichert in MEIPASS: {output_file}")
    except Exception as e:
        print(f"[ERROR] Fehler beim Schreiben der startdir.txt: {e}")


if __name__ == "__main__":
    try:
        time.sleep(0.5)

        # Schreibe das Startverzeichnis in den MEIPASS-Ordner
        save_exe_dir_to_meipass()

        print("[DEBUG] Starte hardware.py...")
        hardware_info = detect_hardware()
        print("[DEBUG] hardware.py exit...")

        result_queue = queue.Queue()

        # GUI im MainThread starten!
        start_gui_and_get_selection(hardware_info, result_queue)

        print("[INFO] GUI beendet.")

        try:
            selected_components = result_queue.get(timeout=11)
            tray_should_start = any([
                selected_components.get('cpu'),
                selected_components.get('ram'),
                selected_components.get('gpu'),
                selected_components.get('network'),
                bool(selected_components.get('drives'))
            ])
        except queue.Empty:
            print("[WARN] Keine Rückgabe durch GUI. Traymonitor wird nicht gestartet.")
            tray_should_start = False

        if tray_should_start:
            print("[INFO] Auswahl empfangen:", selected_components)
            time.sleep(1)

            tray_thread = threading.Thread(
                target=start_tray_monitoring,
                args=(hardware_info, selected_components),
                daemon=False
            )
            tray_thread.start()

            # Haupt-Exit-Überwachung
            while not shutdown_requested.wait(timeout=0.1):
                pass

            print("[INFO] Tray-Exit wurde erkannt – beende main.py.")
            sys.exit(0)


            print("[INFO] Tray-Monitoring gestartet. GUI ist geschlossen.")
            tray_thread.join()
        else:
            print("[INFO] Programm wird beendet, da keine Auswahl getroffen wurde (GUI geschlossen).")
            sys.exit(0)  # Sauber beenden, wenn kein Traymonitor starten soll

    except KeyboardInterrupt:
        print("[INFO] Manuell beendet.")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] Unerwarteter Fehler: {e}", file=sys.stderr)
        sys.exit(1)

