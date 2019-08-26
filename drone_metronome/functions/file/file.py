from string import Template
from typing import Optional


def read_file(file_path: str) -> str:
    """Read a file and returns it's contents (as a string), raise FileNotFoundError if file does not exist

        Arguments:
            file_path -- the path of the file to be read
        Returns:
            file_contents -- a string of the file contents
    """
    with open(file_path) as f:
        file_contents = f.read()
    return file_contents


# populate string from template
def populate_template_string(pre_template_string: str, template_values_dict: Optional[dict]) -> str:
    """Takes a pre_template_string string and populates it with dynamic values from the given template_values_dict

        Arguments:
            pre_template_string -- a string to apply the templating to
            template_values_dict -- a dict of values to to be inserted in the template
        Returns:
            post_template_string -- the result string after the templating
    """
    if template_values_dict is None:
        template_values_dict = {}

    post_template_string = Template(pre_template_string).safe_substitute(template_values_dict)
    return post_template_string
