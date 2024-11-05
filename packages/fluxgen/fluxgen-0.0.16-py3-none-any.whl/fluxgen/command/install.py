from fluxgen.template import Template

# Optional arguments (with defaults)
# I don't see the need to expose these (will do when there is reason)
# - mamba_prefix
# - python_version


class FluxInstallScript:
    required = []

    # Defaults
    # Optional:
    # mamba_prefix

    def __init__(self):
        """
        Create a new installl script.
        """
        self.template = Template("install-flux.sh")

    def render(self, **vars):
        """
        Render the variables into the template
        """
        return self.template.render(install_only=True)

    @classmethod
    def get_required(cls):
        return cls.required
