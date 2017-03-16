import sys
import logging
import socket
from tornado import iostream
from tornado import ioloop
import uuid
from tornado.options import define, options
import json
import ssl


def main():

    delim = '\r\n\r\n'

    def send_request():
        print "sending OK"
        stream.write("OK")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

    # stream = iostream.IOStream(s)
    stream = iostream.SSLIOStream(s, 
        ssl_options= dict(
            ca_certs="mycert.pem",
            cert_reqs=ssl.CERT_NONE))

    print "about to connect"
    stream.connect(('', 8013), send_request)

    ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()

