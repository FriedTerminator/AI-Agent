import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    working_directory_abs = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory_abs, file_path))

    if not full_path.startswith(working_directory_abs):
        return f'Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory'
    
    if not os.path.isfile(full_path):
        return f'Error: File \"{file_path}\" not found.'
    
    if not full_path.endswith(".py"):
        return f'Error: \"{file_path}\" is not a Python file.'
    
    try:
        cmd = ["python", full_path] + args

        completed_process = subprocess.run(cmd, capture_output=True, timeout=30)

        stdout = completed_process.stdout.decode()
        stderr = completed_process.stderr.decode()

        if completed_process.returncode != 0:
            error_message = f"Process exited with code {completed_process.returncode}"

            if not stdout and not stderr:
                return f"{error_message}\nNo output produced."
            return f"{error_message}\nSTDOUT: {stdout}\nSTDERR: {stderr}"
        return f"STDOUT: {stdout}\nSTDERR: {stderr}"
    except Exception as e:
        return f'Error: executing Pyton file: {e}'
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file": types.Schema(
                type=types.Type.STRING,
                description="The Python file to execute.",
            ),
        },
        required=["file"],
    ),
)