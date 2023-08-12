import PyPDF2


def read_pdf_content(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        content = []
        for page_num in range(len(pdf_reader.pages)):
            # page = pdf_reader.getPage(page_num)
            page = pdf_reader.pages[page_num]
            content.append(page.extract_text())

        return '\n'.join(content).encode('utf-8')

pdf_path = r"C:\Users\Student\Downloads\test.pdf"

pdf_content = read_pdf_content(pdf_path)

with open('Upload.docx', 'wb') as dest:
    dest.write(pdf_content)