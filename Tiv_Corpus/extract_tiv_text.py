import fitz  # PyMuPDF
import os


def extract_text_from_pdf(pdf_path, output_directory):
    try:
        text = ''
        with fitz.open(pdf_path) as pdf_document:
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                text += page.get_text("text")  

        # Create the output file path
        output_file_path = os.path.join(output_directory, "tiv_corpus.txt")
        
        # Ensure the output directory exists
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Write extracted text to a file
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(text)

        print(f"Text extracted and saved to: {output_file_path}")
        return output_file_path

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

pdf_path = r"C:\Users\user\Desktop\software\WSD\Tiv_Nballs\Tiv_Corpus\bi7_TV.pdf"

# Writable directory for the output data
output_directory = os.path.expanduser(r"C:\Users\user\Desktop\software\WSD\nTiv_Nballs\Tiv_Corpus\data")

corpus_text_file = extract_text_from_pdf(pdf_path, output_directory)

