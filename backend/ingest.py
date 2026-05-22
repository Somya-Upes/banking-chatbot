from pypdf import PdfReader
from rag import store_chunks
import os

# Function to read PDF files
def load_pdf(file_path):
    text = ""

    # Open the PDF
    reader = PdfReader(file_path)

    # Read all pages
    for page in reader.pages:
        text += page.extract_text()

    return text


# Function to split text into chunks
def split_text(text, chunk_size=500, overlap=100):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]
        chunks.append(chunk)

        # overlap keeps context between chunks
        start += chunk_size - overlap

    return chunks


# Test function
if __name__ == "__main__":

    data_folder = "data"

    for filename in os.listdir(data_folder):

        if filename.endswith(".pdf"):

            file_path = os.path.join(data_folder, filename)

            print(f"\nReading: {filename}")

            text = load_pdf(file_path)

            print("\nFirst 1000 characters:\n")
            print(text[:1000])

            chunks = split_text(text)

            print(f"\nTotal chunks created: {len(chunks)}")
            store_chunks(chunks)