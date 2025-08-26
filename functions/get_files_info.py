import os

# Try to import genai types, but don't crash the module if it fails
try:
    from google.genai import types
except Exception:
    types = None  # we'll build with a local import later

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

def build_schema_get_files_info():
    """
    Build the FunctionDeclaration at call-time so import never fails.
    """
    # Import here to guarantee availability at runtime
    from google.genai import types as _types
    return _types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=_types.Schema(
            type=_types.Type.OBJECT,
            properties={
                "directory": _types.Schema(
                    type=_types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )

# Best-effort eager schema (won't crash import if types wasn't ready)
try:
    schema_get_files_info = build_schema_get_files_info() if types is not None else None
except Exception:
    schema_get_files_info = None

__all__ = ["get_files_info", "schema_get_files_info", "build_schema_get_files_info"]
