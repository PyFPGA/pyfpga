# -*- coding: utf-8 -*-

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

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
