from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import redis
from rq import Queue
import background

r = redis.Redis("localhost", port=6379)
q = Queue(connection=r)


class S(BaseHTTPRequestHandler):
    def do_POST(self):
        content_len = int(self.headers["Content-Length"])
        body = self.rfile.read(content_len)
        data = json.loads(body)

        if data.get("log",0)!=0:
            # add the text to the background task
            task = q.enqueue(background.background_task, data)

            self.send_response(200)
            self.end_headers()
        
        else:
            self.send_response(400)
            self.end_headers()


httpd = HTTPServer(("localhost", 3000), S)
httpd.serve_forever()
