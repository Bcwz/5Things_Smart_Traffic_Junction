import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        # print(self.data)
        print(self.data.upper())
        
        # just send back the same data, but upper-cased
        data = "Helo"
        self.request.sendall(bytes(data, 'UTF-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 1883

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        print("Server up!")
        server.serve_forever()