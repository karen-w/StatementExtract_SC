import pdfplumber
import re
from datetime import datetime
import os
import tkinter as tk
from tkinter import filedialog

def parse_date(transaction_date_str, statement_date):
    """Deduce the full transaction date from transaction date string and statement date."""
    try:
        # Use a placeholder year (2000, a leap year) to avoid deprecation warning
        trans_date = datetime.strptime(f"{transaction_date_str} 2000", "%d %b %Y")
    except ValueError:
        return None  # Skip if date format is invalid

    # Get statement year and month
    stmt_year = statement_date.year
    stmt_month = statement_date.month
    trans_month = trans_date.month

    # Deduce year: if transaction month is later than statement month, use previous year
    trans_year = stmt_year if trans_month <= stmt_month else stmt_year - 1
    return trans_date.replace(year=trans_year)

def extract_statement_date(pdf_path):
    """Extract statement date from the first page of the PDF."""
    with pdfplumber.open(pdf_path) as pdf_file:
        first_page = pdf_file.pages[0]
        text = first_page.extract_text()
        if text:
            # Look for date pattern like "10 Jan 2025"
            date_match = re.search(r"\d{1,2}\s+[A-Za-z]{3}\s+\d{4}", text)
            if date_match:
                try:
                    return datetime.strptime(date_match.group(), "%d %b %Y")
                except ValueError:
                    pass
    return None

def extract_transactions(pdf_path, statement_date):
    """Extract transactions from a single PDF by parsing text lines."""
    transactions = []
    # Regex to match a line with date (DD Mon), description, and amount
    # Handles: "10 Dec Grocery Store 123.45", "10 Dec Grocery Store $123.45", "10 Dec Cafe -123,45"
    pattern = re.compile(r"(\d{1,2}\s+[A-Za-z]{3})\s+(.+?)\s+([\$€£]?-?\d+[,.]?\d{0,2}(?:-|\+)?)$")
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            # Split text into lines
            lines = text.split("\n")
            print(f"Processing page with {len(lines)} lines in {pdf_path}")
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                match = pattern.match(line)
                if match:
                    trans_date_str = match.group(1).strip()  # e.g., "10 Dec"
                    description = match.group(2).strip()      # e.g., "Grocery Store"
                    amount = match.group(3).strip()          # e.g., "123.45" or "-123,45"
                    print(f"Match found: Date={trans_date_str}, Description={description}, Amount={amount}")
                    trans_date = parse_date(trans_date_str, statement_date)
                    if trans_date:
                        transactions.append({
                            "Date": trans_date.strftime("%Y-%m-%d"),
                            "Description": description,
                            "Amount": amount
                        })
                else:
                    print(f"No match for line: {line}")
    return transactions

def select_files():
    """Open a file selection dialog to choose multiple PDF files."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    pdf_paths = filedialog.askopenfilenames(
        title="Select PDF Files",
        filetypes=[("PDF files", "*.pdf")]
    )
    return list(pdf_paths)

def select_output_file():
    """Open a dialog to select the output text file."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    output_file = filedialog.asksaveasfilename(
        title="Select Output File",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")]
    )
    return output_file

def process_pdfs(pdf_paths, output_file):
    """Process multiple PDFs and write transactions to a tab-delimited file."""
    if not output_file:
        print("No output file selected.")
        return
    all_transactions = []
    for pdf_path in pdf_paths:
        if not os.path.exists(pdf_path):
            print(f"Warning: {pdf_path} does not exist.")
            continue
        statement_date = extract_statement_date(pdf_path)
        if not statement_date:
            print(f"Warning: Could not extract statement date from {pdf_path}.")
            continue
        transactions = extract_transactions(pdf_path, statement_date)
        if not transactions:
            print(f"Warning: No transactions found in {pdf_path}.")
        all_transactions.extend(transactions)
    
    # Write to tab-delimited file
    with open(output_file, "w", encoding="utf-8") as f:
        # Write header
        f.write("Date\tDescription\tAmount\n")
        # Write transactions
        for trans in all_transactions:
            f.write(f"{trans['Date']}\t{trans['Description']}\t{trans['Amount']}\n")
    print(f"Transactions written to {output_file}")

if __name__ == "__main__":
    pdf_paths = select_files()
    if not pdf_paths:
        print("No PDF files selected.")
    else:
        output_file = select_output_file()
        if output_file:
            process_pdfs(pdf_paths, output_file)
        else:
            print("No output file selected.")