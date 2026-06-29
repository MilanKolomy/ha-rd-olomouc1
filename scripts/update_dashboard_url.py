"""
Změní url_path dashboardu přes HA WebSocket API.
Spustit na HA: python3 /tmp/update_dashboard_url.py
"""
import socket, struct, os, json, base64

HOST = 'localhost'
PORT = 8123
TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI4MTYwNzI0N2E0YWI0ZGM4ODA1NDdhZjc4ZTY2NzlmZSIsImlhdCI6MTc4MjI4MTc0MiwiZXhwIjoyMDk3NjQxNzQyfQ.9naAxzzfU2hkbK8IGLBykLXGIjoF3mgJQ_Xz1FTpyH4'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.settimeout(20)

key = base64.b64encode(os.urandom(16)).decode()
s.sendall((
    "GET /api/websocket HTTP/1.1\r\n"
    f"Host: {HOST}:{PORT}\r\n"
    "Upgrade: websocket\r\n"
    "Connection: Upgrade\r\n"
    f"Sec-WebSocket-Key: {key}\r\n"
    "Sec-WebSocket-Version: 13\r\n"
    "\r\n"
).encode())

buf = b''
while b'\r\n\r\n' not in buf:
    buf += s.recv(4096)
_leftover = buf[buf.index(b'\r\n\r\n') + 4:]

def _read(n):
    global _leftover
    while len(_leftover) < n:
        _leftover += s.recv(4096)
    chunk, _leftover = _leftover[:n], _leftover[n:]
    return chunk

def recv_frame():
    hdr = _read(2)
    length = hdr[1] & 0x7f
    if length == 126:
        length = struct.unpack('>H', _read(2))[0]
    elif length == 127:
        length = struct.unpack('>Q', _read(8))[0]
    return json.loads(_read(length).decode('utf-8'))

def send_frame(msg):
    data = json.dumps(msg, ensure_ascii=False).encode('utf-8')
    mk = os.urandom(4)
    masked = bytes(b ^ mk[i % 4] for i, b in enumerate(data))
    frame = bytearray([0x81])
    l = len(data)
    if l < 126:
        frame.append(0x80 | l)
    elif l < 65536:
        frame.append(0x80 | 126)
        frame.extend(struct.pack('>H', l))
    else:
        frame.append(0x80 | 127)
        frame.extend(struct.pack('>Q', l))
    frame.extend(mk)
    frame.extend(masked)
    s.sendall(bytes(frame))

msg = recv_frame()
print('1)', msg.get('type'))

send_frame({'type': 'auth', 'access_token': TOKEN})
msg = recv_frame()
print('2)', msg.get('type'))
if msg.get('type') != 'auth_ok':
    print('AUTH FAILED:', msg)
    s.close()
    exit(1)

send_frame({
    'id': 1,
    'type': 'lovelace/dashboards/update',
    'dashboard_id': 'dashboard_dashboard',
    'url_path': 'home',
    'title': 'Home',
    'icon': 'mdi:home',
    'show_in_sidebar': True,
    'require_admin': False,
})
msg = recv_frame()
print('3) update result:', msg)

s.close()
