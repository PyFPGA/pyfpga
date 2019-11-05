# PyFPGA User Guide

## Logging

PyFPGA internally uses the [logging](https://docs.python.org/3/library/logging.html) module,
with a NULL handler and the INFO level by default.

You can enable messages with:

```
import logging

logging.basicConfig()
```

You can enable the DEBUG messages adding:

```
logging.getLogger('fpga.project').level = logging.DEBUG
```

Instead, you can suppress all the messages with:

```
logging.getLogger('fpga.project').level = 100
```
