import os
import PyPDF2
import argparse

def search_pdfs_in_folder(folder_path, search_string):
    found_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'rb') as pdf_file:
                        reader = PyPDF2.PdfReader(pdf_file)
                        for page_num in range(len(reader.pages)):
                            page = reader.pages[page_num]
                            text = page.extract_text()
                            if text and search_string.lower() in text.lower():
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

def main():
    # Argument parser to accept folder path and search string from the command line
    parser = argparse.ArgumentParser(description="Search for a string in PDF files within a folder.")
    parser.add_argument('folder_path', type=str, help='The path to the folder containing PDF files.')
    parser.add_argument('search_string', type=str, help='The string to search for in PDF files.')

    args = parser.parse_args()

    # Call the function with arguments from the command line
    search_pdfs_in_folder(args.folder_path, args.search_string)

if __name__ == "__main__":
    main()
