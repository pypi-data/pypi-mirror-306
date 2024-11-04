from fluxgen.template import Template

# Optional arguments (with defaults)
# I don't see the need to expose these (will do when there is reason)
# - mamba_prefix
# - python_version
# - linkname (should be discovered if not provided)
# - command (should be added if being used)


class FluxInstallScript:
    # Required template variables
    # Note this isn't currently used
    required = ["lead-broker", "brokers"]

    # Defaults
    # Optional:
    # mamba_prefix

    def __init__(self):
        """
        Create a new installl script.

        The kwargs are expected to be variables for the template.
        """
        self.template = Template("install-flux.sh")

    def render(self, **vars):
        """
        Render the variables into the template
        """
        for varname in self.required:
            if varname not in vars or vars[varname] is None:
                raise ValueError(f"{varname} is required.")

            # Convert "-" to _ for jinja2
            if "-" in varname:
                updated = varname.replace("-", "_")
                vars[updated] = vars[varname]

        # Brokers needs to be list
        brokers = vars["brokers"]

        # Command should be a string
        command = vars.get("command")
        if command is not None and isinstance(command, list):
            vars["command"] = " ".join(command)

        if not isinstance(brokers, list):
            brokers = [x.strip() for x in brokers.split(",") if x.strip()]
            vars["brokers"] = brokers
        return self.template.render(**vars)

    @classmethod
    def get_required(cls):
        return cls.required
