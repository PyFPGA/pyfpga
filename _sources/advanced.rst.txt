Advanced usage
==============

PyFPGA offers advanced features for more customized and flexible control over FPGA project management.
This section covers two key advanced features:

1. **Hooks**: These are points in the code where you can insert custom code to extend or modify the behavior of the tool.
Hooks provide a way to integrate additional functionality or perform specific actions at predefined stages of the project lifecycle.

2. **Options**: This feature allows you to specify additional options to fine-tune the tool's behavior.
Options provide greater control over the tool's operation and enable you to customize the processing according to your specific requirements.

Hooks
-----

Hooks allow you to insert custom code at specific stages of the project lifecycle. The available hooks are:

+---------+---------------------------------------------------------------------------------------------+
| Stage   | Description                                                                                 |
+=========+=============================================================================================+
| precfg  | Code inserted after project creation and before files inclusion (e.g., specify HDL version) |
+---------+---------------------------------------------------------------------------------------------+
| postcfg | Code inserted after files inclusion (e.g., additional project configurations)               |
+---------+---------------------------------------------------------------------------------------------+
| presyn  | Code inserted before synthesis (e.g., synthesis-specific options)                           |
+---------+---------------------------------------------------------------------------------------------+
| postsyn | Code inserted after synthesis (e.g., report generation)                                     |
+---------+---------------------------------------------------------------------------------------------+
| prepar  | Code inserted before place and route (e.g., place-and-route-specific options)               |
+---------+---------------------------------------------------------------------------------------------+
| postpar | Code inserted after place and route (e.g., report generation)                               |
+---------+---------------------------------------------------------------------------------------------+
| prebit  | Code inserted before bitstream generation (e.g., bitstream-specific options)                |
+---------+---------------------------------------------------------------------------------------------+
| postbit | Code inserted after bitstream generation (e.g., report generation)                          |
+---------+---------------------------------------------------------------------------------------------+

You can specify hooks for a specific stage either line-by-line:

.. code-block:: python

   prj.add_hook('presyn', 'COMMAND1')
   prj.add_hook('presyn', 'COMMAND2')
   prj.add_hook('presyn', 'COMMAND3')

Or in a multi-line format:

.. code-block:: python

   prj.add_hook('presyn', """
   COMMAND1
   COMMAND2
   COMMAND3
   """)

Options
-------

.. ATTENTION::

   WIP feature.
