# SC_smart_import

`SC_smart_import.py` is a Python script that extracts transaction details from credit card statement PDFs and outputs them to a tab-delimited text file. It processes multiple PDFs, extracts "Date", "Description", and "Amount" from transaction lines, and deduces the transaction year based on the statement date. The script uses a graphical interface (via `tkinter`) for selecting input PDFs and the output file.

## Features
- Extracts transaction details ("Date", "Description", "Amount") from PDF credit card statements.
- Deduces transaction year by comparing transaction month (e.g., "10 Dec") to the statement date (e.g., "10 Jan 2025").
- Supports batch processing of multiple PDFs.
- Outputs a tab-delimited text file with transaction data.
- Uses a file selection dialog for user-friendly input and output file selection.

## Requirements
- Python 3.6 or higher
- `pdfplumber` library for PDF parsing
- `tkinter` (usually included with Python; ensure it's installed on your system)

## Installation
1. **Install Python**: Ensure Python 3.6+ is installed. Download from [python.org](https://www.python.org/downloads/) if needed.
2. **Install Dependencies**: Install `pdfplumber` using pip:
   ```bash
   pip install pdfplumber
   ```
3. **Clone the Repository**: Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/SC_smart_import.git
   cd SC_smart_import
   ```

## Usage
1. **Run the Script**:
   ```bash
   python SC_smart_import.py
   ```
2. **Select Input PDFs**:
   - A file selection dialog will open.
   - Choose one or more PDF files (hold Ctrl or Shift for multiple selections).
3. **Select Output File**:
   - Another dialog will prompt for the output file location and name (e.g., `output.txt`).
   - The file will be created with a `.txt` extension if not specified.
4. **Output**:
   - The script processes the PDFs and writes transactions to the specified tab-delimited text file.
   - The output file will have columns: `Date` (YYYY-MM-DD), `Description`, `Amount`.

## Input Format
- **PDFs**: Credit card statement PDFs with transactions listed as text lines (not tables).
- **Transaction Lines**: Each line should contain:
  - Date: Format "DD Mon" (e.g., "10 Dec").
  - Description: Any text describing the transaction (e.g., "OCL* OCTOPUS AD50428KOWLOON BAY HK Transaction Ref 74481324345500001490184").
  - Amount: Numeric value with optional currency symbols or signs (e.g., "123.45", "$123.45", "-123.45").
- **Statement Date**: Expected on the first page in the format "DD Mon YYYY" (e.g., "10 Jan 2025").

## Output Format
The output is a tab-delimited text file (e.g., `output.txt`) with the following columns:
- `Date`: Transaction date in YYYY-MM-DD format (year deduced from statement date).
- `Description`: Full transaction description from the PDF.
- `Amount`: Transaction amount as extracted.

Example output:
```
Date        Description                                                      Amount
2024-12-10  OCL* OCTOPUS AD50428KOWLOON BAY HK Transaction Ref 74481324345500001490184  450.00
2024-12-15  UNICORN STORES TAIKOHONG KONG HK Transaction Ref 74552354351112000533451    23.00
```

## How It Works
- **Date Deduction**: For each transaction date (e.g., "10 Dec"), the script compares the month to the statement date's month. If the transaction month is later than the statement month, it assigns the previous year (e.g., if statement date is "10 Jan 2025", "10 Dec" becomes "2024-12-10").
- **Text Extraction**: Uses `pdfplumber` to extract text lines from PDFs and regex to match transaction lines.
- **File Selection**: Uses `tkinter` for a graphical interface to select input PDFs and the output text file.
- **Error Handling**: Skips invalid lines, missing files, or PDFs without a statement date, with appropriate warnings.

## Troubleshooting
- **No Transactions Extracted**:
  - Ensure transaction lines in the PDF match the expected format (e.g., "10 Dec Grocery Store 123.45").
  - Verify the statement date is on the first page in "DD Mon YYYY" format.
  - Check if the PDF is text-based (not a scanned image). Scanned PDFs require OCR, which this script does not support.
  - Enable debug output by uncommenting `print(line)` in the `extract_transactions` function to inspect extracted lines.
- **Deprecation Warning**: If you see a `DeprecationWarning` about date parsing, the script uses a placeholder year (2000) to avoid issues, compatible with Python 3.15+.
- **File Not Found**: Ensure selected PDFs exist and are accessible.
- **Incorrect Date Deduction**: If transaction years are incorrect, verify the statement date format and ensure transaction dates are in "DD Mon" format.
