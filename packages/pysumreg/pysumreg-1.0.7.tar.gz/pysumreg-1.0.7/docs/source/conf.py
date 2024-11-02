# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import json
import pathlib
import sys
import tomllib

sys.path.insert(0, str(pathlib.Path().absolute().parent.parent))
import pysumreg  # noqa

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

gh_org = "prjemian"
project = "pysumreg"
release = pysumreg.__version__
version = ".".join(release.split(".")[:2])

root_path = pathlib.Path(__file__).parent.parent.parent
with open(root_path / "pyproject.toml", "rb") as fp:
    toml = tomllib.load(fp)
metadata = toml["project"]

project = metadata["name"]
copyright = toml["tool"]["copyright"]["copyright"]
author = metadata["authors"][0]["name"]
description = metadata["description"]
rst_prolog = f".. |author| replace:: {author}"
github_url = f"https://github.com/{gh_org}/{project}",

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = """
    sphinx.ext.autodoc
    sphinx.ext.autosummary
    sphinx.ext.coverage
    sphinx.ext.githubpages
    sphinx.ext.inheritance_diagram
    sphinx.ext.mathjax
    sphinx.ext.todo
    sphinx.ext.viewcode
""".split()

templates_path = ["_templates"]
exclude_patterns = []

today_fmt = "%Y-%m-%d %H:%M"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_css_files = [
    "css/custom.css",
]
html_static_path = ["_static"]
html_theme = "pydata_sphinx_theme"
html_theme_options = {
   "github_url": "https://github.com/prjemian/pysumreg",
   "logo": {
      "image_dark": "pysumreg-logo-dark.png",
      "image_light": "pysumreg-logo-light.png",
   }
}
html_title = "PySumReg"
