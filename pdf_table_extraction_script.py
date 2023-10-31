import cv2
import pytesseract
import pandas as pd
from pdf2image import convert_from_path

def extract_and_process_table(img):
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray, config='--psm 6').strip()

    # Process the extracted text to form a structured table
    rows = text.split('\n')
    table_data = []
    for row in rows:
        columns = [col.strip() for col in row.split('  ') if col.strip() != ""]
        if columns:
            table_data.append(columns)

    # Separate rank from the chemical name using the space before rank as a delimiter
    processed_data = []
    for row in table_data:
        new_row = []
        for item in row:
            parts = item.rsplit(' ', 1)  # Splitting using the last space in the string
            if len(parts) == 2 and parts[1].replace('-', '').isdigit():
                new_row.extend(parts)
            else:
                new_row.append(item)
        processed_data.append(new_row)

    return processed_data

if __name__ == '__main__':
    pdf_path = input("Enter the path to the PDF: ")
    images = convert_from_path(pdf_path)
    for idx, img in enumerate(images, start=1):
        processed_data = extract_and_process_table(img)
        df = pd.DataFrame(processed_data)
        csv_path = pdf_path.rsplit('.', 1)[0] + f'_page_{idx}.csv'
        df.to_csv(csv_path, index=False, header=False)
        print(f"Processed CSV for page {idx} saved to: {csv_path}")
