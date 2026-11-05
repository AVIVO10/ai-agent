import os
import subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working file_path'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist'
        if not (file_path[-3:] == ".py"):
            return f'Error: "{file_path}" is not a Python file'
        #LOGIC
        command = ["python", target_file]
        if not args == None:
            command.extend(args)
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        output_string = ""
        if not (result.returncode == 0):
            output_string += f"Process exited with code {result.returncode}"
        if result.stdout == "" and result.stderr == "":
            output_string += "No output produced"
        else:
            output_string += f"STDOUT: {result.stdout} STDERR: {result.stderr}"
        return output_string


    except Exception as e:
        return f"Error: executing Python file: {e}"