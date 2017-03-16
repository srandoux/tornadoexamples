import tornado
import tornado.web
import tornado.httpserver
import tornado.ioloop
#key generation
#openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout mycert.pem -out mycert.pem
#test:
#curl -X POST -v -k https://localhost:8080
class Docker(tornado.web.RequestHandler):
  def post(self, *args, **kwargs):
	self.write('1\n')

application = tornado.web.Application(
	handlers=[
	(r'/', Docker),
	],
	debug=True,
	)

if __name__ == '__main__':
	ssl_options={'certfile': 'mycert.pem',
	'keyfile': 'mycert.pem'}
	srv = tornado.httpserver.HTTPServer(application, xheaders=True, ssl_options=ssl_options)
	srv.bind(8080)
	srv.start()
	tornado.ioloop.IOLoop.instance().start()

