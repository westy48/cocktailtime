#!/usr/bin/env python

import time
import motephat as mote
import tweepy
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener

# Insert your own Twitter consumer and access keys here:
ckey = 'YOURCONSUMERKEY'
csecret = 'YOURCONSUMERSECRET'
atoken = 'YOURACCESSTOKEN'
asecret = 'YOURACCESSSECRET'

mote.configure_channel(1, 16, False)
mote.configure_channel(2, 16, False)
mote.configure_channel(3, 16, False)
mote.configure_channel(4, 16, False)

colors = [
    (255,   0,   0),
    (0,   255,   0),
    (0,     0, 255),
    (255, 255, 255)
]

class listener(StreamListener):
    def on_data(self, data):
        cocktailtime()
        return True

def cocktailtime():
    mote.clear()
    for step in range(4):
        for channel in range(4):
            for pixel in range(mote.get_pixel_count(channel + 1)):
                r, g, b = colors[channel]
                mote.set_pixel(channel + 1, pixel, r, g, b)
                mote.show()
                time.sleep(0.01)
        colors.append(colors.pop(0))
    for channel in range(1, 5):
        for pixel in range(16):
            mote.set_pixel(channel, pixel, 255, 0, 0)
            mote.show()
            time.sleep(0.001)
    for channel in range(1, 5):
        for pixel in range(16):
            mote.set_pixel(channel, pixel, 0, 255, 0)
            mote.show()
            time.sleep(0.001)
    for channel in range(1, 5):
        for pixel in range(16):
            mote.set_pixel(channel, pixel, 0, 0, 255)
            mote.show()
            time.sleep(0.001)
    for channel in range(1, 5):
        for pixel in range(16):
            mote.set_pixel(channel, pixel, 255, 255, 255)
            mote.show()
            time.sleep(0.001)
# this bit fades the Motes down - is there a more elegant way?
    try:
        b = 255
        while b >= 0:
            for channel in range(1, 5):
                for pixel in range(16):
                    mote.set_pixel(channel, pixel, b, b, b)
            mote.show()
            b -= 1
    finally:
        mote.clear()
        mote.show()

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth)
twitterstream = Stream(auth, listener())
twitterstream.filter(track=['#cocktailtime'])
