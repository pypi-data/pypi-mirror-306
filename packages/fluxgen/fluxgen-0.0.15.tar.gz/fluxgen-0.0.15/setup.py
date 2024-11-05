import os

from setuptools import find_packages, setup  # noqa: H301

DESCRIPTION = "Helper tool to install and configure Flux Framework"

# Try to read description, otherwise fallback to short description
try:
    with open(os.path.abspath("README.md")) as filey:
        LONG_DESCRIPTION = filey.read()
except Exception:
    LONG_DESCRIPTION = DESCRIPTION

# Read in the version
# This is a bit janky I admit :)
with open(os.path.join("fluxgen", "__init__.py")) as fd:
    version = fd.read().strip().replace("__version__ = ", "").replace('"', "")

################################################################################
# MAIN #########################################################################
################################################################################

if __name__ == "__main__":
    setup(
        name="fluxgen",
        version=version,
        author="Vanessasaurus",
        author_email="vsoch@users.noreply.github.com",
        maintainer="Vanessasaurus",
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        url="https://github.com/converged-computing/fluxgen",
        license="MIT",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        keywords="multi-cluster, scheduler",
        setup_requires=["pytest-runner"],
        install_requires=[
            "Jinja2",
            "pyyaml",
        ],
        classifiers=[
            "Intended Audience :: Science/Research",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: Apache Software License",
            "Programming Language :: C",
            "Programming Language :: Python",
            "Topic :: Software Development",
            "Topic :: Scientific/Engineering",
            "Operating System :: Unix",
            "Programming Language :: Python :: 3.11",
        ],
        entry_points={
            "console_scripts": [
                "fluxgen=fluxgen.client:run_fluxgen",
            ]
        },
    )
