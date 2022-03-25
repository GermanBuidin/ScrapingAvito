import logging


class Logging:

    def logger_init(self, name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        handler_stream = logging.StreamHandler()
        handler_stream.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] - %(message)s'))
        handler_stream.setLevel(logging.DEBUG)
        logger.addHandler(handler_stream)
        logger.info('logger was initialized')


Logging().logger_init('processing')
logger = logging.getLogger('processing.main')
