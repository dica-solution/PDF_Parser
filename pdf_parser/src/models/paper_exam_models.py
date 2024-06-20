from datetime import datetime
from sqlalchemy import Column, String, Integer, Date, DateTime, func, Text, Numeric, Boolean, BigInteger, DOUBLE_PRECISION
from ..modules.connect import Base

class PaperExams(Base):
    __tablename__ = 'paper_exams'

    id = Column(Integer, primary_key=True)

    created_at = Column(DateTime, default=datetime.now(), server_default=func.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=func.now(), server_default=func.now())
    created_by_id = Column(BigInteger, default=1, nullable=False)
    updated_by_id = Column(BigInteger, default=1, nullable=False)

    title = Column(String(255), nullable=False)
    exam_term = Column(String(255), nullable=False)
    duration = Column(Integer, nullable=False)
    school_year = Column(String(255), nullable=False)

    published_at = Column(DateTime, default=datetime.now(), server_default=func.now())


class CommonComponentsProperties(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)

    entity_id = Column(Integer, nullable=False)
    component_id = Column(Integer, nullable=False)
    component_type = Column(String(255), nullable=False)
    field = Column(String(255), nullable=False)
    order = Column(Integer, nullable=False)

class PaperExamsComponents(CommonComponentsProperties):
    __tablename__ = 'paper_exams_components'

class ComponentsExamGroupedQuizsComponents(CommonComponentsProperties):
    __tablename__ = 'components_exam_grouped_quizs_components'

class ComponentsExamGroupedEssaysComponents(CommonComponentsProperties):
    __tablename__ = 'components_exam_grouped_essays_components'

class ComponentsExamGroupQuizTrueFalsesComponents(CommonComponentsProperties):
    __tablename__ = 'components_exam_group_quiz_true_falses_components'

class ComponentsExamGroupEntryTextsComponents(CommonComponentsProperties):
    __tablename__ = 'components_exam_group_entry_texts_components'


class CommonGroupProperties(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)

    title = Column(String(255), nullable=False)
    group_content = Column(Text, nullable=True)

class ComponentsExamGroupedQuizs(CommonGroupProperties):
    __tablename__ = 'components_exam_grouped_quizs'
    group_audio = Column(String(255), nullable=True)

class ComponentsExamGroupedEssays(CommonGroupProperties):
    __tablename__ = 'components_exam_grouped_essays'
    group_audio = Column(String(255), nullable=True)

class ComponentsExamGroupQuizTrueFalses(CommonGroupProperties):
    __tablename__ = 'components_exam_group_quiz_true_falses'

class ComponentsExamGroupEntryTexts(CommonGroupProperties):
    __tablename__ = 'components_exam_group_entry_texts'


class CommonSingleProperties(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)

    title = Column(String(255), nullable=False)
    question_content = Column(Text, nullable=True)
    point = Column(Numeric(10, 2), nullable=False)
    long_answer = Column(Text, nullable=True)

class ComponentsExamSingleQuizs(CommonSingleProperties):
    __tablename__ = 'components_exam_single_quizs'
    question_audio = Column(String(255), nullable=True)
    short_answer = Column(Text, nullable=True)
    label_a = Column(Text, nullable=True)
    label_b = Column(Text, nullable=True)
    label_c = Column(Text, nullable=True)
    label_d = Column(Text, nullable=True)
    correct_label = Column(String(255), nullable=True)

class ComponentsExamSingleEssays(CommonSingleProperties):
    __tablename__ = 'components_exam_single_essays'
    question_audio = Column(String(255), nullable=True)
    short_answer = Column(Text, nullable=True)

class ComponentsExamSingleQuizTrueFalses(CommonSingleProperties):
    __tablename__ = 'components_exam_single_quiz_true_falses'
    answer = Column(Boolean, nullable=False)

class ComponentsExamSingleTextEntries(CommonSingleProperties):
    __tablename__ = 'components_exam_single_text_entries'
    answer = Column(Text, nullable=False)


class CommonPaperExamsLinks(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)

    paper_exam_id = Column(Integer, nullable=False)
    paper_exam_order = Column(DOUBLE_PRECISION, nullable=False)

class PaperExamsSchoolLinks(CommonPaperExamsLinks):
    __tablename__ = 'paper_exams_school_links'
    school_id = Column(Integer, nullable=False)

class PaperExamsGradeLinks(CommonPaperExamsLinks):
    __tablename__ = 'paper_exams_grade_links'
    grade_id = Column(Integer, nullable=False)

class PaperExamsSubjectLinks(CommonPaperExamsLinks):
    __tablename__ = 'paper_exams_subject_links'
    subject_id = Column(Integer, nullable=False)