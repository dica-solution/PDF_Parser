import sys
import os
project_root = os.path.dirname(os.path.abspath("__file__"))
sys.path.append(project_root)

from pdf_parser.src.config.settings import get_settings
from pdf_parser.src.modules.convert_pdf2base64 import ConvertPdf2Base64
from pdf_parser.src.modules.logger_config import setup_logger
import openai
import json
import time
from datetime import datetime, timezone, timedelta
import logging
import re
from tqdm import tqdm

# Setting Logging
setup_logger()

logger = logging.getLogger(__name__)


class LazyDecoder(json.JSONDecoder):
    def decode(self, s, **kwargs):
        regex_replacements = [
            (re.compile(r'([^\\])\\([^\\])'), r'\1\\\\\2'),
            (re.compile(r',(\s*])'), r'\1'),
        ]
        for regex, replacement in regex_replacements:
            s = regex.sub(replacement, s)
        return super().decode(s, **kwargs)

def resolve_name(file_path, additional_name=""):
    directory = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    file_name = additional_name + "".join(c for c in file_name if c != " ")
    new_file_path = os.path.join(directory, file_name)
    if new_file_path != file_path:
        # print(f"New file name: {file_name}")
        return True, new_file_path
    else:
        return False, file_path

def init_conversation_with_pdf_base64(pdf_base64_content, prompt_collection):
    init_messages_list = []
    init_messages_list.append(
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt_collection['extract_information']},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:application/pdf;base64,{pdf_base64_content}"
                    }
                }
            ]
        }
    )

    return init_messages_list

def add_messages(messages_list, message_role, message):
    messages_list.append(
        {
            "role": message_role,
            "content": message
        }
    )

    return messages_list

def get_response(client, messages_list, settings):
    stream = client.chat.completions.create(
        model = settings.ai_model_name,
        messages = messages_list,
        stream = True,
        temperature = settings.temperature,
    )
    response_chunks = []
    for chunk in stream:
        chunk_message = chunk.choices[0].delta.content
        if chunk_message:
            response_chunks.append(chunk_message)
    
    full_response =  "".join(response_chunks)

    messages_list = add_messages(messages_list, "assistant", full_response)

    return full_response, messages_list

def generate(pdf_path, prompt_collection_path):

    result, resolved_pdf_path = resolve_name(pdf_path)
    if result:
        os.rename(pdf_path, resolved_pdf_path)

    # Load settings
    settings = get_settings(os.path.join(project_root, ".env.dev"))

    # Convert PDF to base64, after that load the base64 file
    _, base64_pdf_path = resolve_name(resolved_pdf_path, "base64_")
    base64_pdf_path = base64_pdf_path.replace(".pdf", ".txt")
    converter = ConvertPdf2Base64(resolved_pdf_path, base64_pdf_path)
    converter.save_base64()
    pdf_base64_content = open(base64_pdf_path, "r").read()

    # Load prompt collection
    prompt_collection = json.load(open(prompt_collection_path, 'r'))[0]

    # API client
    client = openai.OpenAI(base_url=settings.base_url, api_key=settings.api_key)

    # Extract information of exam
    messages_list = init_conversation_with_pdf_base64(pdf_base64_content, prompt_collection)
    information_dict, messages_list = get_response(client, messages_list, settings)
    information_dict = json.loads(information_dict.replace('```json\n', '').replace('\n```', ''))
    logger.info(f"Extracted information: {information_dict}")

    messages_list = add_messages(messages_list, "user", prompt_collection['get_correct_answer_table'][0])
    response, messages_list = get_response(client, messages_list, settings)
    logger.info(f"Extracted Correct answer table - 0: {response}")

    messages_list = add_messages(messages_list, "user", prompt_collection['get_correct_answer_table'][1])
    response, messages_list = get_response(client, messages_list, settings)
    logger.info(f"Extracted Correct answer table - 1: {response}")

    # Formats and function tag
    messages_list = add_messages(messages_list, "user", prompt_collection['format_and_function_tag'])
    response, messages_list = get_response(client, messages_list, settings)
    logger.info(f"Format and function tag: {response}")

    # Extract questions
    questions = []
    # for i in range(information_dict['number_of_questions']):
    for i in tqdm(range(information_dict['number_of_questions'])):
        try:
            messages_list = add_messages(messages_list, "user", f"/extract({i+1})")
            response, messages_list = get_response(client, messages_list, settings)
            logger.info(f"Extracted question {i+1}, Raw response: {response}")

            replaced_response = response.replace('```json\n', '').replace('\n```', '')
            questions.append(json.loads(replaced_response, cls=LazyDecoder))
            logger.info(f"Processed response: {questions[-1]}")
        except Exception as e:
            logger.error(f"Error at question {i+1}: {e}")
            logger.error(f"Raw response: {response}")
    
    logger.info("All questions have been extracted.")

    # Save information and questions
    _, info_pdf_path = resolve_name(pdf_path, "exam_info_")
    _, questions_pdf_path = resolve_name(pdf_path, "exam_questions_")

    info_pdf_path = info_pdf_path.replace(".pdf", ".json")
    questions_pdf_path = questions_pdf_path.replace(".pdf", ".json")

    with open(info_pdf_path, "w") as info_file:
        json.dump(information_dict, info_file, indent=4, ensure_ascii=False)
    with open(questions_pdf_path, "w") as questions_file:
        json.dump(questions, questions_file, indent=4, ensure_ascii=False)
    
    return info_pdf_path, questions_pdf_path