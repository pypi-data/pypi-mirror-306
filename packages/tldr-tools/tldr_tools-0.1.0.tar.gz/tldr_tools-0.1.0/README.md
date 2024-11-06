## What is it?

A toolkit to interface the [https://tldr.docking.org/](https://tldr.docking.org/) webserver, a webserver home to a collection of docking optimization and benchmark molecular docking programs.

  * [BSD license](https://github.com/rdkit/rdkit/blob/master/license.txt) - a business friendly license for open source
  * Core data structures and algorithms in C++
  * [Python 3.x wrapper](https://www.rdkit.org/docs/GettingStartedInPython.html) generated using Boost.Python
  * Java and C# wrappers generated with SWIG
  * JavaScript (generated with emscripten) and CFFI wrappers around important functionality
  * 2D and 3D molecular operations
  * [Descriptor](https://www.rdkit.org/docs/GettingStartedInPython.html#list-of-available-descriptors) and [Fingerprint](http://www.rdkit.org/docs/GettingStartedInPython.html#list-of-available-fingerprints) generation for machine learning
  * Molecular database [cartridge](https://www.rdkit.org/docs/Cartridge.html) for PostgreSQL supporting substructure and similarity searches as well as many descriptor calculators
  * Cheminformatics nodes for [KNIME](https://www.knime.com/rdkit)
  * [Contrib](https://github.com/rdkit/rdkit/tree/master/Contrib) folder with useful community-contributed software harnessing the power of the RDKit

## Installation

Installation is super easy and pip installable. Pleaes make sure you have Python 3.6 installed.

```shell-session
$ pip install tldr-tools
```


## Usage
To view the current implemented modules in tldr-tools, please run:

```shell-session
$ tldr-submit --list-modules
```

For example, if running decoy generation is desired:

```shell-session
tldr-submit --module decoys --activesism input_files/actives.ism --decoygenin input_files/decoy_generation.in --memo "Decoy generation for ADA, replicate 1"
```

Documenting runs with the optional memo parameter is encouraged.

Pass in a job number to check on a status of a run:
```shell-session
tldr-status --job-number 14886
```

Once a run is successful, you can download the output to a local directory:

```shell-session
tldr-download --job-number 14886 --output some_folder
```

## Extending tldr-tools

Community and expansion is encouraged and made easy with this codebase. Adding new modules that are newly introduced on https://tldr.docking.org/ is painless, and is as simple as adding a new Endpoint and required/optional list of files.