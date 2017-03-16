import tornado.web
import tornado.httpserver
import select
import socket
import tornado.iostream
import random
import logging
import ssl
import errno
import functools


class SSLSocketServer(object):

    def __init__(self, io_loop=None, config_file=None, debug=False):
        if io_loop is None: io_loop = tornado.ioloop.IOLoop.instance()

        # Set up our node-accepting socket on port 8013
        HOST = ''                 # Symbolic name meaning all available interfaces
        PORT = 8013               # Arbitrary non-privileged port

        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.setblocking(0)

        server_sock.bind((HOST, PORT))
        # We allow a backlog of up to 128 pending connections.
        server_sock.listen(128)

        callback = functools.partial(self.connection_ready, server_sock)
        io_loop.add_handler(server_sock.fileno(),
            callback, io_loop.READ)

    def connection_ready(self, sock, fd, events):
        # In part from: https://github.com/saucelabs/monocle/blob/7bd978f1c6a2ad3d78dd3da0b5b73c3e215ebbf3/monocle/tornado_stack/network/__init__.py
        while True:

            # Wait for the basic socket to be available.
            try:
                node_sock, address = sock.accept()
            except socket.error, e:
                if e.args[0] not in (errno.EWOULDBLOCK, errno.EAGAIN):
                    raise
                return

            # Wait for the ssl socket to be available.
            try:
                node_sock = ssl.wrap_socket(node_sock,
                            do_handshake_on_connect=False,
                            server_side=True,
                            certfile="mycert.pem",
                            ssl_version=ssl.PROTOCOL_TLSv1)
            except ssl.SSLError, err:
                if err.args[0] == ssl.SSL_ERROR_EOF:
                    s.close()
                    return
                else:
                    raise
            except socket.error, err:
                if err.args[0] == errno.ECONNABORTED:
                    s.close()
                    return
                else:
                    raise

            node_io_stream = tornado.iostream.SSLIOStream(node_sock)

            def on_ok(data):
                print "received OK!"
            node_io_stream.read_until("OK", on_ok)


if __name__ == '__main__':
    # Get a handle to the instance of IOLoop
    io_loop = tornado.ioloop.IOLoop.instance()
    worker = SSLSocketServer(io_loop)
    # Start the IOLoop
    io_loop.start()

