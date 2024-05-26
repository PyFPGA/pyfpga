# -*- coding: utf-8 -*-

import sys, re
from pathlib import Path

sys.path.insert(0, str(Path.cwd().resolve().parent))

# -- Project information -----------------------------------------------------

project = 'PyFPGA'
copyright = '2024, Rodrigo Alejandro Melo'
author = 'Rodrigo Alejandro Melo'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
]

autodoc_default_options = {
    "members": True,
    'undoc-members': True,
    'inherited-members': True,
}

extlinks = {
   'repositoy': ('https://github.com/PyFPGA/pyfpga/tree/main/%s', None)
}

exclude_patterns = ['_build', 'wip']

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
