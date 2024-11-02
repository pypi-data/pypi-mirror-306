import os
from jinja2 import Environment, FileSystemLoader


def render_template_file(template_file: str, **kwargs):
    """
    Renders a given template file.

    Args:
        template_file (str): template file path
        kwargs: variables passed to the template

    Returns:
        str
    """
    env = Environment(loader=FileSystemLoader(os.path.dirname(template_file)))
    template_file = env.get_template(os.path.basename(template_file))
    return template_file.render(**kwargs)
