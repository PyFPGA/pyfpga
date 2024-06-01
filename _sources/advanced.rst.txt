Advanced usage
==============

.. ATTENTION::

  (2024-05-31) To be updated.

Multi project managment
-----------------------

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

.. _hooks:

Hooks
-----

The following table depicts the parts of the *Project Creation* and the
*Design Flow* internally performed by PyFPGA.

+--------------------------+----------------------+
| Project Creation         | Design Flow          |
+==========================+======================+
| Part specification       | **preflow** hook     |
+--------------------------+----------------------+
| **prefile** hook         | Synthesis            |
+--------------------------+----------------------+
| Files addition           | **postsyn** hook     |
+--------------------------+----------------------+
| Top specification        | Place and Route      |
+--------------------------+----------------------+
| Parameters specification | **postpar** hook     |
+--------------------------+----------------------+
| **project** hook         | Bitstream generation |
+--------------------------+----------------------+
|                          | **postbit** hook     |
+--------------------------+----------------------+

If the provided API if not enough or suitable for your project, you can
specify additional *hooks* in different parts of the flow, using:

.. code-block:: python

   prj.add_hook(hook, phase)

.. NOTE::

  * Valid vaues for *phase* are ``prefile``, ``project`` (default), ``preflow``,
    ``postsyn``, ``postpar`` and ``postbit``.
  * The *hook* string must be a valid command (supported by the used tool).
  * If more than one *hook* is needed in the same *phase*, you can call this
    method several times (the commands will be executed in order).

Parameters
----------

The generics/parameters of the project can be optionally changed with:

.. code-block:: python

   prj.add_param('param1', value1)
   ...
   prj.add_param('paramN', valueN)

Generate options
----------------

The method ``generate`` (previously seen at the end of
[Basic usage](#basic-usage) section) has optional parameters:

.. code-block:: python

   prj.generate(to_task, from_task, capture)

With *to_task* and *from_taks* (with default values ``bit`` and ``prj``),
you are selecting the first and last task to execute when `generate` is
invoqued. The order and available tasks are ``prj``, ``syn``, ``par`` and ``bit``.
It can be useful in at least two cases:

* Maybe you created a file project with the GUI of the Tool and only want to
  run the Design Flow, so you can use: ``generate(to_task='bit', from_task='syn')``

* Despite that a method to insert particular commands is provided, you would
  want to perform some processing from Python between tasks, using something
  like:

.. code-block:: python

   prj.generate(to_task='syn', from_task='prj')
   #Some other Python commands here
   prj.generate(to_task='bit', from_task='syn')

In case of *capture*, it is useful to catch execution messages to be
post-processed or saved to a file:

.. code-block:: python

   result = prj.generate(capture=True)
   print(result)

In case of *capture*, it is useful to catch execution messages to be
post-processed or saved to a file.

Exceptions
----------

Finally, you must run the bitstream generation or its transfer. Both of them
are time-consuming tasks, performed by a backend tool, which could fail.
Exceptions are raised in such cases, that should be ideally caught to avoid
abnormal program termination.

.. code-block:: python

   try:
       prj.generate()
       prj.transfer()
   except Exception as e:
       print('{} ({})'.format(type(e).__name__, e))

And wait for the backend Tool to accomplish its task.
