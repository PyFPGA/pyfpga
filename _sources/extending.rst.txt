Extending
=========

1. Add support for the new tool:

.. code-block:: python

   pyfpga/templates/<NEWTOOL>.jinja
   pyfpga/templates/<NEWTOOL>-prog.jinja
   pyfpga/<NEWTOOL>.py

2. Include the new tool on Factory:

.. code-block:: python

   pyfpga/factory.py

3. Add tests and a tool mock-up:

.. code-block:: python

   tests/test_tools.py
   tests/mocks/<NEWTOOL_EXECUTABLE>

4. Updated the project's documentation:

.. code-block:: python

   README.md
   docs

5. [OPTIONAL] Add examples:

.. code-block:: python

   examples/sources/cons/<NEWBOARD>/timing.<EXT>
   examples/sources/cons/<NEWBOARD>/clk.<EXT>
   examples/sources/cons/<NEWBOARD>/led.<EXT>
   examples/projects/<NEWTOOL>.py
   examples/hooks/<NEWTOOL>.py
