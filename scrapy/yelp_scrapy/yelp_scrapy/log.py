import logging

# create logger
logger = logging.getLogger('my-logger')
logger.setLevel(logging.INFO)

# create console handler and set level to debug
err_handler = logging.FileHandler('error_log.txt', 'a')
err_handler.setLevel(logging.WARNING)

info_handler = logging.FileHandler('info_log.txt', 'a')
info_handler.setLevel(logging.INFO)

# create formatter
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
# ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(err_handler)
logger.addHandler(info_handler)
