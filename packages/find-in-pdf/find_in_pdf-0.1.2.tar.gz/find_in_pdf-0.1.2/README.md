# PDFSearcher

PDFSearcher is a simple Python tool for searching a specific string within PDF files located in a specified directory and its subdirectories. It outputs the file paths where the string is found.

## Features

- Recursively searches for a given string in all PDF files within a folder and its subfolders.
- Prints out the paths of the PDF files where the search string is found.
- Easy to install and use.

## Installation

You can install the package via `pip` after uploading it to PyPI:

```bash
pip install find-in-pdf
```

Or, you can install it locally by cloning the repository and using:

```bash
pip install .
```

## Usage

To use pdfsearcher in your Python code, you can simply import it and call the search_pdfs_in_folder function.

```bash
from pdfsearcher import search_pdfs_in_folder

# Example usage
folder_path = "/path/to/folder"
search_string = "your search string"
search_pdfs_in_folder(folder_path, search_string)
```

You can also use it as a command-line tool:

```bash
pdfsearcher /path/to/folder "search string"
```