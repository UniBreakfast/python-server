import http.server
import socketserver
import os
import json

from user import User, Task

PORT = 8080

tasks = [
    {"id": 1, "text": "Buy groceries", "done": True},
    {"id": 2, "text": "Read a book", "done": False},
    {"id": 3, "text": "Go for a walk", "done": False},
    {"id": 4, "text": "Practice coding", "done": False},
]

egor: User = User("Egor", 0)
egor.from_dict(tasks)

misha = User("Misha", 1)
misha.from_dict(tasks)

users = [egor, misha]

class CustomHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        root_directory = os.path.join(os.getcwd(), "public")
        path = self.path[1:] if self.path != "/" else "index.html"

        if path.startswith('api/'):
            endpoint = path.split('/')
            print(endpoint)

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            match endpoint[1]:
                case 'users': 
                    payload = self.get_users()
                case 'tasks':
                    payload = self.get_tasks(int(endpoint[2]))

            return self.wfile.write(json.dumps(payload, default=Task.to_dict).encode())
        
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
        
        payload = self.get_payload()
        data = json.loads(payload)
        
        userId = data.get('userId', None)
        taskId = data.get('taskId', None)
        done = data.get('done', None)
        
        if any([userId is None, taskId is None, done is None]):
            self.send_error(400, "Bad Request")
            return
        
        user = users[userId]
        task = next((task for task in user.tasks if task.id == taskId), None)
        task.done = done
                        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps(user.tasks, default=Task.to_dict).encode())

    def do_DELETE(self):
        if not self.path.startswith('/api/'):
            self.send_error(404, "Not Found")
            return
        
        payload = self.get_payload()
        data = json.loads(payload)
        
        userId = data.get('userId', None)
        taskId = data.get('taskId', None)
        
        if any([userId is None, taskId is None]):
            self.send_error(400, "Bad Request")
            return
        
        user = users[userId]
        user.tasks = [task for task in user.tasks if task.id != taskId]

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps(user.tasks, default=Task.to_dict).encode())

    def get_users(self):
        return [{k: v for k, v in user.__dict__.items() if k != 'tasks'} for user in users]

    def get_tasks(self, user_id):
        return users[user_id].tasks

    def get_payload(self):
        return self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8')
        

server = socketserver.TCPServer(("", PORT), CustomHandler)

with server:
    print(f"Server started at http://localhost:{PORT}")
    server.serve_forever()
