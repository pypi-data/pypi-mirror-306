"""
CadOrchestrator is a new Python framework for creating consistent production files,
assembly documentation, and assemly images for modular hardware projects.

Once your project is configured in CadOrchestrator you will be able to generate documentation
and production files for a specific configuration from your terminal or to launch a webapp
with an interactive interface for congifuration.

CadOrchestrator used a number of other tools such as [GitBuilding](https://gitbuilding.io)
for documentation, and [ExSource](https://gitlab.com/gitbuilding/exsource-tools) for running
CAD file generation. It supports CAD files generated in OpenSCAD, CadQuery and FreeCAD.

Currently the framework is in an experimental stage. If your CAD models do not build please
open an issue either in this project or in
[ExSource Tools](https://gitlab.com/gitbuilding/exsource-tools).


## Installation

To install you will need Python 3.10 or newer, as well as pip. From your terminal run:

    pip install cadorchestrator


## Getting started

To get started we recommend cloning a copy of
[our example project](https://gitlab.com/gitbuilding/CadOrchestrator-Example).

There are three main files to consider when doing so.

* `cadorchestration.yaml` - This is your main configuration file. It points to
the Python module you will use for configuration, and points to the file that sets
your configuration options. For more detail see `cadorchestrator.settings`
* `OrchestratorConfigOptions.json` - This holds the configuration options that will
be displayed in the web interface, and will be passed through to your configuration
function. We are still working on standardising this data and creating a schema.
You can rename this file if you modify `cadorchestration.yaml`.
* `configure.py` - This holds the configuration function. A configuration is passed
to this function as a Python dictionary, a `cadorchestrator.components.Assembly`
object is returned. You can rename this file if you modify the
`configuration-function -> module` option in `cadorchestration.yaml`

For more information on writing your assembly code see `cadorchestrator.components`.

"""
