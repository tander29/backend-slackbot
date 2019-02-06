import logging
import os
import time
import sys
from datetime import datetime as dt
import argparse

import slackclient
from twitbot import WatchTwitter

logger = logging.getLogger(os.path.base(__file__))


class SlackBot:
    def __init__(self, bot_user_token, bot_id=None):
        self.sc = slackclient.SlackClient(token=bot_user_token)
        self.bot_id = bot_id
        if not self.bot_id and self.sc.rtm_connect(with_team_state=False):
            """Get our bot's id if was not given to us"""
            response = self.sc.api_call('auth.test')
            self.bot_id = response.get('user_id')
        # this string allows to filter away sgs not directed at me
        self.at_bot = '<@' + self.bot_id + '>'


def main(loglevel):
    logging.basicConfig(
        format=(
            '%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s '
            '[%(threadName) -12s] %(message)s'),
        datefmt='%Y-%m-%d %H:%M:%S')

    logger.setLevel(logging.DEBUG)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Slackbot')
    parser.add_argument('-l', '--loglevel', type=str, default='INFO',
                        help='Set level: INFO, DEBUG, WARN ')

    exit(main(ns.loglevel))
