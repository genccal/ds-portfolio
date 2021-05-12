from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os


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

            # dump json to directory 'parsed'
            os.makedirs("parsed", exist_ok=True)
            store_path = os.path.join(os.curdir, "parsed/#")
            with open(store_path + vehicle["id"] + ".json", "w") as fh:
                json.dump(vehicle, fh)

            self.send_response(200)
            self.end_headers()
        
        else:
            self.send_response(400)
            self.end_headers()


httpd = HTTPServer(("localhost", 3000), S)
httpd.serve_forever()
