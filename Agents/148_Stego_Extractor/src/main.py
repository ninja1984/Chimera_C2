import sys
import os
from PIL import Image

def extract_lsb_data(image_path, output_bin):
    """
    Weaponized Stego: Iterates through every pixel and extracts 
    the LSB of the Red, Green, and Blue channels to rebuild a binary file.
    """
    print(f"[*] Analyzing Image: {image_path}")
    
    try:
        img = Image.open(image_path)
        # Ensure we are in RGB mode for consistent bit-depth
        img = img.convert('RGB')
        pixels = img.getdata()
        
        bit_stream = ""
        print(f"[*] Processing {len(pixels)} pixels...")
        
        # Extract 1 bit from each color channel
        for r, g, b in pixels:
            bit_stream += str(r & 1)
            bit_stream += str(g & 1)
            bit_stream += str(b & 1)
            
        # Group bits into 8-bit bytes
        byte_chunks = [bit_stream[i:i+8] for i in range(0, len(bit_stream), 8)]
        
        # Convert bit strings to actual bytes
        binary_payload = bytearray()
        for chunk in byte_chunks:
            if len(chunk) == 8:
                binary_payload.append(int(chunk, 2))
        
        # Write reconstructed binary to the output file
        with open(output_bin, 'wb') as f:
            f.write(binary_payload)
            
        print(f"[!] RECONSTRUCTION COMPLETE: {output_bin}")
        print(f"[*] Size: {len(binary_payload)} bytes")
        
        # Tactical Note: Run 'file' or 'binwalk' on the output to identify contents.
        with open("../loot/stego_history.log", "a") as log:
            log.write(f"Source: {image_path} | Target: {output_bin} | Bytes: {len(binary_payload)}\n")

    except Exception as e:
        print(f"[-] Stego Fault: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: 135_stego <input_image> <output_binary_path>")
        sys.exit(1)
    
    extract_lsb_data(sys.argv[1], sys.argv[2])
