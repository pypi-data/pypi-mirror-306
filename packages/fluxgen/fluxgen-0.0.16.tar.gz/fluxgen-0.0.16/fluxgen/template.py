import os

from jinja2 import Environment, FileSystemLoader

here = os.path.dirname(os.path.abspath(__file__))

# Allow includes from this directory OR providing strings
template_dir = os.path.join(here, "templates")
env = Environment(loader=FileSystemLoader(template_dir))


class Template:
    """
    Supporting functions for loading a script template.
    """

    def __init__(self, template_file):
        self.get(template_file)

    def get(self, template_name):
        """
        Get a template from templates
        """
        template_file = os.path.join(here, "templates", template_name)
        if not os.path.exists(template_file):
            template_file = os.path.abspath(template_name)
        if not os.path.exists(template_file):
            raise ValueError(f"template file {template_file} does not exist.")
        self.template_file = template_file

    def render(self, **vars):
        """
        Load varibles into the template
        """
        with open(self.template_file, "r") as temp:
            template = env.from_string(temp.read())
        return template.render(vars)
