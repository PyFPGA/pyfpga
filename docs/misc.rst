Miscellaneous
=============

History
-------

The origins of this project trace back to 2015, when an in-house, never-released script called **fpga_tools**, written in *Perl*, was used to populate templates for the Xilinx ISE tool.

In 2016, the project was renamed **fpga_helpers**, transitioning from *Perl* to *Python*.
It was published as open-source on GitHub, adding support for Xilinx Vivado and Altera Quartus, and later for Microsemi (now Microchip) Libero-SoC.
It evolved into a Makefile-based system with two Tcl scripts - one for synthesis and another for programming - both designed to support multiple vendors, along with a few automation scripts.

By the end of 2019, **PyFPGA** emerged as a complete rewrite, replacing the Makefile and Tcl scripts with a Python-based workflow system.
The project was launched on GitLab, with its first official release (0.1.0) on February 29, 2020 - just before the onset of the COVID-19 pandemic.

Throughout 2020, support for open-source tools was gradually introduced.
Initially, Yosys was integrated as the synthesizer, while ISE/Vivado handled place-and-route and bitstream generation.
Later, support for VHDL via *ghdl-yosys-plugin* was added, followed by the introduction of OpenFlow - a fully solved with FLOSS tools workflow - at the end of the year.
Additionally, command-line utilities were introduced to simplify working with small projects and simple and quick proof-of-concepts.

In 2021, PyFPGA was migrated from GitLab to GitHub, aligning with the broader FPGA-related FLOSS ecosystem.
That year, the codebase was significantly expanded and improved, but it also became more complex to maintain.
This led to the release of version 0.2.0 on May 15, 2022, marking a new starting point.

Between 2023 and 2024, the project underwent a major rewrite, incorporating substantial improvements.
In 2024, support for a new vendor tool, Diamond, was contributed.
As a result, a new release is taking place in March 2025.
