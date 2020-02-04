import logging


c_handler  = logging.StreamHandler()
f_handler  = logging.FileHandler("logFile.log")
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)


def configLogger(logger):
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    return logger