# PyFPGA User Guide

You can read the detailed [API reference](api-reference.md) and/or start with
the [Examples](../examples). In this document, you will find a tutorial about
basic and advanced uses of PyFPGA.

* [System Setup](#system-setup)
* [Basic usage](#basic-usage)
* [Advanced usage](#advanced-usage)
* [Transfer to a device](#transfer-to-a-device)
* [Logging capabilities](#logging-capabilities)

## System setup

## Basic usage

First step is to import and instantiate the `Project` *class*:

```py
from fpga.project import Project

prj = Project('vivado', 'ProjectName')
```

Where the first parameter is one of the supported Tools (`ise`, `libero`,
`quartus`, `vivado`) and the second one is the name of the project.

The default output directory, where files will be generated, is created in the
same directory that the running script and is called `build`.
You can optionally change it with:

```py
prj.set_outdir('NewOutputDir')
```

You can use the default FPGA part for a quick test, but generally, you will
want to specify a particular one:

```py
prj.set_part('FPGApart')
```

> Examples:
> * Ise: `xc7k160t-3-fbg484`
> * Libero: `mpf100t-1-fcg484`
> * Quartus: `10cl120zf780i8g`
> * Vivado: `xc7k160t-3-fbg484`

Next step is to specify the project files (HDL and Constraints) and the
top-level name.

```py
# First, we recommend Verilog Header Files (if used)
prj.add_files('headers/project.vh')
# Then HDL Components/Modules
prj.add_files('vhdl/*.vhdl', 'OptionalLibraryName')
prj.add_files('verilog/*.v')
# And finally constraints
prj.add_files('project.sdc')
...
prj.set_top('TopName')
```

> NOTE:
> * For some Tools, the order could be a problem. If a complain about
> something not Found is displayed, try to change the order.
> * For some Tools, the file extension could be a problem. If a file
> seems unsupported, you can always use project options
> (see [Advanced usage](#advanced-usage)).

Finally, you must run the files generation:

```py
prj.generate()
```

And wait for the backend Tool to accomplish its task.

See [basic.py](../examples/basic.py) for the full code of a basic example.

## Advanced usage

![Tcl Structure](images/tcl-structure.png)

TODO:
```py
prj.add_project_opt('# PROJECT OPTIONS 1')
prj.add_project_opt('# PROJECT OPTIONS 2')
prj.add_preflow_opt('# PRE FLOW OPTIONS')
prj.add_postsyn_opt('# POST SYN OPTIONS')
prj.add_postimp_opt('# POST IMP OPTIONS')
prj.add_postbit_opt('# POST BIT OPTIONS')
```

TODO: explain `generate` options and exception.

See [advanced.py](../examples/advanced.py) for the full code of an advanced
example.

## Transfer to a device

TODO: explain `transfer`.

## Logging capabilities

PyFPGA uses the [logging](https://docs.python.org/3/library/logging.html)
module, with a *NULL* handler and the *INFO* level by default.
Messages can be enabled with:

```py
import logging

logging.basicConfig()
```

You can enable *DEBUG* messages adding:

```py
logging.getLogger('fpga.project').level = logging.DEBUG
```
