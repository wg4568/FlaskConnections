import connections, random

server = connections.Server(host="0.0.0.0", port=5000, debug=True)

server.add_link("random", random.randint)

server.start()