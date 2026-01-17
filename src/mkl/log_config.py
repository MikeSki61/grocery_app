import logging
import os

import mkl.constants as constants
from mkl.paths import DATA_DIR, ensure_dirs


# Create the export path if it doesn't exist
ensure_dirs()

# Get the log filemname
log_file_name = os.path.join(DATA_DIR, 'grocery_logger.log')

# Set up the log config
logging.basicConfig(
    filename=log_file_name,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
)