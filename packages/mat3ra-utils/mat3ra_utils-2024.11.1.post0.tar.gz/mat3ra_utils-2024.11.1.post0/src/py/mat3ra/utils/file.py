import os
import fcntl


def get_file_content(file_path: str) -> str:
    """
    Returns the content of a given file.

    Args:
        file_path (str): file path.

    Returns:
         str
    """
    content = ""
    if file_path and os.path.exists(file_path):
        with open(file_path) as f:
            content = f.read()
    return content


def append_line_to_file(line: str, file_path: str, add_newline: bool = True):
    """
    Append line to given file.

    Args:
        line (str): line to add. End of line (EOL) is added automatically.
        file_path (str): file path
    """
    with open(file_path, "a+") as f:
        f.write(line + "\n" if add_newline else "")


def remove_line_containing_pattern(pattern: str, file_path: str):
    """
    Removes line containing given pattern form the file.

    Args:
        pattern (str): pattern to look for.
        file_path (str): file path
    """
    with open(file_path, "r+") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        lines = f.readlines()
        f.seek(0)
        f.truncate()
        for line in lines:
            if pattern not in line:
                f.write(line)
