import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO

class PDFTableExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tables = []

    def extract_tables(self):
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                extracted_tables = page.extract_tables()
                if extracted_tables:
                    for table in extracted_tables:
                        df = pd.DataFrame(table[1:], columns=table[0])
                        self.tables.append(df)

    def save_to_excel(self, output):
        if self.tables:
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                for i, table in enumerate(self.tables):
                    table.to_excel(writer, sheet_name=f'Sheet{i+1}', index=False)

st.title("PDF Table Extractor to Excel")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    with open("uploaded_file.pdf", "wb") as f:
        f.write(uploaded_file.read())

    extractor = PDFTableExtractor("uploaded_file.pdf")
    st.write("Extracting tables from PDF...")
    extractor.extract_tables()

    if extractor.tables:
        output = BytesIO()
        extractor.save_to_excel(output)
        st.download_button(
            label="Download Excel file",
            data=output.getvalue(),
            file_name="extracted_tables.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.write("No tables found in the PDF. Please upload a PDF containing tables.")
