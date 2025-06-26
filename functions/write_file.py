import os

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
    if not target_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    try:
        #Check if path to file exists from working directory, if not, create it
        target_dir = os.path.dirname(target_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
    except Exception as e:
        return f"Error generating filepath: {e}"
    try:
        #Try to write or overwrite the contents of the file
        with open(target_path, "w") as f:
            f.write(content)
    except Exception as e:
        return f"Error writing to file: {e}"
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'