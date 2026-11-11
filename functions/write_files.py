import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "writes a file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The file name and optional relative directory path of the file to write.",
                },
                "content": {
                    "type": "string",
                    "description": "the content for the file (that will be written)",
                }
            },
            "required": ["file_path", "content"],
        },
    },
}



def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, target_file]) != abs_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working file_path'
        if  os.path.isdir(target_file):
            return f'Error: "{file_path}" is a directory'
        #LOGIC
        os.makedirs(os.path.dirname(target_file),exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return  f"Error: writing files: {e}"