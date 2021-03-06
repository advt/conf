#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import collections

from i3pystatus import Status


class MySettings(collections.MutableMapping):

    def __init__(self, settings_file=None, *args, **kwargs):
        """Settings object for retreiving personal user data for i3pystatus.

        Usage:

        .. code-block:: python

            >>> settings = MySettings()
            >>> settings.get("weather")
            { "weather": { "location_code": "USCA0001", "units": "imperial" }}

            >>> settings = MySettings(settings_file="/path/to/config.json")
            >>> settings.get("weather")
            { "weather": { "location_code": "USCA0001", "units": "imperial" }}

        :param settings_file: Location of JSON config file.
        :type settings_file: string

        """

        super(MySettings, self).__init__(*args, **kwargs)

        if not settings_file:
            settings_file = os.path.expanduser('~/.i3/local_settings.json')

        self.settings_file = settings_file

        if os.path.isfile(settings_file):
            self._data = json.loads(open(settings_file).read())
        else:
            self._data = {}

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value
        self.dirty = True

    def __delitem__(self, key):
        del self._data[key]
        self.dirty = True

    def keys(self):
        """Return list of keys."""
        return self._data.keys()

    def __iter__(self):
        return self._data.__iter__()

    def __len__(self):
        return len(self._data.keys())


# Load settings from ``$HOME/.i3/local_settings.json
my_settings = MySettings()


# Initialize i3pystatus instance
status = Status(standalone=True)

# Shows pulseaudio default sink volume
#"color": "#FF0000"
# Note: requires libpulseaudio from PyPI
status.register("pulseaudio",
				format="♪: {volume}%",
				format_muted="Mute",)

# Displays clock like this: # Tue 30 Jul 11:59:46 PM KW31
#               format="%a %-d %b %l:%M%p %Z",
#                          ^-- calendar week

status.register("clock",
				format="%a %-d %b %X",
                color="#CCCCCC",)

status.register("clock",
				format="Paris: %H:%M",
                timezone="Europe/Paris",
				interval=5,
				color="#028482",)

# Shows disk usage of /
# Format:
# 42/128G [86G]
status.register("disk",
                path="/home",
                format="/home: {avail}G",
                color="#FFF168",)

status.register("disk",
                path="/",
                format="/: {avail}G",
                color="#FFF168",)

# This would look like this:
# Discharging 6h:51m
status.register("battery",
                format="{status} {percentage:.2f}% {remaining:%E%hh:%Mm}",
                alert=True,
                alert_percentage=20,
                status={
                    "DIS":  "DIS",
                    "CHR":  "CHR",
                    "FULL": "FULL",
                },)

# Shows the average load of the last minute and the last 5 minutes
# (the default value for format is used)
status.register("load",
				format="Load: {avg1}",)

# Shows your CPU temperature, if you have a Intel CPU
status.register("temp",
                format="{temp:.0f}°C",)

status.register("mem_bar",
                format="Mem usage: {used_mem_bar}",)

# The battery monitor has many formatting options, see README for details

# This would look like this, when discharging (or charging)
# ↓14.22W 56.15% [77.81%] 2h:41m
# And like this if full:
# =14.22W 100.0% [91.21%]
#
# This would also display a desktop notification (via dbus) if the percentage
# goes below 5 percent while discharging. The block will also color RED.
#status.register("battery",
#                format="{status}/{consumption:.2f}W {percentage:.2f}% [{percentage_design:.2f}%] {remaining:%E%hh:%Mm}",
#                alert=True,
#                alert_percentage=20,
#                status={
#                    "DIS": "↓",
#                    "CHR": "↑",
#                    "FULL": "=",
#                },)

# Displays whether a DHCP client is running
status.register("runwatch",
                name="DHCP",
                path="/var/run/dhclient*.pid",)

# Shows the address and up/down state of eth0. If it is up the address is shown in
# green (the default value of color_up) and the CIDR-address is shown
# (i.e. 10.10.10.42/24).
# If it's down just the interface name (eth0) will be displayed in red
# (defaults of format_down and color_down)
#
# Note: the network module requires PyPI package netifaces-py3
status.register("network",
                interface="eth0",
                format_up="{v4cidr}",)

# Has all the options of the normal network and adds some wireless specific things
# like quality and network names.
#
# Note: requires both netifaces-py3 and basiciw
status.register("wireless",
                interface="wlan0",
                format_up="{essid} {quality:03.0f}% {v4cidr}",)

# Shows weather
#if my_settings.get('weather'):♪: {volume}
#    status.register("weather",
#                    **my_settings.get('weather')
#                    )

# Shows mpd status
# Format:
# Cloud connected▶Reroute to Remain
#status.register("mpd",
#                format="{title} {status} {album}",
#                status={
#                    "pause": "▷",
#                    "play": "▶",
#                    "stop": "◾",
 #               },)

from i3pystatus.mail import imap

status.register("mail",
    backends=[
        imap.IMAP(
             # port and ssl are the defaults
             host="imap.googlemail.com", port=993, ssl=True,
             username="", password="", 
            )
    ],
    email_client="icedove",
    interval=300)

status.register("countdown",
				date="23-12-2014",
                format="{days} days left",
                interval=300,
                )

status.register("countdown",
				date="01-10-2014",
                format="{days} days passed",
                interval=300,
                )

status.run()
