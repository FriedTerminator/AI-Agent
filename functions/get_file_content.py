import os
from google.genai import types

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
            file_content_string = f.read()
            if len(file_content_string) > MAX_CHARACTERS:
                file_content_string = file_content_string[:MAX_CHARACTERS]
                file_content_string += f"\n[...File \"{full_path}\" truncated at 10000 characters]"
            return file_content_string
    except Exception as e:
        return f"Error: {str(e)}"
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the full contents of a file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file": types.Schema(
                type=types.Type.STRING,
                description="The file to read.",
            ),
        },
        required=["file"],
    ),
)