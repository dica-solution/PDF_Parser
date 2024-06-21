# PDF Parser

This project is a PDF parser that allows you to extract text from PDF exam file and return the PaperExam ID. 

## Installation

To use this project, follow these steps:

1. `git clone git@github.com:dica-solution/PDF_Parser.git`
2. `cd PDF_Parser`
3. `poetry install`  
4. `poetry shell`
5. Set up the Environment variables in the `.env.dev`

## Usage

- Prepare the PDF exam and save it in a folder, for example: `pdf_parser/pdf_exams/exam_001/exam.pdf`  
- Run the following command, wait for the text extraction process, finally you will get an ID of `PaperExam` (a system of storing  structured exam).
```
python scripts/pipeline.py --pdf_file_path `path to pdf file` --prompt_collection_path `path to prompt collection file`
```
