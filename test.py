import connections, random

def random_num(min, max):
	return random.randint(min, max)

server = connections.Server(host="0.0.0.0", port=5000, debug=True)

server.add_link("random", random_num)

server.start()