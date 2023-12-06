# mpdnado

A simple web interface for mpd using Tornado, providing:

  * Start/stop playback control
  * Volume control
  * Playlist viewing and selecting (but no editting)
  * "now playing" info

# Requirements

  * a system running [mpd](https://www.musicpd.org)
  * [Python](https://www.python.org/)
  * [Tornado](https://www.musicpd.org/)
  * [python-mpd2](https://github.com/Mic92/python-mpd2)

# Comments

The interface is intentionally kept simple, providing only a few basic
actions. It's assumed most of the mpd configuration, like creating
playlist, etc. has already been done.

To keep the requirements minimal, all CSS and JavaScript is written
from scratch. So intentionally **not** using any of the many available
CSS (bootstrap, etc.) frameworks or JavaScript (jquery, etc.) libraries.