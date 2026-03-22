import os 
from pathlib import Path 
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content in a provided file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path relative to working drectory",
            )
        }
    )
)
def get_file_content(working_directory:str, file_path:str):
    try:
        
        abs_working_dir = os.path.abspath(working_directory)
        print(f"{abs_working_dir=}")
        normalized_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
        print(f"{normalized_path=}")
        if os.path.commonpath([abs_working_dir, normalized_path]) != abs_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        with open(normalized_path, 'r') as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content
    except Exception as ex:
        return f"Error: {ex}"