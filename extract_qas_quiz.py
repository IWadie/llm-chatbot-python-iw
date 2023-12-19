import fitz  # PyMuPDF
import csv

# Function to extract data from the PDF
def extract_data_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    data = []

    line_count = 1
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text = page.get_text("text")
        lines = text.splitlines()

        num_lines = len(lines)
        print(f"num_lines: {num_lines}")
        for line_num in range(num_lines):
            print(f"line_num: {line_num}, line: {lines[line_num]}")
            if line_count == 3:
                answer = lines[line_num].rstrip()
                if line_num < num_lines - 1:
                    if not lines[line_num+1].strip().isdigit():
                        answer = answer + " " + lines[line_num+1].rstrip()
                data.append([question, answer])
                print(f"{question}, {answer}")
                line_count = 4  # to stop subsequent lines being treated as answers until a digit comes
            if line_count == 2:
                question = lines[line_num].rstrip()
                line_count = 3
            if not isinstance(lines[line_num], int):
                if lines[line_num].strip().isdigit():
                    line_count = 2
    return data

# Function to write data to a CSV file
def write_data_to_csv(data, csv_filename):
    with open(csv_filename, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=";")
        # Write headers
        csv_writer.writerow(["Question", "Answer"])
        # Write data rows
        csv_writer.writerows(data)

if __name__ == "__main__":
    pdf_file = "/home/iain/Software_Projects/llm-chatbot-python-quiz-qam/10.000vragen.pdf"  # Replace with the path to your PDF file
    csv_file = "/home/iain/Software_Projects/llm-chatbot-python-quiz-qam/output.csv"  # Replace with the desired CSV file name

    extracted_data = extract_data_from_pdf(pdf_file)

    if extracted_data:
        write_data_to_csv(extracted_data, csv_file)
        print(f"Data extracted and saved to {csv_file}")
    else:
        print("No data found in the PDF.")