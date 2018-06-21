#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#
#

__author__ = '@nulls0'

import os, sys, urllib2
import cv2, numpy, threading

class MJPEGStream(object):
    def __init__(self, stream_url):
        self.stream_url = stream_url
        self.stream = urllib2.urlopen(self.stream_url)

        self.data = ''
        self.frame = None

        thread = threading.Thread(target=self.start)
        thread.daemon = True
        thread.start()

    def read(self):
        return self.frame

    def start(self):
        while True:
            self.data += self.stream.read(5120)

            start_pos = self.data.find('\xff\xd8')
            end_pos = self.data.find('\xff\xd9')

            if start_pos != -1 and end_pos != -1:
                self.frame = self.data[start_pos:end_pos+2]
                self.data = self.data[end_pos+2:]

class MJPEGStreamViewer(object):
    def __init__(self, stream):
        self.stream = stream

    def start(self):
        while True:
            frame = self.stream.read()
            if frame == None:
                continue

            frame = numpy.fromstring(frame, dtype=numpy.uint8)
            frame = cv2.resize(cv2.imdecode(frame, 1), (640, 480))
            cv2.imshow('MJPEG Stream Viewer', frame)

            if (cv2.waitKey(5) & 0xFF) == 27:
                sys.exit()

if __name__ == '__main__':
    app = MJPEGStreamViewer(MJPEGStream('http://208.72.70.171/mjpg/1/video.mjpg'))
    app.start()