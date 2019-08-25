def read_file(file_path: str) -> str:
    """Read a file and returns it's contents (as a string), raise FileNotFoundError if file does not exist

     Arguments:
    file_path -- the path of the file to be read
    """
    with open(file_path) as f:
        file_contents = f.read()
    return file_contents
