import logging
from datetime import datetime
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logs_dir = 'Logs'
os.makedirs(logs_dir, exist_ok=True)
log_file_name = f"{logs_dir}/scraper_{datetime.now().strftime('%Y-%m-%d')}.log"
file_handler = logging.FileHandler(log_file_name)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
