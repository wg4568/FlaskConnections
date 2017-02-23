def root_var(var):
	new = None
	try:
		new = int(var)
	except Exception:
		try:
			new = float(var)
		except Exception:
			new = str(var)
	return new

class Server:
	def __init__(self, host, port, debug=False):
		self.flask = __import__("flask")
		self.debug = debug
		self.host = host
		self.port = port
		self.links = {}
		self.app = self.flask.Flask(__name__)
		@self.app.route("/", methods=["GET"])
		def index():
			divs = ""
			for link in self.links:
				divs += self.render_link(link)
			return self.flask.render_template("index.html", divs=divs)

		@self.app.route("/send", methods=["POST"])
		def send():
			name = self.flask.request.args.get("link")
			func = self.links[name]
			args = func.__code__.co_varnames
			data = {}
			func_dat = []
			for arg in args:
				data[arg] = self.flask.request.args.get(arg)
				func_dat.append(None)
			for arg in args:
				func_dat[args.index(arg)] = root_var(data[arg])
			return str(func(*func_dat))


	def add_link(self, name, func):
		self.links[name] = func

	def render_link(self, name):
		args = self.links[name].__code__.co_varnames

		data = "'?' +"
		for arg in args:
			data += "'%s=' + $('#%s_%s_input').val() +'&'+" % (arg, arg, name)
		print data
		data += "'link=%s'" % (name)

		script = """
		<script>
		function %s_submit() {
			data = %s;
			console.log(data);
			$.ajax({
				url:'send' + data,
				type:'post',
				success:function(response){
					console.log(response);
					if (response) {
						$('#%s_output').html(response);
					} else {
						$('#%s_output').html("None");					
					}
				},
				error:function() {
					$('#%s_output').html("ERROR");
				}
			});
		}
		</script>
		""" % (name, data, name, name, name)

		inputs = ''
		for arg in args:
			inp = "<input placeholder='%s' id='%s_%s_input' width='500px'><br/><br/>" % (arg, arg, name)
			inputs += inp

		submit = "<button onclick='%s_submit()'>run '%s'</button>&nbsp<p class='output' id='%s_output'>None</p>" % (name, name, name)

		return script + "<div class='input ui-widget-content'><h3>%s</h3>" % (name) + inputs + submit + "</div>"

	def start(self):
		self.app.run(self.host, self.port, debug=self.debug)