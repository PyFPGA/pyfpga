#
# Generates a Markdown document from a python module.
#
# Based on a blog post by Christian Medina:
# How to write your own Python documentation generator
#

import os
import pydoc
from pydoc import inspect
import sys

mheader = '# Module {} documentation\n'
cheader = '## Class {}\n'
fheader = '### `{}{}`\n'


def get_markdown(module):
    output = [mheader.format(module.__name__)]
    if inspect.getdoc(module):
        output.append('{}\n'.format(inspect.getdoc(module)))
    output.extend(get_classes(module))
    return "\n".join(output)


def get_classes(module):
    output = list()
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if name.startswith('_') or obj.__module__ != module.__name__:
            continue
        output.append(cheader.format(name))
        output.append('{}\n'.format(inspect.getdoc(obj)))
        output.extend(get_functions(obj))
    return output


def get_functions(module):
    output = list()
    for name, obj in inspect.getmembers(module, inspect.isroutine):
        if name.startswith('_') and name != '__init__':
            continue
        output.append(fheader.format(
            name, inspect.formatargspec(*inspect.getargspec(obj))
        ))
        if inspect.getdoc(obj):
            output.append('{}\n'.format(inspect.getdoc(obj)))
    return output


def generatedocs(module):
    try:
        sys.path.append(os.getcwd())
        mod = pydoc.safeimport(module)
        if not mod:
            sys.exit('Module not found')
        return get_markdown(mod)
    except pydoc.ErrorDuringImport as e:
        sys.exit('Error while trying to import {}'.format(module))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(generatedocs(sys.argv[1]))
    else:
        sys.exit('Module not specified')
