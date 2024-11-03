import os
from yaspin import yaspin



def process_file(file_path):
    """Reads the content of a file and returns it as a string."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()  # Store file content in a string
            return content
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None




@yaspin(text="Scanning project...")
def process_directory(directory)-> str:
    loader = yaspin()
    loader.start()
    """Walks through the directory and reads each file's content into a string."""
    
    # Walk through the directory and its subdirectories
    folders_to_ignore = [".pytest_cache", "__pycache__", "node_modules", "documents", "dist", "ano_code.egg-info", "auto-code-env"]

    fl = {".py", ".js", ".go", ".ts", ".tsx", ".jsx", ".dart"}
    
    code = ""
    for root, dirs, files in os.walk(directory):
        # Modify dirs in-place to exclude specific directories
        dirs[:] = [d for d in dirs if d not in folders_to_ignore]
        for filename in files:
        # Check if the file has an excluded extension
            if filename.endswith(tuple(fl)):
                        file_path = os.path.join(root, filename)
                        content = process_file(file_path)  # Read file into a string
                        if content is not None:
                            
                            if filename:
                                code += f"{content}\n"

    loader.stop()
    return code

