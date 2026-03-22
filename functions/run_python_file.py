import os 
from pathlib import Path 
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a provided python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the python file relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="List of arguments to pass to the function call",
                items=types.Schema(
                        type=types.Type.STRING, 
                        description="argument to pass to function call"
                    )
                
            )
        }
    )
)

def run_python_file(working_directory, file_path, args=None):
    print(f"attempting {working_directory=}, {file_path=}, {args=}")
    try:
        abs_work_dir = os.path.abspath(working_directory)
        norm_file_path = os.path.normpath(os.path.join(abs_work_dir, file_path))
        if os.path.commonpath([norm_file_path, abs_work_dir]) != abs_work_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(norm_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if Path(file_path).suffix != '.py':
            return f'Error: "{file_path}" is not a Python file'
        command= ["python", norm_file_path]
        if args:
            command.extend(args)
        print(f"command : {command}")
        completed_process = subprocess.run(command, 
                                        cwd=abs_work_dir, 
                                        capture_output=True,
                                        text=True, timeout=30)

        output_str = []
        if completed_process.returncode != 0:
            output_str.append("Process exited with code X")
        if completed_process.stderr == None and completed_process.stdout == None:
            output_str.append("No output produced")
        if completed_process.stderr != "":
            output_str.append(f"STDERR: {completed_process.stderr}")
        if completed_process.stdout != "":
            output_str.append(f"STDOUT: {completed_process.stdout}")
        return "".join(output_str)
    except Exception as ex:
        return f"Error: executing Python file: {ex}"



