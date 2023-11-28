import os
import mpd
import tornado.httpserver
import tornado.web

PORT = 8080
PLAYLIST = "boxy"
TRACK = 0
DEBUG = False

def DBG(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

#--------------------------------------------------------------------
# M P D
#--------------------------------------------------------------------
mpc = mpd.MPDClient()

def mpd_init():
    """Initialize MPD."""
    mpc.connect("localhost", 6600)
    mpc.stop()
    mpc.clear()
    mpc.load(PLAYLIST)
    mpc.close()
    mpc.disconnect()

def mpd_stop():
    """Stop playback."""
    try:
        mpc.connect("localhost", 6600)
        mpc.stop()
        mpc.close()
        mpc.disconnect()
    except:
        pass

def mpd_play(track=None):
    """Play specified track index."""
    try:
        mpc.connect("localhost", 6600)
        if track is not None:
            mpc.play(track)
        else:
            mpc.play()
        mpc.close()
        mpc.disconnect()
    except:
        pass

def mpd_change_vol(amount):
    """Change volume by amount in percent."""
    try:
        mpc.connect("localhost", 6600)
        mpc.volume(amount)
        mpc.close()
        mpc.disconnect()
    except:
        pass

#--------------------------------------------------------------------
# T O R N A D O
#--------------------------------------------------------------------
class RootHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("mpdnado.html")

class ButtonHandler(tornado.web.RequestHandler):
    def get(self):
        btn_uri = self.request.uri
        DBG("BUTTON HANDLER: ", btn_uri)
        if "btn_b1" in btn_uri:
            DBG("button1")
            mpd_stop()
        if "btn_b2" in btn_uri:
            DBG("button2")
            mpd_play(TRACK)
        if "btn_b3" in btn_uri:
            DBG("button3")
            mpd_change_vol(10)
        if "btn_b4" in btn_uri:
            DBG("button4")
            mpd_change_vol(-10)

class MainServerApp(tornado.web.Application):
    """Main Server application."""
    def __init__(self):
        handlers = [
            (r"/", RootHandler),
            (r"/btn_b1", ButtonHandler),
            (r"/btn_b2", ButtonHandler),
            (r"/btn_b3", ButtonHandler),
            (r"/btn_b4", ButtonHandler),
        ]

        settings = {
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
            "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        }

        tornado.web.Application.__init__(self, handlers, **settings)

#--------------------------------------------------------------------
# M A I N
#--------------------------------------------------------------------
if __name__ == '__main__':
    mpd_init()
    tornado.httpserver.HTTPServer(MainServerApp()).listen(PORT)
    print("Server starting on", PORT)
    tornado.ioloop.IOLoop.instance().start()