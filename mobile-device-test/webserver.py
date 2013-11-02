#!/usr/bin/env python
import tornado.web
import tornado.websocket
import tornado.ioloop
import ADIS
import FC
import os

static_path = os.path.join(os.path.dirname(__file__), 'static')
template_path = os.path.join(os.path.dirname(__file__), 'templates')

# Fake ADIS device
adis = ADIS.SensorDevice()


# index page
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html', actions=FC.actions)

    def post(self):
        btn = self.get_argument('action', '')

        action = FC.actions[int(btn)].get('run')
        if action is not None:
            message = action()
            if message is not None:
                print message
            else:
                print "no responce"

        self.render('index.html', actions=FC.actions)


# mobile page
class MobileHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('mobile.html')

class FrontEndWebSocket(tornado.websocket.WebSocketHandler):

    clients = []

    def open(self):
        if self not in self.clients:
            self.clients.append(self)

    def on_message(self, message):
        adis.send_message(message)

    def on_close(self):
        if self in self.clients:
            self.clients.remove(self)


if __name__ == "__main__":

    # setup
    application = tornado.web.Application([
            (r'/', MainHandler),
            (r'/mobile', MobileHandler),
            (r'/ws', FrontEndWebSocket)
        ], template_path=template_path, static_path=static_path)
    application.listen(5000)

    # Start
    tornado.ioloop.IOLoop.instance().start()

