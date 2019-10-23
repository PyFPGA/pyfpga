from setuptools import setup, find_packages

import fpga

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='pyfpga',
    version=fpga.__version__,
    description='A Python binding for the FPGA development tools',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Rodrigo A. Melo',
    author_email='rodrigomelo9@gmail.com',
    license='GPLv3',
    url='https://gitlab.com/rodrigomelo9/pyfpga',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'fpga-temp = fpga.temp:main',
            'fpga-synt = fpga.synt:main',
            'fpga-prog = fpga.prog:main'
        ],
    },
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
