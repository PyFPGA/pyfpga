# PyFPGA User Guide

You can read the detailed [API reference](api-reference.md) and/or start with
the [Examples](../examples). In this document, you will find a tutorial about
basic and advanced uses of PyFPGA.

* [Basic usage](#basic-usage)
* [Advanced usage](#advanced-usage)
* [Transfer to a device](#transfer-to-a-device)
* [Logging capabilities](#logging-capabilities)

> **ATTENTION:**
> PyFPGA assumes that the backend Tool is ready to run.
> This implies, depending on the operating system, things such as:
> * Tool installed.
> * A valid License configured.
> * Tool available in the system PATH.
> * In a GNU/Linux: extra packages installed, environment variables assigned
> and permissions granted on devices (to transfer the bitstream).

## Basic usage

The first steps are import and instantiate the `Project` *class*, specifying
the tool to use and, optionally, the project name. By default, the directory
where files are generated is called `build` and is located in the same place
that the script, but another name and location can be specified.

```py
from fpga.project import Project

prj = Project('vivado', 'projectName')
prj.set_outdir('../temp')
```

> The supported tool names are: `ise`, `libero`, `quartus`, `vivado`,
> `yosys`, `yosys-ise` and `yosys-vivado`.

Next, the FPGA part, the project files and the top-level name must be
specified. The file addition allows specifying one or more HDL, constraint or
Tcl files, using glob internally, which makes available the use of wildcards.
The path to their location must be relative to the script, and there is an
optional parameter to indicate if it is a member of a VHDL package.

```py
prj.set_part('xc7k160t-3-fbg484')

prj.add_files('hdl/blinking.vhdl', 'examples')
prj.add_files('hdl/examples_pkg.vhdl', 'examples')
prj.add_files('hdl/top.vhdl')

prj.set_top('Top')
```

> **Notes:**
> * You can use the default FPGA part for a quick test, but generally, you
> will want to specify a particular one. Examples:
>     * Ise: `xc7k160t-3-fbg484`
>     * Libero: `mpf100t-1-fcg484`
>     * Quartus: `10cl120zf780i8g`
>     * Vivado: `xc7k160t-3-fbg484`
> * For some Tools, the files order could be a problem.
> If a complain about something not found is displayed, try changing the
> order.
> If a file seems unsupported, you can always use the `prefile` or `postprj`
> commands (see [Advanced usage](#advanced-usage)).
> * A file with the tcl extension will be included with the `source` command.
> It could be used to have a file with particular additional options.
> * A relative path to a valid VHDL/Verilog file is also accepted by
> `set_top`, to automatically extract the top-level name.
> * In case of Verilog, `add_include` can be used to specify where to search
> included files.

Finally, you must run the bitstream generation or its transfer. Both of them
are time-consuming tasks, performed by a backend tool, which could fail.
Exceptions are raised in such cases, that should be ideally caught to avoid
abnormal program termination.

```py
try:
    prj.generate()
    prj.transfer()
except Exception as e:
    print('{} ({})'.format(type(e).__name__, e))
```

And wait for the backend Tool to accomplish its task.

## Advanced usage

The following picture depicts the parts of the Project Creation and the Design
Flow internally performed by PyFPGA.

![Tcl Structure](images/tcl-structure.png)

If the provided API if not enough or suitable for your project, you can
specify additional *commands* in different parts of the flow, using:

```py
prj.add_prefile_cmd('A text string')  # for *Pre-file commands*.
prj.add_postprj_cmd('A text string')  # for *Post-prj commands*.
prj.add_preflow_cmd('A text string')  # for *Pre-flow commands*.
prj.add_postsyn_cmd('A text string')  # for *Post-syn commands*.
prj.add_postimp_cmd('A text string')  # for *Post-imp commands*.
prj.add_postbit_cmd('A text string')  # for *Post-bit commands*.
```

> **Notes:**
> * The text string must be a valid command supported by the used backend.
> * If more than one command is needed, you can call these methods several
> times (will be executed in order).

The generics/parameters of the project can be optinally changed with:

```py
prj.set_param('param1', value1)
...
prj.set_param('paramN', valueN)
```

The method `generate` (previously seen at the end of
[Basic usage](#basic-usage) section) has optional parameters:

```py
prj.generate(strategy, to_task, from_task, capture)
```

The initial value of *strategy* is `default`, but you can apply some
optimizations using `area`, `power` or `speed`. At this point you are
selecting if apply or not certain commands.

In case of *to_task* and *from_taks* (with default values `bit` and `prj`),
you are selecting the first and last task to execute when `generate` is
invoqued. The order and available tasks are `prj`, `syn`, `imp` and `bit`.
It can be useful in at least two cases:
* Maybe you created a file project with the GUI of the Tool and only want to
run the Design Flow, so you can use: `generate(to_task='bit', from_task='syn')`
* Methods to insert particular commands are provided, but you would want to
perform some processing from Python between tasks, using something like:
```py
prj.generate(to_task='syn', from_task='prj')
#Some other Python commands here
prj.generate(to_task='bit', from_task='syn')
```

In case of *capture*, it is useful to catch execution messages to be
post-processed or saved to a file:
```py
result = prj.generate(capture=True)
print(result)
```

## Transfer to a device

This method is in charge of run the needed tool to transfer a bitstream to a
device (commonly an FPGA, but memories are also supported in some cases).
It has up to five optional parameters:

```py
prj.transfer(devtype, position, part, width, capture)
```

Where *devtype* is `fpga` by default but can also be `spi`, `bpi`, etc, if
supported. An integer number can be used to specify the *position* (1) in the
Jtag chain. When a memory is used as *devtype*, the *part* name and the
*width* in bits must be also specified. In case of *capture*, it is useful to
catch execution messages to be post-processed or saved to a file.

> **Notes:**
> * In Xilinx, `spi` and `bpi` memories are out of the Jtag chain and are
programmed through the FPGA. You must specify the FPGA *position*.
> * In a Linux systems, you need to have permission over the device
> (udev rule, be a part of a group, etc).

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
