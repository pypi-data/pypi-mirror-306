import argparse
import csv
import os
import re
from datetime import datetime

import pdfplumber


def search_pdfs_in_folder(folder_path, search_string):
    found_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                file_path = os.path.join(root, file)
                try:
                    with pdfplumber.open(file_path) as pdf:
                        for page_num, page in enumerate(pdf.pages):
                            text = page.extract_text()

                            # Search for the string in the regular text
                            if text and search_string.lower() in text.lower():
                                found_paths.append(file_path)
                                break

                            # Search for the string in table data
                            table = page.extract_table()
                            if table:
                                for row in table:
                                    row_text = ' '.join(filter(None, row))  # Join non-empty cells
                                    if search_string.lower() in row_text.lower():
                                        found_paths.append(file_path)
                                        break
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    if found_paths:
        print(f"Search string '{search_string}' found in the following files:")
        for path in found_paths:
            print(path)

        # Save results to a text file with error handling
        results_file_path = f"{search_string}_results.txt"
        try:
            with open(results_file_path, 'w') as results_file:
                for path in found_paths:
                    results_file.write(path + '\n')
            print(f"Results saved to '{results_file_path}'.")
        except Exception as e:
            print(f"Error writing to file '{results_file_path}': {e}")
    else:
        print(f"Search string '{search_string}' not found in any PDF files.")
    return found_paths


def extract_date_from_filename(filename):
    """Extracts the date from the filename in YYYYMMDD format and returns a datetime object."""
    date_pattern = re.compile(r'_([0-9]{8})\.pdf$')
    match = date_pattern.search(filename)
    if match:
        date_str = match.group(1)
        return datetime.strptime(date_str, "%Y%m%d")
    return None


def exclude_summary_pages(reader):
    """Finds the page with 'Summary of Changes' and returns pages to search up to that page."""
    for page_num in range(len(reader.pages)):
        text = reader.pages[page_num].extract_text()
        if text and "Summary of Changes" in text:
            return range(page_num)  # Exclude from this page onwards
    return range(len(reader.pages))  # Include all pages if no summary found


def extract_products_from_pdf(file_path):
    """Extracts unique product codes in the format 'NNNNNN-B21' from a PDF file, excluding pages after 'Summary of Changes'."""
    product_pattern = re.compile(r'\b\d{6}-B21\b')
    products = set()

    try:
        with pdfplumber.open(file_path) as pdf:
            pages_to_search = exclude_summary_pages(pdf)
            for page_num in pages_to_search:
                page = pdf.pages[page_num]
                text = page.extract_text()

                # Search for product IDs in regular text
                if text:
                    found_products = product_pattern.findall(text)
                    products.update(found_products)

                # Search for product IDs in table data
                table = page.extract_table()
                if table:
                    for row in table:
                        row_text = ' '.join(filter(None, row))  # Join non-empty cells
                        found_products = product_pattern.findall(row_text)
                        products.update(found_products)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

    return products


def list_products(folder_path):
    pdf_files_with_dates = []

    # Collect PDF files with dates
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                date = extract_date_from_filename(file)
                if date:
                    file_path = os.path.join(root, file)
                    pdf_files_with_dates.append((file_path, date))

    # Sort files by date (ascending)
    pdf_files_with_dates.sort(key=lambda x: x[1])

    # Dictionary to store first and last appearance dates of each product
    product_dates = {}

    # Process each PDF file in ascending order of date
    for i, (file_path, date) in enumerate(pdf_files_with_dates):
        # print('--------')
        # print('file_path',file_path)

        products_in_file = extract_products_from_pdf(file_path)
        # print(products_in_file, 'products_in_file')
        # print('xxxxxxx')
        # Update the first and last appearance dates for each product
        for product in products_in_file:
            if product not in product_dates:
                # print("ITS NOT HERE!")
                # If product is found for the first time, record the date
                product_dates[product] = {"first_seen": date, "last_seen": date, "stopped_seen": None}
            else:
                # Update the last_seen date if product is already recorded
                product_dates[product]["last_seen"] = date

        # Check for products that are not in the current file but exist in product_dates
        for product in list(product_dates.keys()):
            if product not in products_in_file:
                # If it's the first time product is missing after being seen, set stopped_seen to this date
                if product_dates[product]["stopped_seen"] is None:
                    product_dates[product]["stopped_seen"] = date
    # Save the results to a CSV file
    with open('products.csv', mode='w', newline='') as csvfile:
        fieldnames = ['Product', 'First Seen', 'Stopped existing']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for product, dates in product_dates.items():
            first_seen = dates["first_seen"].strftime('%Y-%m-%d')
            stopped_seen = dates["stopped_seen"].strftime('%Y-%m-%d') if dates["stopped_seen"] else "Still present"
            writer.writerow({'Product': product, 'First Seen': first_seen, 'Stopped existing': stopped_seen})

    # # Print the results
    # print("Unique products with their first appearance and the date they were no longer found:")
    # for product, dates in product_dates.items():
    #     first_seen = dates["first_seen"].strftime('%Y-%m-%d')
    #     stopped_seen = dates["stopped_seen"].strftime('%Y-%m-%d') if dates["stopped_seen"] else "Still present"
    #     print(f"{product}, {first_seen}, {stopped_seen}")

    return product_dates


def main():
    parser = argparse.ArgumentParser(description="PDF utility: search PDF files in a folder or list products in PDFs.")
    parser.add_argument('mode', type=str, choices=['search', 'list'],
                        help="Specify 'search' to search PDFs, or 'list' to list all products in PDFs")
    parser.add_argument('folder_path', type=str, help='The path to the folder containing PDF files.')

    # Only required for 'search' mode
    parser.add_argument('search_string', type=str, nargs='?',
                        help='The string to search for in PDF files (only for search mode).')

    args = parser.parse_args()

    if args.mode == 'search':
        if not args.search_string:
            print("Error: search mode requires a search_string argument.")
            return
        search_pdfs_in_folder(args.folder_path, args.search_string)
    elif args.mode == 'list':
        list_products(args.folder_path)


if __name__ == "__main__":
    main()
