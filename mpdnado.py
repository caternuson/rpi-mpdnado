import os
import mpd
import tornado.httpserver
import tornado.web

PORT = 8080
PLAYLIST = "boxy"

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

def mpd_status():
    """Return status dictionary or None."""
    try:
        mpc.connect("localhost", 6600)
        status = mpc.status()
        mpc.close()
        mpc.disconnect()
        return status
    except:
        return None

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

def mpd_toggle():
    """Toggle play back. Play if stopped, stop if playing."""
    try:
        s = mpd_status()
        if s is not None:
            if s['state'] == 'play':
                mpd_stop()
            else:
                mpd_play()
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

class BtnStopHandler(tornado.web.RequestHandler):
    def get(self):
        print("STOP!")
        mpd_stop()

class BtnPlayHandler(tornado.web.RequestHandler):
    def get(self):
        print("PLAY!")
        mpd_play()

class BtnVolUpHandler(tornado.web.RequestHandler):
    def get(self):
        print("VOL+!")
        mpd_change_vol(10)

class BtnVolDnHandler(tornado.web.RequestHandler):
    def get(self):
        print("VOL-!")
        mpd_change_vol(-10)

class BtnVolDnHandler(tornado.web.RequestHandler):
    def get(self):
        print("VOL-!")
        mpd_change_vol(-10)

class MainServerApp(tornado.web.Application):
    """Main Server application."""

    def __init__(self):
        handlers = [
            (r"/", RootHandler),
            (r"/btn_stop", BtnStopHandler),
            (r"/btn_play", BtnPlayHandler),
            (r"/btn_volup", BtnVolUpHandler),
            (r"/btn_voldn", BtnVolDnHandler),
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
    tornado.httpserver.HTTPServer(MainServerApp()).listen(PORT)
    print("Server stating on", PORT)
    tornado.ioloop.IOLoop.instance().start()