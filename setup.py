from setuptools import setup, find_packages

import fpga

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='pyfpga',
    version=fpga.__version__,
    description='A Python Class and helper scripts to use FPGA development tools in a vendor-independent way',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Rodrigo A. Melo',
    author_email='rodrigomelo9@gmail.com',
    license='GPLv3',
    url='https://gitlab.com/rodrigomelo9/pyfpga',
    package_data={'': ['tool/*.tcl']},
    packages=find_packages(),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
        'Topic :: Software Development :: Build Tools'
    ]
)
