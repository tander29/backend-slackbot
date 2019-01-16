#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Travis Anderson"

"""
This is for contacting twitter, and watching a specific user or word

"""
import logging
import signal
import tweepy
import time
import os
import datetime
from threading import Thread

logger = logging.getLogger(__file__)
exit_flag = False


def signal_handler(sig_num, frame):
    """Smooth exit from system"""
    global exit_flag
    logger.warning('Received exit signal number: {}'.format(str(sig_num)))
    if sig_num:
        exit_flag = True


def _start(self, is_async):
    self.running = True
    if is_async:
        logger.warning("Running Daemon thread")
        self._thread = Thread(
            target=self._run, name="Tweepy Thread", daemon=True)
        self._thread.start()
    else:
        self._run()


class WatchTwitter(tweepy.StreamListener):

    def __init__(self):
        logger.info("Creating api")
        consumer_key = os.getenv("API_KEY")
        assert consumer_key is not None
        consumer_secret = os.getenv("API_SECRET")
        access_token = os.getenv("ACCESS_TOKEN")
        access_token_secret = os.getenv("ACCESS_SECRET")
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
        logger.warning("Did a monkey patch, could use a demo on this")
        tweepy.Stream._start = _start

    def start_stream(self, find_string):
        logger.info('Found string: {}'.format(find_string))
        self.stream = tweepy.Stream(auth=self.api.auth, listener=self)
        self.stream.filter(track=[find_string], is_async=True)

    def on_status(self, status):
        logger.info(status.text)

    def on_connect(self):
        logger.info('Connected at: {}'.format(datetime.datetime.now()))


def log_config():
    """Adjusts how info is displayed in log"""
    return logging.basicConfig(
        format=(
            '%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s '
            '[%(threadName) -12s] %(message)s'),
        datefmt='%Y-%m-%d %H:%M:%S')


def log_set_level():
    """Sets defaulf log level"""
    logger.setLevel(logging.DEBUG)


def main():
    log_config()
    log_set_level()
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    tb = WatchTwitter()
    tb.start_stream('python')
    while not exit_flag:
        logger.info("Hello world")
        time.sleep(1)


if __name__ == "__main__":
    main()
    pass
