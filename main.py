import http.server
import socketserver
import os
import json

PORT = 8080

items = [
    {"name": "Bob"},
    {"name": "Alex"},
]

class CustomHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        root_directory = os.path.join(os.getcwd(), "public")
        path = self.path[1:] if self.path != "/" else "index.html"

        if path.startswith('api/'):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            self.wfile.write(json.dumps(items).encode())
        
        else:
            file_path = os.path.join(root_directory, path)

            if os.path.exists(file_path):
                with open(file_path, "rb") as file:
                    file_content = file.read()

                if file_path.endswith(".html"):
                    content_type = "text/html"
                elif file_path.endswith(".css"):
                    content_type = "text/css"
                else:
                    content_type = "application/octet-stream"

                self.send_response(200)
                self.send_header("Content-type", content_type)
                self.end_headers()

                self.wfile.write(file_content)
            else:
                self.send_error(404, "File Not Found: %s" % self.path)


with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print("Server started at port", PORT)
    httpd.serve_forever()
