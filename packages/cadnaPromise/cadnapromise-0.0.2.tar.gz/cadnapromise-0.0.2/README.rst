cadnaPromise
==============


.. image:: https://github.com/PEQUAN/cadnaPromise/actions/workflows/main.yml/badge.svg
    :target: https://github.com/PEQUAN/cadnaPromise/actions/workflows/main.yml
    :alt: Build


.. image:: https://img.shields.io/pypi/v/cadnaPromise?color=pink
    :target: setup.py
    :alt: Publish



.. image:: https://img.shields.io/badge/License-GPLv3-yellowgreen.svg
    :target: LICENSE
    :alt: License


Software for precision auto-tuning of floating-point variables in program.

--------
Install
--------

To install ``cadnaPromise``, simply use the pip command:  

.. parsed-literal::

  pip install cadnaPromise


Then to activate the ``cadnaPromise``, use 

.. parsed-literal::

  activate-cadna





-------------
Dependencies
-------------

The installation of ``cadnaPromise`` requires the the following Python libraries: `colorlog`, `colorama`, `docopt`, `pyyaml`, `regex`.

The compiling of ``cadnaPromise`` requires ``g++``. Please ensure the installation of above libraries for a proper running of cadnaPromise.


-------------
Usage
-------------


.. parsed-literal::

	promise -h | --help
	promise (hsd|hs|sd) [options]


Options:

.. parsed-literal::

  -h --help                     Show this screen.
  --conf CONF_FILE              get the configuration file [default: promise.yml]
  --output OUTPUT               set the path of the output (where the result files are put)
  --verbosity VERBOSITY         set the verbosity (betwen 0  and 4 for very low level debug) [default: 1]
  --log LOGFILE                 set the log file (no log file if this is not defined)
  --verbosityLog VERBOSITY      set the verbosity of the log file
  --debug                       put intermediate files into `debug/` (and `compileErrors/` for compilation errrors) and display the execution trace when an error comes
  --run RUN                     file to be run
  --compile COMMAND             command to compile the code
  --files FILES                 list of files to be examined by Promise (by default, all the .cc files)
  --nbDigits DIGITS             general required number of digits
  --path PATH                   set the path of the project (by default, the current path)
  --pause                       do pause between steps
  --noParsing                   do not parse the C file (__PROMISE__ are replaced and that's all)
  --alias ALIAS                 allow aliases (examples "g++=g++-14") [default:""]
  hsd                           Half/Single/Double mixed-precision
  hs                            Half/Single mixed-precision
  sd                            Single/Double mixed-precision


-----------------
Acknowledgements
-----------------

This PROMISE version has been developed with the financial support of the COMET project Model-Based Condition Monitoring and Process Control Systems, hosted by the Materials Center Leoben Forschung GmbH.
This PROMISE version is a full rewriting of the first PROMISE version, written by Romain Picot et al.
