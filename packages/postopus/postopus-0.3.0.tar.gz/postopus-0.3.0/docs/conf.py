import importlib.metadata
import os

# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------
project = "postopus"
copyright = "2022, MPSD"


# environment variable used in CI to build a dev version of postopus on a tag pipeline,
# which is required to have a complete webpage (with dev at the root)
version = os.environ.get("CI_POSTOPUS_VERSION", importlib.metadata.version("postopus"))
if "dev" in version:
    version = "dev"
release = version

# -- General configuration ---------------------------------------------------

# The suffix of source filenames.
source_suffix = ".rst"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "nbsphinx",
    "pydata_sphinx_theme",
]

# Add any paths that contain templates here, relative to this directory.
# templates_path = ["_templates"]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", ".venv"]

intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}

# -- Options for HTML output -------------------------------------------------
html_theme = "pydata_sphinx_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_theme_options = {
    "check_switcher": False,  # json not available during build
    "switcher": {
        # `versions.json` is always taken from the current main (root of the postopus
        # documentation). The file is generated in the pages CI job based on the
        # available artifacts using the script `.gitlab/multiversion.py`
        "json_url": "https://octopus-code.gitlab.io/postopus/_static/versions.json",
        "version_match": version,
    },
    "navbar_start": ["navbar-logo", "version-switcher"],
    "logo": {
        "text": "Postopus",
    },
    "secondary_sidebar_items": ["page-toc"],
    "icon_links": [
        {
            "name": "GitLab",
            "url": "https://gitlab.com/octopus-code/postopus",
            "icon": "fa-brands fa-gitlab",
        },
    ]
}
html_sidebars = {
    "application_examples": [],
    "notebooks/Quick_Start": [],
    "changelog": [],
    "api/modules": [],
}
