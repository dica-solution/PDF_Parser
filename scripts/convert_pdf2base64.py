import base64
import argparse

def convert_pdf2base64(pdf_file):
    with open(pdf_file, "rb") as pdf_file:
        pdf_base64 = base64.b64encode(pdf_file.read())
        return pdf_base64

def save_base64(base64_string, output_file):
    with open(output_file, "w") as output_file:
        output_file.write(base64_string)
    
def main():
    parser = argparse.ArgumentParser(description='Convert PDF to base64')
    parser.add_argument('--path', type=str, help='Path PDF file to convert')
    args = parser.parse_args()
    pdf_base64 = convert_pdf2base64(args.path)
    # print(pdf_base64.decode())
    save_base64(pdf_base64.decode(), args.path.replace(".pdf", ".txt"))

if __name__ == "__main__":
    main()