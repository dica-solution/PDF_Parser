import os
import logging
from datetime import datetime, timezone, timedelta


def setup_logger():
    now = datetime.now(timezone(timedelta(hours=7)))
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    log_path = os.path.join("pdf_parser/log/generate_logs", f"{now_str}.log")
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )