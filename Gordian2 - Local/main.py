"""
Main Gordian file; runs at localhost:9000

"""
from graph_creator import create_graph, get_crossings, get_edges
from fundamental_set_cycles import find_fund_set
from all_cycles import find_all_cycles, dictify_cycles
from links import find_links
from knots import find_knots


from links import listify
from links import find_links
from functools import cached_property
from urllib.parse import parse_qsl, urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import http.server
from http.cookies import SimpleCookie
import numpy as np

"""
Full integration of all other files
"""
def Gordian(graph_filepath):
    if graph_filepath != 'favicon.ico':
        print("================ Graph_filepath ================ ", graph_filepath)
        graph  = create_graph("./Graph data files/" + graph_filepath)
        graph_edges = get_edges("./Graph data files/" + graph_filepath)
        crossings = get_crossings("./Graph data files/" + graph_filepath, graph)
        fundamental_set_cycles = find_fund_set(graph, graph_edges)
        all_cycles = find_all_cycles(dictify_cycles(fundamental_set_cycles))
        links = find_links(all_cycles, crossings)
        # FOR WHEN KNOT FUNCTION IS MADE:
        find_knots(all_cycles, crossings)
        return links
        # return {links: knots}    , then integrate as key/values into html

"""
HTTPServer Handler
"""
class handler(BaseHTTPRequestHandler):
    @cached_property
    def url(self):
        return urlparse(self.path)

    @cached_property
    def query_data(self):
        return dict(parse_qsl(self.url.query))

    @cached_property
    def post_data(self):
        content_length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(content_length)

    @cached_property
    def form_data(self):
        return dict(parse_qsl(self.post_data.decode("utf-8")))

    @cached_property
    def cookies(self):
        return SimpleCookie(self.headers.get("Cookie"))

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        self.wfile.write(bytes("<html><head><title>Gordian 2.</title></head>", "utf-8"))
        self.wfile.write(bytes("<body><p>Input graph data file as path in URL. (ex: localhost:9090/k7.txt) </p>", "utf-8"))
        self.wfile.write(bytes("<p>You accessed file: %s</p>" % self.path[1:], "utf-8"))

        graph_filepath = self.path[1:]
        links = Gordian(graph_filepath)
        for link in links:
            self.wfile.write(bytes("<p>%s</p>" %str(link), "utf-8"))

        self.wfile.write(bytes('There are: ' + str(len(links)) + ' links', "utf-8"))

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        message = "Hello, World! Here is a POST response"
        self.wfile.write(bytes(message, "utf8"))


"""
Server executiion
"""
host = 'localhost'
port = 8080
try:
    server = http.server.HTTPServer((host, port), handler)
    print('Started server. Running Gordian 2')
    server.serve_forever()
except KeyboardInterrupt:
    print('^C received, shutting down server')
    server.socket.close()
