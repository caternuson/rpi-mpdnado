import os
import mpd
import tornado.httpserver
import tornado.web

WEB_PORT = 8081
MPD_PORT = 6600
DEBUG = True

def DBG(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

#--------------------------------------------------------------------
# M P D
#--------------------------------------------------------------------
mpc = mpd.MPDClient()

def mpd_status():
    try:
        mpc.connect("localhost", MPD_PORT)
        status = mpc.status()
        mpc.close()
        mpc.disconnect()
        return status
    except:
        pass

def mpd_stop():
    """Stop playback."""
    try:
        mpc.connect("localhost", MPD_PORT)
        mpc.stop()
        mpc.close()
        mpc.disconnect()
    except:
        pass

def mpd_play(track=None):
    """Play specified track index."""
    try:
        mpc.connect("localhost", MPD_PORT)
        if track is not None:
            mpc.play(track)
        else:
            mpc.play()
        mpc.close()
        mpc.disconnect()
    except:
        pass

def mpd_toggle():
    try:
        if mpd_status()['state']=='play':
            mpd_stop()
        else:
            mpd_play()
    except:
        pass

def mpd_set_vol(level):
    """Change volume by amount in percent."""
    try:
        mpc.connect("localhost", MPD_PORT)
        mpc.setvol(level)
        mpc.close()
        mpc.disconnect()
    except:
        pass

def mpd_get_current_song(item):
    try:
        mpc.connect("localhost", MPD_PORT)
        info =  mpc.currentsong()
        mpc.close()
        mpc.disconnect()
        return info.get(item, "unknown")
    except:
        pass

#--------------------------------------------------------------------
# T O R N A D O
#--------------------------------------------------------------------
class RootHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("mpdnado.html")

class XHRHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        DBG("XHR: ", end='')
        try:
            params = self.request.arguments
            for command, value in params.items():
                command = command.strip().upper()
                DBG(" command={}, value={}".format(command, value))
                if command=="PLAY":
                    DBG("PLAY")
                    mpd_toggle()
                if command=="VOLUME":
                    level = int(value[0])
                    DBG("VOLUME {}".format(level))
                    mpd_set_vol(level)
                if command=="SONG":
                    DBG("SONG")
                    self.write(mpd_get_current_song('title'))
        except:
            DBG("NO ARG")

class MainServerApp(tornado.web.Application):
    """Main Server application."""
    def __init__(self):
        handlers = [
            (r"/", RootHandler),
            (r"/xhr", XHRHandler)
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
    tornado.httpserver.HTTPServer(MainServerApp()).listen(WEB_PORT)
    print("Server starting on", WEB_PORT)
    tornado.ioloop.IOLoop.instance().start()