import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

logs_path = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_path, exist_ok=True)

log_file_path = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="[%(asctime)s] - %(levelname)s - %(message)s",
)