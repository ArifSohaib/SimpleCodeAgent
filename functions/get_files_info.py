from pathlib import Path 
import os 
from google.genai import types 

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
                default="."
            )
        }
    )
)
def get_files_info(working_directory, directory="."):
    result_str = []
    if directory == ".":
        current_directory = "current"
    else: 
        current_directory = directory
    result_str.append(f"Result for {current_directory} directory:")
    try:
        
        abs_path_workdir = os.path.abspath(working_directory)

        target_dir = os.path.normpath(os.path.join(abs_path_workdir, directory))

        if os.path.commonpath([abs_path_workdir, target_dir]) != abs_path_workdir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not Path(target_dir).is_dir():
            return f'Error: "{directory}" is not a directory'
        for item in Path(target_dir).iterdir():
            result_str.append(f"{item.name}, file_size={item.stat().st_size}, is_dir={item.is_dir()}\n")
        return "".join(result_str)
    except  Exception as ex:
        return f"Error: {ex}"