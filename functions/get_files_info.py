import os

def get_files_info(working_directory, directory=None):
    abs_working_dir = os.path.abspath(working_directory)
    target_path = abs_working_dir
    if directory:
        target_path = os.path.abspath(os.path.join(abs_working_dir, directory))
    if (os.path.isdir(target_path) == False):
        return f'Error: "{directory}" is not a directory'
    if not target_path.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    try:
        files_info = []
        for filename in os.listdir(target_path):
            filepath = os.path.join(target_path, filename)
            file_size = 0
            is_dir = os.path.isdir(filepath)
            file_size = os.path.getsize(filepath)
            files_info.append(
                f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}"
            )
        return "\n".join(files_info)
    except Exception as e:
        return f"Error listing files: {e}"