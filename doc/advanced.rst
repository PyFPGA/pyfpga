.. program:: pyfpga

Advanced usage
##############

Multi project managment
=======================

.. code-block:: python

   PROJECTS = {
       '<NAME1>': Project(
           '<TOOLNAME>',
           '<PROJECTNAME>',
           {
               'outdir': '<DIRNAME>',
               'part': '<PARTNAME>'
               'paths': [
                   '<PATHNAME1>',
                   ...
                   '<PATHNAMEn>'
               ],
               'vhdl': [
                   ['<FILENAME1>', '<LIBRARYNAME1>'],
                   '<FILENAME2>',
                   ...
                   '<FILENAMEn>'
               ],
               'verilog': [
                   '<FILENAME1>',
                   ...
                   '<FILENAMEn>'
               ],
               'constraint': [
                   '<FILENAME1>',
                   ...
                   '<FILENAMEn>'
               ],
               'params': {
                   '<PARAMNAME1>': '<VALUE1>',
                   ...
                   '<PARAMNAMEn>': '<VALUEn>'
               },
               'top': '<TOPNAME>'
           }
       )
       '<NAME2>': Project(
           ...
       )
   }
