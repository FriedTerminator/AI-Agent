from google.genai import types

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

FUNCTION_MAP = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file
}

WORKING_DICT = "./calculator"

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

def call_function(function_call_part, verbose=False):
    name = function_call_part.name
    raw_args = dict(function_call_part.args or {})

    if verbose:
        print(f"Calling function: {name}({function_call_part.args})")
    else:
        print(f" - Calling function: {name}")

    func = FUNCTION_MAP[name]    

    if func is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={"error": f"Unknown function: {name}"},
                )
            ],
        )
    
    try:
        if name == "get_files_info":
            directory = raw_args.get("directory", ".")
            function_result = func(WORKING_DICT, directory)
        elif name == "get_file_content":
            function_result = func(WORKING_DICT, raw_args["file"])
        elif name == "write_file":
            function_result = func(WORKING_DICT, raw_args["file"], raw_args["content"])
        elif name == "run_python_file":
            function_result = func(WORKING_DICT, raw_args["file"])
        else:
            function_result = func(working_directory=WORKING_DICT, **raw_args)
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[types.Part.from_function_response(
                name=name, response={"error": f"{type(e).__name__}: {e}"},
            )],
        )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=name,
                response={"result": function_result},
            )
        ],
    )