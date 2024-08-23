import logging
import sys
from logging.handlers import RotatingFileHandler

def setup_logger(log_file='app.log', log_level=logging.INFO, max_file_size=50*1024*1024, backup_count=10):
    '''
    Create a logger file with 50mb limit and a backup of 10 files
    '''
    try:
       
        logger = logging.getLogger()
        logger.setLevel(log_level)

        file_handler = RotatingFileHandler(log_file, maxBytes=max_file_size, backupCount=backup_count)
        console_handler = logging.StreamHandler(sys.stdout)

        file_handler.setLevel(log_level)
        console_handler.setLevel(log_level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    except Exception as e:
        print(f"Error setting up logger: {str(e)}")
        raise

logger = setup_logger()
