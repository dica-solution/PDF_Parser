import sys
import os
notebook_dir = os.path.dirname(os.path.abspath("__file__"))

project_root = os.path.abspath(os.path.join(notebook_dir))

if project_root not in sys.path:
    sys.path.append(project_root)

from pdf_parser.src.config.settings import get_settings
from sqlalchemy import text
from pdf_parser.src.modules.connect import create_and_check_engine, get_session_from_engine
from pdf_parser.src.modules.import_ import import_exam
from pdf_parser.src.modules.generate import generate
from datetime import datetime, timezone, timedelta
import logging

now = datetime.now(timezone(timedelta(hours=7)))
now_str = now.strftime("%Y-%m-%d %H:%M:%S")
log_path = os.path.join(project_root, "pdf_parser/log/generate_logs", f"{now_str}.log")
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

settings = get_settings("/home/dica/Projects/syvan_projects/pdf_parser/.env.dev")

engine = create_and_check_engine(f"{settings.database_url}{settings.db_name}")

pdf_file_path = "/home/dica/Projects/syvan_projects/pdf_parser/pdf_parser/paper_exams/003/de-giua-ky-1-toan-12-nam-2022-2023-truong-thpt-phu-cu-hung-yen-HanhTruong.pdf"
prompt_collection_path = "/home/dica/Projects/syvan_projects/pdf_parser/pdf_parser/src/prompt_collections/collection_01.json"

print("Strart generating exam info and questions...")
exam_info_path, exam_question_path = generate(pdf_file_path, prompt_collection_path)
print("Generated exam info and questions.")
print(f"Exam info path: {exam_info_path}")
print(f"Exam question path: {exam_question_path}")

with get_session_from_engine(engine) as session:
    paper_exam_id, noti = import_exam(session, exam_info_path, exam_question_path)
print(f"Paper exam ID: {paper_exam_id}")
print(f"Notification: {noti}")