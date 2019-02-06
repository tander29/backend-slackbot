import twitbot
import logging
import time
import signal

logger = logging.getLogger(__name__)
exit_flag = False

logger = logging.getLogger(__name__)
exit_flag = False


def signal_handler(sig_num, frame):
    """Smooth exit from system"""
    global exit_flag
    logger.warning(
        '!!!!!!!!!!-----------!!!!!!!!!!!!!!!!!: {}'.format(str(sig_num)))
    if sig_num:
        exit_flag = True


def init_logger():
    logging.basicConfig(
        format=(
            '%(asctime)s.%(msecs)03d %(name)-12s %(levelname)-8s '
            '[%(threadName) -12s] %(message)s'),
        datefmt='%Y-%m-%d %H:%M:%S')

    logger.setLevel(logging.DEBUG)


def main():
    global exit_flag
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    twitbot.init_logger()
    twitterbot = twitbot.WatchTwitter()

    while not exit_flag:
        with twitterbot as tb:
            tb.init_stream('python')
            # logger.info("hello me")
            time.sleep(3)
            tb.pause_stream()
            time.sleep(3)
            tb.add_subscription('Trump')
            time.sleep(2)


if __name__ == "__main__":
    main()
