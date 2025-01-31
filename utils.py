import os


def read_markdown_file(file_path: str) -> str:
    """
    Read content from a markdown file.
    
    Args:
        file_path (str): Path to the markdown file
        
    Returns:
        str: Content of the markdown file
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        IOError: If there's an error reading the file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} was not found")
    except IOError as e:
        raise IOError(f"Error reading file {file_path}: {str(e)}")