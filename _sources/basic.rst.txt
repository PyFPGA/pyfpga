Basic usage
===========

.. ATTENTION::

  (2024-08-08) To be updated.

Project Creation
----------------

The first steps are import the module and instantiate the ``Project`` *class*,
specifying the *TOOL* to use and, optionally, a *PROJECT NAME* (the *tool*
name is used when *no name* is provided).

.. code-block:: python

   from fpga.project import Project

   prj = Project('vivado', 'projectName')

By default, the directory where the project is generated is called ``build``
and is located in the same place that the script, but another name and location
can be specified.

.. code-block:: python

   prj.set_outdir('../temp')

Next, the FPGA part would be specified:

.. code-block:: python

   prj.set_part('xc7k160t-3-fbg484')

.. NOTE::

  You can use the default FPGA part for a quick test or make a lazy comparison
  between tools, but generally, you will want to specify a particular one.
  Examples about how to specify a part according the tool, are (default values
  when ``set_part`` is not employed):

    * **Ise:** ``xc7k160t-3-fbg484`` (*device-speed-package*)
    * **Libero:** ``mpf100t-1-fcg484`` (*device-speed-package*)
    * **Openflow:** ``hx8k-ct256`` (*device-package*)
    * **Quartus:** ``10cl120zf780i8g`` (*part*)
    * **Vivado:** ``xc7k160t-3-fbg484`` (*part*)

The files addition method allows specifying one or more HDL or constraint files
(also block designs in case of Vivado).
It uses ``glob`` internally, which makes available the use of wildcards.
The path to their location must be relative to the Python script, and there
are optional parameters to indicate the file type (``vhdl``, ``verilog``,
``constraint`` or ``design``), which is automatically detected based on the
file extension, and if it is a member of a VHDL package.

.. code-block:: python

   prj.add_files('hdl/blinking.vhdl', library='examples')
   prj.add_files('hdl/examples_pkg.vhdl', library='examples')
   prj.add_files('hdl/top.vhdl')

.. NOTE::

  * In some cases, the files order could be a problem, so take into account to
    change the order if needed.
  * If a file seems unsupported, you can always use the ``prefile`` or
    ``project`` :ref:`hooks`.
  * In case of Verilog, ``add_vlog_include`` can be used to specify where to
    search for included files.

Finally, the top-level must be specified:

.. code-block:: python

   prj.set_top('Top')

.. NOTE::

  A relative path to a valid VHDL/Verilog file is also accepted by ``set_top``,
  to automatically extract the top-level name.

Project generation
------------------

Next step if to generate the project. In the most basic form, you can run the
following to get a bitstream:

.. code-block:: python

   prj.generate()

Additionally, you can specify which task to perform:

.. code-block:: python

   prj.generate('syn')

.. NOTE::

  The valid values are:

  * ``prj``: to generate only a project file (only supported for privative tools)
  * ``syn``: to performs synthesis.
  * ``imp``: to performs synthesis and implementation (place and route,
    optimizations and static timming analysis when available).
  * ``bit``: (default) to perform synthesis, implementation and bitstream generation.

Bitstream transfer
------------------

This method is in charge of run the needed tool to transfer a bitstream to a
device (commonly an FPGA, but memories are also supported in some cases).
It has up to four main optional parameters:

.. code-block:: python

   prj.transfer(devtype, position, part, width)

Where *devtype* is ``fpga`` by default but can also be ``spi``, ``bpi``, etc, if
supported. An integer number can be used to specify the *position* (1) in the
Jtag chain. When a memory is used as *devtype*, the *part* name and the
*width* in bits must be also specified.

.. NOTE::

  * In Xilinx, `spi` and `bpi` memories are out of the Jtag chain and are
    programmed through the FPGA. You must specify the FPGA *position*.
  * In a Linux systems, you need to have permission over the device
    (udev rule, be a part of a group, etc).

Logging capabilities
--------------------

PyFPGA uses the `logging <https://docs.python.org/3/library/logging.html>`_
module, with a *NULL* handler and the *INFO* level by default.
Messages can be enabled with:

.. code-block:: python

   import logging

   logging.basicConfig()

You can enable *DEBUG* messages adding:

.. code-block:: python

   logging.getLogger('fpga.project').level = logging.DEBUG
