import os 
import socket
import mimetypes

class TCPServer:
    """Base server class for handling TCP connections. 
    The HTTP server will inherit from this class.
    """

    def __init__(self, host='127.0.0.1', port=8888):
        self.host = host
        self.port = port

    def start(self):
        """Method for starting the server"""

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen(5)

        print("Listening at", s.getsockname())

        while True:
            conn, addr = s.accept()
            print("Connected by", addr)

            # This just reads the first 1024 bytes sent by the client
            data = conn.recv(1024)

            response = self.handleRequest(data)

            conn.sendall(response)
            conn.close()
    
    def handle_request(self, data):
        """Handles incoming data and returns a response.
        Override this in subclass.
        """
        return data
    
class HTTPServer(TCPServer):
    """The actual HTTP server class"""

    headers = {
        'Server': 'CrudeServer',
        'Content-Type': 'text/html',
    }

    status_codes = {
        200: 'OK',
        404: 'Not Found',
        501: 'Not Implemented',
    }

    def handle_request(self, data):
        """Handles incoming requests"""

        request = HTTPRequest(data)

class HTTPRequest:
    """Parser for HTTP requests.

    It takes raw data and extracts meaningful information about the incoming request.

    Instances of this class have the following attributes:
        self.method: The current HTTP request method sent by client (string)
        self.uri: URI for the current request (string)
        self.http_version = HTTP version used by  the client (string)
    """

    def __init__(self, data):
        self.method = None
        self.uri = None
        self.http_version = 1.1 # default to HTTP/1.1 if request doesnt provide a version

        # parse incoming data
        self.parse(data)
    
    def parse(self, data):
        alines = data.split(b'\r\n')

        request_line = lines[0]  # request line is the first line of the data

        # split request line into seperate words
        words = request_line.split(b' ')

        # call decode to convert bytes to string
        self.method = words[0].decode()

        if len(words) > 1:
            # we put this in if block because sometimes browsers
            # don't send URI with the request for homepage
            # call decode to convert bytes to string
            self.uri = words[1].decode()

        if len(words) > 2:
            # we put this in if block because sometimes browsers
            # don't send HTTP version
            self.http_version = words[2]


if __name__ == '__main__':
    print('Hello HTTP')
