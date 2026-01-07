import logging
import os

import mkl.constants as constants

os.makedirs(constants.EXPORT_PATH, exist_ok=True)
log_file_name = os.path.join(constants.EXPORT_PATH, 'grocery_logger.log')

logging.basicConfig(
    filename=log_file_name,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
)