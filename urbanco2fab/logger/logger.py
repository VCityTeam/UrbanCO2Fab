import logging


def set_logger(level=logging.DEBUG):
    format = '%(levelname)s - %(asctime)s - file:%(module)s.py - %(message)s'

    # create logger
    logger = logging.getLogger('root')
    logger.setLevel(level)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # create formatter
    formatter = logging.Formatter(format)

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    return logger



if __name__ == "__main__":
    logger = set_logger()
    # 'application' code
    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')

 