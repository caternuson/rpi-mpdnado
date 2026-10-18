# mpdnado

A simple web interface for mpd using Tornado, providing:

  * Start/stop playback control
  * Volume control
  * Status info dump

# Requirements

  * a system running:
    * [mpd](https://www.musicpd.org)
    * [Python](https://www.python.org/)
  * A Python venv with:
    * [Tornado](https://www.musicpd.org/)
    * [python-mpd2](https://github.com/Mic92/python-mpd2)
  * [Bootstrap](https://getbootstrap.com/) and [jQuery](https://jquery.com/) are included locally

# Systemd
Here's a basic systemd unit file that can be placed in `/etc/systemd/system/mpdnado.service`:
```
[Unit]
Description=MPD Web Server

[Service]
ExecStart=/home/pi/env/bin/python3 /home/pi/rpi-mpdnado/mpdnado.py

[Install]
WantedBy=multi-user.target
```



