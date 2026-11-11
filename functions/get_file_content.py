import os
import config

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Outputs the content of the file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The file name and optional relative directory path of the file to read.",
                },
            },
            "required": ["file_path"],
        },
    },
}


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working file_path'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" is not a file'
        #HERE GOES LOGIC
        with open(target_file, "r") as f:
            file_content_string = f.read(config.MAX_CHARS)
            if f.read(1):
                file_content_string += f'[{file_path} truncated: True ]'
            return file_content_string
    except Exception as e:
         return f"Error: listing files: {e}"
