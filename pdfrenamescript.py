import os
import requests
import re

# Define the path to the directory containing the PDF files
pdf_directory = r'D:\sad'

def get_book_metadata(isbn):
    """Fetch book title and author from Google Books API."""
    url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}'
    response = requests.get(url)
    
    # Debugging: Print the status code and response
    print(f"Request URL: {url}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
    
    data = response.json()
    
    if 'items' in data:
        volume_info = data['items'][0]['volumeInfo']
        title = volume_info.get('title', 'Unknown Title')
        authors = volume_info.get('authors', ['Unknown Author'])
        return title, ', '.join(authors)
    return None, None

def sanitize_filename(filename):
    """Remove or replace invalid characters in filenames."""
    # Define invalid characters for Windows
    invalid_chars = r'\/:*?"<>|'
    sanitized = re.sub(f'[{invalid_chars}]', '', filename)
    return sanitized

def rename_pdfs(directory):
    """Rename PDF files based on their ISBN number."""
    for filename in os.listdir(directory):
        if filename.lower().endswith('.pdf'):
            isbn = filename.replace('.pdf', '')
            title, authors = get_book_metadata(isbn)
            
            if title and authors:
                # Create a sanitized filename
                sanitized_title = sanitize_filename(title)
                sanitized_authors = sanitize_filename(authors)
                new_filename = f'{sanitized_title} - {sanitized_authors}.pdf'
                
                old_file_path = os.path.join(directory, filename)
                new_file_path = os.path.join(directory, new_filename)
                
                # Rename the file
                try:
                    os.rename(old_file_path, new_file_path)
                    print(f'Renamed "{filename}" to "{new_filename}"')
                except OSError as e:
                    print(f"Error renaming file {filename}: {e}")
            else:
                print(f'No metadata found for ISBN {isbn}')

if __name__ == "__main__":
    rename_pdfs(pdf_directory)
