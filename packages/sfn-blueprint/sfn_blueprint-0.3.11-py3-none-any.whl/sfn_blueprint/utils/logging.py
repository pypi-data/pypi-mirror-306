import logging

# RD: logger name has to be taken from json file (so that it will use name of agent)

def setup_logger():
    logger = logging.getLogger("FeatureSuggestionApp")
    logger.setLevel(logging.INFO)
    # StreamHandler for logging to console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(stream_handler)
    return logger, stream_handler
