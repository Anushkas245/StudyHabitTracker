from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser

PORT = 8000
server_address = ('', PORT)
httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
print(f"Serving HTTP on port {PORT}...")
print(f"Open http://localhost:{PORT} in your browser")
webbrowser.open(f'http://localhost:{PORT}')
httpd.serve_forever()
