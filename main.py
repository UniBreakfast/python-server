import http.server
import socketserver
import os
import json

PORT = 8080

tasks = [
    {"id": 1, "task": "Buy groceries", "done": True},
    {"id": 2, "task": "Read a book", "done": False},
    {"id": 3, "task": "Go for a walk", "done": False},
    {"id": 4, "task": "Practice coding", "done": False},
]

class CustomHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        root_directory = os.path.join(os.getcwd(), "public")
        path = self.path[1:] if self.path != "/" else "index.html"

        if path.startswith('api/'):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(tasks).encode())
        
        else:
            file_path = os.path.join(root_directory, path)

            if os.path.exists(file_path):
                with open(file_path, "rb") as file:
                    file_content = file.read()

                if file_path.endswith(".html"):
                    content_type = "text/html"
                elif file_path.endswith(".css"):
                    content_type = "text/css"
                elif file_path.endswith(".js"):
                    content_type = "application/javascript"
                else:
                    content_type = "application/octet-stream"

                self.send_response(200)
                self.send_header("Content-type", content_type)
                self.end_headers()

                self.wfile.write(file_content)
            else:
                self.send_error(404, "File Not Found: %s" % self.path)

    def do_PATCH(self):
        if not self.path.startswith('/api/'):
            self.send_error(404, "Not Found")
            return
        
        # path = self.path[5:]
        payload = self.get_payload()
        data = json.loads(payload)
        
        id = data.get('id', None)
        done = data.get('done', None)
        
        if id is None or done is None:
            self.send_error(400, "Bad Request")
            return
        
        for item in tasks:
            if item['id'] == id:
                item['done'] = done
                break
                        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps(tasks).encode())

    def get_payload(self):
        return self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8')
        

server = socketserver.TCPServer(("", PORT), CustomHandler)

with server:
    print(f"Server started at http://localhost:{PORT}")
    server.serve_forever()
