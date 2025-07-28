import os

def get_files_info(working_directory, directory="."):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(working_directory, directory))

        if not full_path.startswith(working_directory_abs):
            return f"Error: cannot list \"{directory}\" as it is outside the permitted working directory"
        
        if not os.path.isdir(full_path):
            return f"Error: \"{directory}\" is not a directory"
        
        entries = []
        for entry in os.listdir(full_path):
            entry_path = os.path.join(full_path, entry)
            size_of_content = os.path.getsize(entry_path)
            is_dir = os.path.isdir(entry_path)
            entries.append(f"- {entry}: file_size={size_of_content} bytes, is_dir={is_dir}")
        return "\n".join(entries)
    except Exception as e:
        return f"Error: {str(e)}"
    
    