from flask import Flask, request, send_file, render_template
import pdfplumber
import pandas as pd
from io import BytesIO

# Create Flask application instance
app = Flask(__name__)

# Define a class to extract tables from PDF
class PDFTableExtractor:
    def __init__(self, file_data):
        self.tables = []
        self.table_extracter(file_data)

    def table_extracter(self, file_data):
        # Open the PDF file
        with pdfplumber.open(BytesIO(file_data)) as pdf:
            for page in pdf.pages:  # Iterate through each page in the PDF
                # Extract tables from the page
                extracted_tables = page.extract_tables()
                if extracted_tables:
                    # Convert each table into a DataFrame and append to the list
                    for table in extracted_tables:
                        df = pd.DataFrame(table)
                        self.tables.append(df)

    def get_tables(self):
        return self.tables

    # Method to save extracted tables to an Excel file
    def save_to_excel(self):
        if self.tables:
            output = BytesIO()
            # Write tables to Excel file
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                for i, table in enumerate(self.tables):
                    table.to_excel(writer, sheet_name=f'Sheet{i+1}', index=False)
            return output.getvalue()
        else:
            return None

            

# Route for uploading PDF and extracting tables
@app.route("/", methods=["GET", "POST"])

def upload_and_extract():
    message = ""  # Initialize message variable

    # Handling POST request
    if request.method == "POST":
        uploaded_file = request.files["file"]  # Get uploaded file
        if uploaded_file:
            # Initialize PDFTableExtractor instance with uploaded file data
            extractor = PDFTableExtractor(uploaded_file.read())
            tables = extractor.get_tables()  # Get extracted tables
            if tables:
                # Save extracted tables to Excel file
                excel_data = extractor.save_to_excel()
                # Send Excel file as response
                return send_file(
                    BytesIO(excel_data),
                    mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    as_attachment=True,
                    download_name="extracted_tables.xlsx",
                )
            else:
                message = "No tables found in the uploaded PDF."  # Update message if no tables found

    # Render index.html template with message
    return render_template("index.html", message=message)

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
