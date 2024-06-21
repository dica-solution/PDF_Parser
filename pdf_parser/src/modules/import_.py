import json
import re
import mistune
from typing import List, Dict, Any, Optional, Union
from pdf_parser.src.models.paper_exam_models import PaperExams, PaperExamsComponents, \
    ComponentsExamGroupedQuizsComponents, ComponentsExamGroupedEssaysComponents, \
    ComponentsExamGroupQuizTrueFalsesComponents, ComponentsExamGroupEntryTextsComponents, \
    ComponentsExamGroupedQuizs, ComponentsExamGroupedEssays, \
    ComponentsExamGroupQuizTrueFalses, ComponentsExamGroupEntryTexts, \
    ComponentsExamSingleQuizs, ComponentsExamSingleEssays, \
    ComponentsExamSingleQuizTrueFalses, ComponentsExamSingleTextEntries, \
    PaperExamsSchoolLinks, PaperExamsGradeLinks, PaperExamsSubjectLinks
from sqlalchemy.orm import Session
from sqlalchemy import text
from pdf_parser.src.config.settings import get_settings
from pdf_parser.src.modules.logger_config import setup_logger
import logging


setup_logger()
logger = logging.getLogger(__name__)




class PrepPaperExam:
    def __init__(self,
                 paper_exam: PaperExams,
                 question_list: List[Union[ComponentsExamSingleQuizs, ComponentsExamSingleEssays]],
                 school_id,
                 grade_id,
                 subject_id) -> None:
        self.paper_exam = paper_exam
        self.question_list = question_list
        self.school_id = school_id
        self.grade_id = grade_id
        self.subject_id = subject_id

class ExamParser:
    def __init__(self, session: Session) -> None:
        self.session = session
    
    def extract_data(self, exam_info_path, exam_question_path):
        exam_info_dict = json.load(open(exam_info_path))
        exam_questions_dict = json.load(open(exam_question_path))
        return exam_info_dict, exam_questions_dict
    
    def wrap_latex_with_span(self, text):
        patterns = [r'\\\((.*?)\\\)', r'\\\[(.*?)\\\]', r'\$\$(.*?)\$\$']
        for i in range(3):
            if i == 0:
                pattern = patterns[i]
                def replace_latex(match):
                    return r'<span class="math-tex">\({}\)</span>'.format(match.group(1))
                text = re.sub(pattern, replace_latex, text, flags=re.DOTALL)
            if i == 1:
                pattern = patterns[i]
                def replace_latex(match):
                    return r'<span class="math-tex">\[{}\]</span>'.format(match.group(1))
                text = re.sub(pattern, replace_latex, text, flags=re.DOTALL)
            if i == 2:
                pattern = patterns[i]
                def replace_latex(match):
                    return r'<span class="math-tex">\[{}\]</span>'.format(match.group(1))
                text = re.sub(pattern, replace_latex, text, flags=re.DOTALL)
        return text

    def support_render_on_mobile(self, text_data: Optional[str]):
        
        if text_data:
            text_data = text_data.replace('&amp;', '&').replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&apos;', "'").replace('operatorname', 'text')

            pattern = r'<span class="math-tex">\\\[.*?\\\]</span>'
            matches = re.findall(pattern, text_data)

            for match in matches:
                new_match = match.replace('\\[', '\\(').replace('\\]', '\\)')
                text_data = text_data.replace(match, new_match)

            pattern = r'\\overparen\{.*?\}'
            matches = re.findall(pattern, text_data)

            for match in matches:
                content = match[11:-1]  # 11 is the length of '\overparen{', -1 is to exclude the closing brace
                new_match = '\\text{cung } ' + content
                text_data = text_data.replace(match, new_match)
            
            return text_data
        return text_data
    
    def escape_markdown_special_characters(self, text):
        escape_chars = {
            # '\\': '\\\\',
            '`': '\\`',
            '*': '\\*',
            '_': '\\_',
            # '{': '\\{',
            # '}': '\\}',
            # '[': '\\[',
            # ']': '\\]',
            # '(': '\\(',
            # ')': '\\)',
            '#': '\\#',
            '+': '\\+',
            '-': '\\-',
            '.': '\\.',
            '!': '\\!',
        }
        return text.translate(str.maketrans(escape_chars))
    
    def transform_data(self, text_data: Optional[str]):
        if text_data:
            html_parser = mistune.create_markdown(
                escape=False,
                plugins=['strikethrough', 'footnotes', 'table', 'speedup', 'url', 'math', 'superscript', 'subscript']
            )
            # text_data = self.escape_markdown_special_characters(text_data)
            text_data = self.wrap_latex_with_span(text_data)
            # text_data = html_parser(text_data)
            text_data = "".join("<p>" + chunk + "</p>" for chunk in text_data.split("\n"))
            text_data = self.support_render_on_mobile(text_data)
            return text_data
        return text_data
    
    def find_school(self, school_name):
        query = text(f"SELECT * FROM schools WHERE name ILIKE '%{school_name}%' LIMIT 1")
        result = self.session.execute(query).fetchall()
        if bool(result):
            return result[0].id, result[0].name
        else:
            return None, None
    
    def find_grade(self, grade_as_num):
        grade_dict = {
            1: 20,
            2: 21,
            3: 22,
            4: 18,
            5: 19,
            6: 6,
            7: 7,
            8: 8,
            9: 9,
            10: 10,
            11: 11,
            12: 12,
        }
        grade_id = grade_dict.get(grade_as_num, None)
        return grade_id
    
    def find_subject(self, subject_name):
        subject_dict = {
            'toán': 1,
        }
        subject_id = subject_dict.get(subject_name, None)
        return subject_id
    
    # def parse_options(self, options_str):
    #     options = re.split(r'(?=[A-D]\.)', options_str)
    #     options = [option.strip() for option in options if option.strip()]
    #     result = []
    #     for option in options:
    #         option = option.strip()
    #         label = option[0]
    #         content = option[2:]
    #         option_dict = {
    #             'label': label,
    #             'content': content
    #         }
    #         result.append(option_dict)
    #     return result   
    def parse_options(self, options):
        options_dict = []
        for option in options:
            label = option[0]
            content = option[2:]
            option_dict = {
                'label': label,
                'content': content
            }
            options_dict.append(option_dict)
        return options_dict

    def parse_single_quiz(self, item, quiz_question_group_id=0) -> ComponentsExamSingleQuizs:
        
        options = self.parse_options(item['quiz_options'])

        title = item['question_title']
        question_content = self.transform_data(item['original_text'])
        long_answer = self.transform_data(item['explanation'])

        label_a = None
        label_b = None
        label_c = None
        label_d = None

        for option in options:
            label = option['label'].lower()
            if label == 'a':
                label_a = self.transform_data(option['content'])
            if label == 'b':
                label_b = self.transform_data(option['content'])
            if label == 'c':
                label_c = self.transform_data(option['content'])
            if label == 'd':
                label_d = self.transform_data(option['content'])
        
        correct_label = 'label' + item['correct_option']

        return ComponentsExamSingleQuizs(
            title = title,
            question_content = question_content,
            long_answer = long_answer,
            label_a = label_a,
            label_b = label_b,
            label_c = label_c,
            label_d = label_d,
            correct_label = correct_label,
        )
    
    def parse_single_essay(self, item, quiz_question_group_id=0) -> ComponentsExamSingleEssays:
        title = item['question_title']
        question_content = self.transform_data(item['original_text'])
        long_answer = self.transform_data(item['explanation'])
        
        return ComponentsExamSingleEssays(
            title = title,
            question_content = question_content,
            long_answer = long_answer,
        )

    def parse_as_dict_collections(self, exam_info_path, exam_question_path):
        exam_info_dict, exam_questions_dict = self.extract_data(exam_info_path, exam_question_path)
        
        if exam_info_dict and exam_questions_dict:
            paper_exam = PaperExams(
                title = f"{exam_info_dict['exam_full_name']} - {exam_info_dict['school']}",
                exam_term = exam_info_dict['exam_term'],
                duration = exam_info_dict['duration'],
                school_year = exam_info_dict['year'],
            )

            school_id, school_name = self.find_school(school_name=exam_info_dict['school'])
            grade_id = self.find_grade(grade_as_num=exam_info_dict['grade'])
            subject_id = self.find_subject(subject_name=exam_info_dict['subject'].lower())


            question_list = []

            for item in exam_questions_dict:
                if item['question_type'] == 'multiple-choice':
                    quiz_question = self.parse_single_quiz(item)
                    question_list.append(quiz_question)

                if item['question_type'] == 'essay':
                    essay_question = self.parse_single_essay(item)
                    question_list.append(essay_question)

            
            return PrepPaperExam(
                paper_exam = paper_exam,
                question_list = question_list,
                school_id = school_id,
                grade_id = grade_id,
                subject_id = subject_id
            )
        return None

    def import_paper_exam(self, exam_info_path, exam_question_path):
        paper_exam_data = self.parse_as_dict_collections(exam_info_path, exam_question_path)

        if paper_exam_data:
            try:
                paper_exam = paper_exam_data.paper_exam
                self.session.add(paper_exam)
                self.session.flush()
                paper_exam_id = paper_exam.id
                # self.session.commit()

                question_list = paper_exam_data.question_list
                self.session.add_all(question_list)
                self.session.flush()

                paper_exam_components_list = []
                for idx, question in enumerate(question_list):
                    if isinstance(question, ComponentsExamSingleQuizs):
                        component_type_value = "exam.single-quiz"
                    if isinstance(question, ComponentsExamSingleEssays):
                        component_type_value = "exam.single-essay"
                    paper_exam_component = PaperExamsComponents(
                        entity_id = paper_exam_id,
                        component_id = question.id,
                        component_type = component_type_value,
                        field = "relatedItems",
                        order = idx + 1
                    )
                    paper_exam_components_list.append(paper_exam_component)

                self.session.add_all(paper_exam_components_list)
                
                school_id = paper_exam_data.school_id
                if school_id:
                    paper_exams_school_links = PaperExamsSchoolLinks(paper_exam_id=paper_exam_id, school_id=school_id, paper_exam_order=1)
                    self.session.add(paper_exams_school_links)

                grade_id = paper_exam_data.grade_id
                if grade_id:
                    paper_exams_grade_links = PaperExamsGradeLinks(paper_exam_id=paper_exam_id, grade_id=grade_id, paper_exam_order=1)
                    self.session.add(paper_exams_grade_links)

                subject_id = paper_exam_data.subject_id
                if subject_id:
                    paper_exams_subject_links = PaperExamsSubjectLinks(paper_exam_id=paper_exam_id, subject_id=subject_id, paper_exam_order=1)
                    self.session.add(paper_exams_subject_links)

                self.session.commit()
                logger.info(f"Imported paper exam ID: {paper_exam_id}")

                return paper_exam_id, None
            except Exception as e:
                # print(f"Error: {e}")
                self.session.rollback()
                logger.error(f"Error: {e}")
                return 0, e
        return 0, "No data to import"

def import_exam(session, exam_info_path, exam_question_path):
    exam_parser = ExamParser(session)
    paper_exam_id, noti = exam_parser.import_paper_exam(exam_info_path, exam_question_path)
    return paper_exam_id, noti

