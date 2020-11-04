.. program:: pyfpga

Basic usage
###########

You can read the detailed :ref:`api` and/or start with the :repo:`Examples <examples>`.
In this document, you will find a tutorial about basic and advanced uses of PyFPGA.

.. ATTENTION::

  PyFPGA assumes that the backend Tool is ready to run.
  This implies, depending on the operating system, things such as:

  * Tool installed.
  * A valid License configured.
  * Tool available in the system PATH.
  * In a GNU/Linux: extra packages installed, environment variables assigned
    and permissions granted on devices (to transfer the bitstream).

Basic usage
===========

The first steps are import and instantiate the ``Project`` *class*, specifying
the tool to use and, optionally, the project name. By default, the directory
where files are generated is called ``build`` and is located in the same place
that the script, but another name and location can be specified.

.. code-block:: python

   from fpga.project import Project

   prj = Project('vivado', 'projectName')
   prj.set_outdir('../temp')

.. NOTE::

  The supported tool names are: ``ghdl``, ``ise``, ``libero``, ``openflow``, ``quartus``,
  ``vivado``, ``yosys``, ``yosys-ise`` and ``yosys-vivado``.

Next, the FPGA part, the project files and the top-level name must be
specified. The file addition allows specifying one or more HDL, constraint or
Tcl files, using glob internally, which makes available the use of wildcards.
The path to their location must be relative to the script, and there is an
optional parameter to indicate if it is a member of a VHDL package.

.. code-block:: python

   prj.set_part('xc7k160t-3-fbg484')

   prj.add_files('hdl/blinking.vhdl', 'examples')
   prj.add_files('hdl/examples_pkg.vhdl', 'examples')
   prj.add_files('hdl/top.vhdl')

   prj.set_top('Top')

.. NOTE::

  * You can use the default FPGA part for a quick test, but generally, you
    will want to specify a particular one. Examples:

    * Ise: ``xc7k160t-3-fbg484``
    * Libero: ``mpf100t-1-fcg484``
    * Openflow: ``hx8k-ct256``
    * Quartus: ``10cl120zf780i8g``
    * Vivado: ``xc7k160t-3-fbg484``

  * For some Tools, the files order could be a problem.
    If a complain about something not found is displayed, try changing the
    order.
    If a file seems unsupported, you can always use the ``prefile`` or ``project``
    hooks (see [Advanced usage](#advanced-usage)).
  * A file with the tcl extension will be included with the ``source`` command.
    It could be used to have a file with particular additional options.
  * A relative path to a valid VHDL/Verilog file is also accepted by
    ``set_top``, to automatically extract the top-level name.
  * In case of Verilog, ``add_include`` can be used to specify where to search
    included files.

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

Advanced usage
==============

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
| Top specification        | Implementation       |
+--------------------------+----------------------+
| Parameters specification | **postimp** hook     |
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
    ``postsyn``, ``postimp`` and ``postbit``.
  * The *hook* string must be a valid command (supported by the used tool).
  * If more than one *hook* is needed in the same *phase*, you can call this
    method several times (the commands will be executed in order).

The generics/parameters of the project can be optionally changed with:

.. code-block:: python

   prj.set_param('param1', value1)
   ...
   prj.set_param('paramN', valueN)

The method ``generate`` (previously seen at the end of
[Basic usage](#basic-usage) section) has optional parameters:

.. code-block:: python

   prj.generate(to_task, from_task, capture)

With *to_task* and *from_taks* (with default values ``bit`` and ``prj``),
you are selecting the first and last task to execute when `generate` is
invoqued. The order and available tasks are ``prj``, ``syn``, ``imp`` and ``bit``.
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


Transfer to a device
====================

This method is in charge of run the needed tool to transfer a bitstream to a
device (commonly an FPGA, but memories are also supported in some cases).
It has up to five optional parameters:

.. code-block:: python

   prj.transfer(devtype, position, part, width, capture)

Where *devtype* is ``fpga`` by default but can also be ``spi``, ``bpi``, etc, if
supported. An integer number can be used to specify the *position* (1) in the
Jtag chain. When a memory is used as *devtype*, the *part* name and the
*width* in bits must be also specified. In case of *capture*, it is useful to
catch execution messages to be post-processed or saved to a file.

.. NOTE::

  * In Xilinx, `spi` and `bpi` memories are out of the Jtag chain and are
    programmed through the FPGA. You must specify the FPGA *position*.

  * In a Linux systems, you need to have permission over the device
    (udev rule, be a part of a group, etc).

Logging capabilities
====================

PyFPGA uses the `logging <https://docs.python.org/3/library/logging.html>`_
module, with a *NULL* handler and the *INFO* level by default.
Messages can be enabled with:

.. code-block:: python

   import logging

   logging.basicConfig()

You can enable *DEBUG* messages adding:

.. code-block:: python

   logging.getLogger('fpga.project').level = logging.DEBUG

