import os
import subprocess

def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
    if not target_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target_path):
        return f'Error: File "{file_path}" not found.'
    if not target_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        print(target_path)
        result = subprocess.run(["python3", target_path], capture_output=True, text=True, check=True, timeout=30)
        if result.stdout:
            return f"STDOUT: {result.stdout}", f"STDERR: {result.stderr}"
        else:
            return "No output produced."

    except subprocess.CalledProcessError as e:
        return f"Process exited with code {e.returncode}" 
    except Exception as e:
        return f"Error: executing Python file: {e}"
    return target_path