import os
import re

def sanitize_filename(filename):
    """
    Removes forbidden characters (', [, ], ;) from a filename.

    Args:
        filename (str): The filename to sanitize.

    Returns:
        str: The sanitized filename.
    """
    return re.sub(r"['\[\];]", "_", filename)

def get_unique_filepath(dir_path, base_name, extension):
    """
    Generates a unique filepath by appending a counter if the file exists.

    Args:
        dir_path (str): The directory where the file will be located.
        base_name (str): The base name of the file (without extension).
        extension (str): The file extension (e.g., ".pdf").

    Returns:
        str: A unique filepath.
    """
    filepath = os.path.join(dir_path, f"{base_name}{extension}")
    if not os.path.exists(filepath):
        return filepath  # Original name is unique
    else:
        counter = 1
        while True:
            new_name = f"{base_name}_{counter}{extension}"
            new_filepath = os.path.join(dir_path, new_name)
            if not os.path.exists(new_filepath):
                return new_filepath  # Found a unique name
            counter += 1

def rename_pdf_files(root_folder):
    """
    Renames PDF files within subfolders of a given root folder.

    This function assumes the root folder contains subfolders named after years
    (e.g., 1950, 1951, etc.), and each year folder contains PDF files to be renamed.
    """
    print(f"Processing PDF files in: {root_folder}")  # Inform the user

    for year_folder in os.listdir(root_folder):  # Iterate through items in root
        year_path = os.path.join(root_folder, year_folder)  # Full path to year folder

        # Check if it's a directory, a year folder, and within the range
        if os.path.isdir(year_path) and year_folder.isdigit() and 1950 <= int(year_folder) <= 2025:
            print(f"  Processing year folder: {year_folder}")  # Indicate year folder

            for filename in os.listdir(year_path):  # Iterate files in year folder
                if filename.lower().endswith(".pdf"):  # Case-insensitive check for .pdf
                    old_filepath = os.path.join(year_path, filename)
                    name, extension = os.path.splitext(filename)
                    sanitized_name = sanitize_filename(name)  # Clean the filename
                    new_filepath = get_unique_filepath(year_path, sanitized_name, extension)

                    if old_filepath != new_filepath:
                        try:
                            os.rename(old_filepath, new_filepath)
                            print(f"    Renamed: {filename}  -->  {os.path.basename(new_filepath)}")
                        except OSError as e:
                            print(f"    Error renaming: {filename}  -  {e}")
                    else:
                        print(f"    Skipped: {filename} (no change needed)")

    print("Finished processing PDF files.")  # Indicate completion

if __name__ == "__main__":
    #  Set this to the path of your 'supreme_court_judgments' folder.
    #  Example (Windows):  r'C:\Users\YourUsername\Documents\supreme_court_judgments'
    #  Example (macOS/Linux): '/Users/YourUsername/Documents/supreme_court_judgments'
    root_directory = r'D:\Legal_Aid_Chatbot\Law Data\supreme_court_judgments'
    rename_pdf_files(root_directory)
