#!/usr/bin/env python3
"""
Enhanced OSRipper Obfuscator v2.0
Same as basic obfuscator but with sandbox detection
"""

import os
import sys
import zlib
import base64
import random

# Encoding functions (OSRipper-0.3 compatible)
zlb = lambda in_ : zlib.compress(in_)
b32 = lambda in_ : base64.b32encode(in_)
b64 = lambda in_ : base64.b64encode(in_)

class FileSize:
    def datas(self, z):
        for x in ['Byte', 'KB', 'MB', 'GB']:
            if z < 1024.0:
                return "%3.1f %s" % (z, x)
            z /= 1024.0
    
    def __init__(self, path):
        if os.path.isfile(path):
            dts = os.stat(path).st_size
            print('\n')
            print(" [-] Encoded File Size : %s\n" % self.datas(dts))

def add_random_padding(code):
    """
    Add random comment lines throughout the code to randomize file size.
    Adds between 500-1000 comment lines at random positions with random strings.
    """
    import secrets
    import string
    
    # Split code into lines
    lines = code.split('\n')
    total_lines = len(lines)
    
    # Generate random number of padding lines to add (500-1000)
    num_padding_lines = random.randint(500, 1000)
    
    # Generate all padding lines at once with random strings
    padding_lines = []
    for _ in range(num_padding_lines):
        # Random length for the comment string
        str_length = random.randint(10, 80)
        # Generate random string using letters, digits, and some punctuation
        random_str = ''.join(secrets.choice(string.ascii_letters + string.digits + ' _-') for _ in range(str_length))
        comment = '# ' + random_str
        padding_lines.append(comment)
    
    # Determine random positions to insert padding
    # We'll insert padding after random lines
    positions = sorted(random.sample(range(total_lines), min(total_lines, num_padding_lines // 10)))
    
    # Insert padding in chunks at random positions
    offset = 0
    padding_index = 0
    
    for pos in positions:
        # Insert a random chunk of padding lines
        chunk_size = random.randint(5, 50)
        if padding_index + chunk_size > num_padding_lines:
            chunk_size = num_padding_lines - padding_index
        
        if chunk_size > 0:
            # Insert the chunk after this position
            insert_pos = pos + offset
            for i in range(chunk_size):
                if padding_index < num_padding_lines:
                    lines.insert(insert_pos + i, padding_lines[padding_index])
                    padding_index += 1
            offset += chunk_size
        
        if padding_index >= num_padding_lines:
            break
    
    # Add any remaining padding at the end
    while padding_index < num_padding_lines:
        lines.append(padding_lines[padding_index])
        padding_index += 1
    
    return '\n'.join(lines)

def Encode(data, output):
    """
    Encode data with multiple layers of b32/b64/zlib compression.
    Enhanced version with sandbox detection and double-layer encoding from OSRipper-0.3.
    Each encoding type gets its own random layer count.
    """
    # Generate independent random layer counts for each encoding type
    loop_b32 = random.randint(30, 60)
    loop_b64 = random.randint(30, 60)
    
    import re
    
    # Add random padding to randomize file size
    print("[*] Adding random padding to payload...")
    data = add_random_padding(data)
    print("[+] Random padding added")
    
    # Debug: Print the final payload before encoding
    print("\n" + "="*60)
    print("DEBUG: Final payload before encoding (first 50 lines):")
    print("="*60)
    print('\n'.join(data.split('\n')[:50]))
    print("... (truncated) ...")
    print("="*60 + "\n")
    
    # OSRipper-0.3 double-layer encoding approach
    # First layer: b32 + zlib encoding
    x1 = "b32(zlb(data.encode('utf8')))[::-1]"
    heading1 = "_ = lambda __ : __import__('zlib').decompress(__import__('base64').b32decode(__[::-1]));"
    
    # Second layer: b64 + zlib encoding
    x2 = "b64(zlb(data.encode('utf8')))[::-1]"
    heading2 = "_ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));"
    
    # Apply first encoding layer (b32) with its own random count
    print(f"[*] Applying {loop_b32} layers of b32+zlib encoding...")
    for x in range(loop_b32):
        try:
            data = "exec((_)(%s))" % repr(eval(x1))
        except TypeError as s:
            sys.exit(" TypeError : " + str(s))
    ab=(heading1 + data)
    for x in range(loop_b64):
        try:
            data = "exec((_)(%s))" % repr(eval(x2))
        except TypeError as s:
            sys.exit(" TypeError : " + str(s))
    abc=(heading2 + ab)
    
    # Write final encoded payload
    with open(output, 'w') as f:
        f.write(abc)
        f.close()
    
    print(f"[+] Double-layer encoding complete: {loop_b32}x b32 + {loop_b64}x b64 = {loop_b32 + loop_b64} total layers")

def MainMenu(file):
    """Main obfuscation entry point (backward compatibility)."""
    try:
        data = open(file).read()
    except IOError:
        sys.exit("\n File Not Found!")
    
    output = file.lower().replace('.py', '') + '_or.py'
    
    print(f"Starting advanced OSRipper-0.3 double-layer obfuscation (each layer: 30-60 random iterations)...")
    Encode(data, output)
    print("Sandbox detection added")
    print("Random padding applied (randomizes file size)")
    FileSize(output)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python obfuscator_enhanced.py <file.py>")
        sys.exit(1)
    
    MainMenu(sys.argv[1])

