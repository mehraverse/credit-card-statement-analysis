I want to analyze spending habits using credit card statements and emails. This project should be generic and reusable for others.

### Detailed Tasks

1. **Organize Files** ✅

   - Create a folder structure to separate different credit card statements.
   - Move all PDF statements into a dedicated folder.
   - Move all `.eml` files into another folder.

2. **Extract Data from PDF Statements** ✅

   - Research and choose a Python library (e.g., PyPDF2, pdfplumber) for extracting text from PDFs.
   - Write a script to extract transaction details from each PDF.
   - Parse and structure the extracted data into a CSV or JSON format.

3. **Extract Data from `.eml` Files** ✅

   - Research and choose a Python library (e.g., email, imaplib) for parsing `.eml` files.
   - Write a script to extract transaction details from each `.eml` file.
   - Parse and structure the extracted data into a CSV or JSON format.

4. **Data Cleaning** ✅

   - Standardize the format of transaction data from all sources.
   - Remove duplicates and ensure all fields (e.g., date, amount, merchant) are consistent.

5. **Data Categorization** ✅

   - Define a list of spending categories (e.g., groceries, entertainment, utilities, dining).
   - Create a mapping of common merchant names or keywords to categories.
   - Write a script to assign each transaction to a category based on the mapping.
   - Allow manual overrides for transactions that cannot be automatically categorized.

6. **Visualization** ✅

   - Use a visualization library (e.g., Matplotlib, Seaborn) to create charts:
     - Monthly spending trends.
     - Spending breakdown by category.
   - Export visualizations as images for reporting.

7. **Reporting**

   - Generate a summary report of spending habits, including key insights and trends.
   - Save the report as a PDF or shareable document.

8. **Automation (Optional)**

   - Create a script to automate the entire process for future statements.
   - Allow users to configure the script for their specific credit card providers.
   - Schedule the script to run periodically (e.g., using cron or Task Scheduler).
