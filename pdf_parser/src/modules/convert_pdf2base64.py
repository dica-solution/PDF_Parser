import base64
import argparse


class ConvertPdf2Base64:
    def __init__(self, pdf_file_path, output_file_path):
        self.pdf_file_path = pdf_file_path
        self.output_file_path = output_file_path

    def convert_pdf2base64(self):  # Add 'self' here
        with open(self.pdf_file_path, "rb") as pdf_file:  # Use 'self.pdf_file_path' here
            pdf_base64 = base64.b64encode(pdf_file.read())
            return pdf_base64
        
    def save_base64(self):
        base64_string = self.convert_pdf2base64()  # Remove 'self.pdf_file_path' here
        # output_file_path = self.pdf_file_path.replace(".pdf", ".txt")
        with open(self.output_file_path, "w") as output_file:
            output_file.write(base64_string.decode())  # Use 'output_file.write' instead of 'output_file_path.write'
        print(f"Saved base64 to {self.output_file_path}")
        # return output_file_path
# def main():
#     parser = argparse.ArgumentParser(description='Convert PDF to base64')
#     parser.add_argument('--path', type=str, help='Path PDF file to convert')
#     args = parser.parse_args()
#     pdf_base64 = convert_pdf2base64(args.path)
#     save_base64(pdf_base64.decode(), args.path.replace(".pdf", ".txt"))

# if __name__ == "__main__":
#     main()