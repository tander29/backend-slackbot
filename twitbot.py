#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Travis Anderson"

"""
This is for contacting twitter, and watching a specific user or word

"""
import logging
# import signal
import tweepy
import time
import os
# import sys
import datetime
from threading import Thread
import json
import threading


logger = logging.getLogger(__name__)
exit_flag = False


# def signal_handler(sig_num, frame):
#     """Smooth exit from system"""
#     global exit_flag
#     logger.warning('Received exit signal number: {}'.format(str(sig_num)))
#     if sig_num:
#         exit_flag = True


def _start(self, is_async):
    """Monkey patch to allow multi threading so twitter can run and
    main program can run"""
    self.running = True
    if is_async:
        logger.warning("Initiating multithread")
        self._thread = Thread(
            target=self._run, name="Tweepy Thread", daemon=True)
        self._thread.start()
    else:
        self._run()


class WatchTwitter(tweepy.StreamListener):
    """Class that subscribes to keywords on twitter """

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
        # logger.warning("Did a monkey patch, could use a demo on this")
        tweepy.Stream._start = _start
        self.subscriptions = []
        self._stop_event = threading.Event()
        self.stream_timestamp = 0
        self.master_timestamp = 0

    def add_subscription(self, subscribe_to):
        """If stream is running adds new subscription, restarts stream"""
        if subscribe_to not in self.subscriptions:
            logger.info('Adding subscription: {}'.format(subscribe_to))
            self.subscriptions.append(subscribe_to)
            logger.info(self.subscriptions)
            self.stream.running = False
            self.start_stream()
        else:
            logger.info("Already subscribed: {}" .format(self.subscriptions))

    def remove_subscription(self, unsubscribe_from):
        logger.info("Attempting to remove {}".format(unsubscribe_from))
        if unsubscribe_from in self.subscriptions:
            logger.info(
                'Removing from subscriptions: {}'.format(unsubscribe_from))
            self.subscriptions.remove(unsubscribe_from)
            self.stream.running = False
            self.start_stream()

    def pause_stream(self):
        if self.stream.running:
            logger.info("Pausing all subscriptions: {}".format(
                self.subscriptions))
            self.stream.running = False

    def restart_stream(self):
        if not self.stream.running:
            logger.info("Restarting stream")
            self.start_stream()

    def init_stream(self, string):
        self.subscriptions.append(string)
        self.start_stream()

    def exit_flag_toggle(self):
        global exit_flag
        if exit_flag:
            self.pause_stream()

    def start_stream(self):
        global exit_flag
        exit_flag = False
        logger.info('Subscriptions: {}'.format(self.subscriptions))
        self.stream = tweepy.Stream(auth=self.api.auth, listener=self)
        time.sleep(1)
        self.stream.filter(track=self.subscriptions, is_async=True)

    def on_status(self, status):
        logger.info(status.text)

    def on_connect(self):
        self.stream_timestamp = datetime.datetime.now()
        logger.info('Connected to twitter at: {}'.format(
            datetime.datetime.now()))
        if not self.master_timestamp:
            self.master_timestamp = self.stream_timestamp

    def get_user_timeline(self, users_name):
        return self.api.user_timeline(screen_name=users_name, count=1)

    def most_recent_tweet(self, users_name):
        logger.info('subscriptions:')
        user = self.get_user_timeline(users_name)
        status = user[0]._json
        json_str = json.dumps(status)
        json_dict = json.loads(json_str)
        logger.info('{} tweeted: {}'.format(users_name, json_dict['text']))


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


def init_logger():
    logging.basicConfig(
        format=(
            '%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s '
            '[%(threadName) -12s] %(message)s'),
        datefmt='%Y-%m-%d %H:%M:%S')

    logger.setLevel(logging.DEBUG)

    # signal.signal(signal.SIGINT, signal_handler)
    # signal.signal(signal.SIGTERM, signal_handler)


def main():
    global exit_flag
    log_config()
    log_set_level()
    # signal.signal(signal.SIGINT, signal_handler)
    # signal.signal(signal.SIGTERM, signal_handler)

    tb = WatchTwitter()
    tb.init_stream('python')
    while not exit_flag:
        time.sleep(5)
        tb.pause_stream()
        time.sleep(5)
        tb.add_subscription('Trump')
        time.sleep(5)
        tb.remove_subscription('Trump')


if __name__ == "__main__":
    main()
    pass
