# Configuration file for the Sphinx documentation builder.
#
# This is a generic configuration that can be plugged in as is, but
# requires jq as too to be present (and you cannot build on
# windows). If you want to avoid this requirement, you will have to
# remove the code that fills git_status, project_name and author_name
# and replace these variables in the next section by constants.

import subprocess
from conf_project import author, project, year  # noqa - reexporting

source_version = subprocess.run(
    ['hatch', 'version'],
    check = True, capture_output = True, encoding = 'utf-8'
).stdout.strip()

git_status = [
    line
    for line in
    subprocess.run(
        "cd $(git rev-parse --show-toplevel); git status -s",
        check = True, capture_output = True, encoding = 'utf-8', shell = True
    ).stdout.strip("\n ").split("\n")
    if line
]

dirty = " [DIRTY]" if git_status else ""


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

copyright = f'{year}, {author}'
release   = source_version + dirty

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'literate_sphinx'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

napoleon_custom_sections = [
    ("Usage example", "Example"),
    ("Usage examples", "Examples")
]

add_module_names = False
autodoc_typehints = 'both'
autodoc_typehints_description_target = 'all'
autodoc_typehints_format = 'short'

# -- Common/global RST roles -------------------------------------------------


rst_prolog = """

.. role:: py-code(code)
   :language: python
"""

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
