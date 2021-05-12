from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import redis

conn = redis.Redis("localhost", port=6379)


class S(BaseHTTPRequestHandler):
    def do_POST(self):
        content_len = int(self.headers["Content-Length"])
        body = self.rfile.read(content_len)
        data = json.loads(body)

        if data.get("log",0)!=0:
            # parse the text into dict
            vehicle = dict()
            for part in data["log"].split():
                key, value = part.split("=")
                vehicle[key] = value

            # push the json to redis list
            conn.rpush(9, json.dumps(vehicle))

            self.send_response(200)
            self.end_headers()
        
        else:
            self.send_response(400)
            self.end_headers()


httpd = HTTPServer(("localhost", 3000), S)
httpd.serve_forever()
