# -*- coding: utf-8 -*-

import sys, re
from pathlib import Path
#from json import dump, loads

sys.path.insert(0, str(Path('.').resolve()))

# -- General configuration ------------------------------------------------

needs_sphinx = '3.0'

extensions = [
    #'recommonmark',
    'sphinx.ext.autodoc',
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.graphviz',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
]

autodoc_default_options = {
    "members": True,
    'undoc-members': True,
    #'private-members': True,
    'inherited-members': True,
}

templates_path = ['_templates']

source_suffix = {
    '.rst': 'restructuredtext',
    # '.txt': 'markdown',
    #'.md': 'markdown',
}

master_doc = 'index'

roject = u'PyFPGA'
copyright = u'2019-2021, Rodrigo Alejandro Melo and contributors'
author = u'Rodrigo Alejandro Melo and contributors'

version = "latest"
release = version  # The full version, including alpha/beta/rc tags.

language = None

exclude_patterns = []

todo_include_todos = True
todo_link_only = True

# -- Options for HTML output ----------------------------------------------

html_logo = "images/logo.png"

html_theme_options = {
    'logo_only': True,
    'home_breadcrumbs': False,
    'vcs_pageview_mode': 'blob',
}

html_context = {
    'gitlab_user': 'rodrigomelo9',
    'gitlab_repo': 'pyfpga',
    'gitlab_version': 'master',
    'conf_py_path': '/doc/',
    'display_gitlab': True
}
#ctx = Path(__file__).resolve().parent / 'context.json'
#if ctx.is_file():
#    html_context.update(loads(ctx.open('r').read()))

html_theme_path = ["."]
html_theme = "_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
#html_static_path = ['_static']

# Output file base name for HTML help builder.
htmlhelp_basename = 'PyFPGAdoc'

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    'papersize': 'a4paper',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'PyFPGA.tex', u'PyFPGA Documentation', author, 'manual'),
]

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'PyFPGA', u'PyFPGA Documentation', [author], 1)
]

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author, dir menu entry, description, category)
texinfo_documents = [
  (master_doc, 'PyFPGA', u'PyFPGA Documentation', author, 'PyFPGA', 'Python Class for vendor-independent FPGA development', 'Miscellaneous'),
]

# -- Sphinx.Ext.InterSphinx -----------------------------------------------

#intersphinx_mapping = {
#   'python': ('https://docs.python.org/3.8/', None),
#   'ghdl': ('https://ghdl.github.io/ghdl', None),
#   'vunit': ('https://vunit.github.io', None),
#   'matplotlib': ('https://matplotlib.org/', None)
#}

# -- Sphinx.Ext.ExtLinks --------------------------------------------------
extlinks = {
   'wikipedia': ('https://en.wikipedia.org/wiki/%s', None),
   'repo': ('https://github.com/PyFPGA/pyfpga/blob/main/%s', None)
}
