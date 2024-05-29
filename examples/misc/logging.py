"""
This script demonstrates how to utilize the logging functionality within the
pyfpga package. The following steps are covered:

1. Creating an instance of the Project class.
2. Testing logging with the default INFO level.
3. Setting the logging level to DEBUG to capture more detailed information.
4. Disabling logging by removing all handlers.

Usage:
- By default, the logger captures messages with level INFO and higher.
- To see more detailed debug information, set the logger level to DEBUG.
- To disable logging, remove all handlers from the logger.
"""

import logging

from pyfpga.project import Project

prj = Project()
prj._test_logging()
prj.logger.setLevel(logging.DEBUG)
prj._test_logging()
prj.logger.handlers = []
prj._test_logging()
