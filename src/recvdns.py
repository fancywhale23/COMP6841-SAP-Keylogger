from binascii import a2b_hex, b2a_hex
import re
import socket
from dnslib import DNSRecord
import base64

hist = set()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 53))

while True:
    data, addr = sock.recvfrom(2048)

    try:
        msg = DNSRecord.parse(a2b_hex(b2a_hex(data)))
    except Exception as e:
        print(e)
        continue

    m = re.search(r'\;(\S+)\.qqq\.wergm\.uk', str(msg), re.MULTILINE)
    if m:
        payload = m.group(1)
        try:
            decoded = base64.b64decode(payload.encode("ascii")).decode("ascii")
            # Only print unique messages to filter out repeated DNS requests
            if decoded not in hist:
                hist.add(decoded)
                print(decoded)
        except:
            print(payload)