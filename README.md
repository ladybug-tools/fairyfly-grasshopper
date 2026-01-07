[![Build Status](https://github.com/ladybug-tools/fairyfly-grasshopper/workflows/CI/badge.svg)](https://github.com/ladybug-tools/fairyfly-grasshopper/actions)

[![IronPython](https://img.shields.io/badge/ironpython-2.7-red.svg)](https://github.com/IronLanguages/ironpython2/releases/tag/ipy-2.7.8/)

# fairyfly-grasshopper

:ant: :green_book: fairyfly plugin for Grasshopper.

This repository contains all Grasshopper components for the fairyfly plugin.
The package includes both the user objects (`.ghuser`) and the Python source (`.py`).
The repository also contains a JSON version of the grasshopper component data.

Note that this library only possesses the Grasshopper components and, in order to
run the plugin, the core libraries must be installed in a way that they can be
discovered by Rhino (see dependencies).

## Dependencies

The fairyfly-grasshopper plugin has the following dependencies (other than Rhino/Grasshopper):

* [ladybug-geometry](https://github.com/ladybug-tools/ladybug-geometry)
* [ladybug-core](https://github.com/ladybug-tools/ladybug)
* [ladybug-rhino](https://github.com/ladybug-tools/ladybug-rhino)
* [fairyfly-core](https://github.com/ladybug-tools/fairyfly-core)
* [fairyfly-therm](https://github.com/ladybug-tools/fairyfly-therm)

## Installation

See the [Wiki of the lbt-grasshopper repository](https://github.com/ladybug-tools/lbt-grasshopper/wiki)
for the installation instructions for the entire Ladybug Tools Grasshopper plugin
(including this repository).
