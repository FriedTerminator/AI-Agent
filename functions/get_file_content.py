import os

MAX_CHARACTERS = 10000

def get_file_content(working_directory, file_path):
    try: 
        working_directory_abs = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not full_path.startswith(working_directory_abs):
            return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"
        
        if not os.path.isfile(full_path):
            return f"Error: File is not found or is not a regular file: \"{file_path}\""
        
        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARACTERS)
            return file_content_string
    except Exception as e:
        return f"Error: {str(e)}"