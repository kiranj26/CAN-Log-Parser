import os
import sys

def validate_file(file_path, description):
    """
    @brief Validate if the given file exists and is a valid file.

    @param file_path Path to file
    @param description Description of the file for error messages
    @return Absolute path of the file if valid, else exits the program
    """
    if not os.path.isfile(file_path):
        print(f"Error: The {description} '{file_path}' does not exist or is not a file.")
        sys.exit(1)
    return os.path.abspath(file_path)