#----------------------------------------------------------
# Simple mpd web interface.
#
# carter nelson
# 2026/10/06
#----------------------------------------------------------

import os
import json
import mpd
import asyncio
import tornado

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

def mpd_get_current_song(item=None):
    try:
        mpc.connect("localhost", MPD_PORT)
        info =  mpc.currentsong()
        mpc.close()
        mpc.disconnect()
        if item:
            return info.get(item, "unknown")
        else:
            return info
    except:
        pass

def mpd_get_playlist():
    try:
        mpc.connect("localhost", MPD_PORT)
        # a list of dicts per play list item
        playlist = mpc.playlistid()
        mpc.close()
        mpc.disconnect()
        # only return "name" info, truncated
        return [item.get('name', 'unknown')[:30] for item in playlist]
    except:
        pass

#--------------------------------------------------------------------
# T O R N A D O
#--------------------------------------------------------------------
class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("mpdnado.html")

    def post(self):
        request_info = json.loads(self.request.body)
        CMD = request_info.get("CMD").strip().upper()
        PAR = request_info.get("PAR", None)
        if "STA"==CMD:
            self.write(json.dumps(mpd_status()))
        elif "TOG"==CMD:
            mpd_toggle()
            self.write(json.dumps(mpd_status()))
        elif "VOL"==CMD:
            mpd_set_vol(PAR.get("level"))
            self.write(json.dumps(mpd_status()))
        elif "LIS"==CMD:
            self.write(json.dumps(mpd_get_playlist()))
        elif "PLY"==CMD:
            mpd_play(int(PAR))
            self.write(json.dumps(mpd_status()))
        elif "CUR"==CMD:
            self.write(json.dumps(mpd_get_current_song()))
        else:
            print("Unknown request:", CMD, PAR)

async def main():
    handlers = [
        (r"/", MainHandler),
    ]
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "template_path": os.path.join(os.path.dirname(__file__), "static"),
    }
    app = tornado.web.Application(handlers, **settings)
    app.listen(WEB_PORT)
    print(f"Server started on {WEB_PORT}...")
    shutdown_event = asyncio.Event()
    await shutdown_event.wait()

#--------------------------------------------------------------------
# M A I N
#--------------------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(main())