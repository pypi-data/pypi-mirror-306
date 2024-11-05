"""Subpackage for outputting vetting results.

Modules
-------
base
    Base classes for creating output, and abstract base classes for writing to
    files or other output channels.
excel
    Classes that implement writing to and formatting output for Excel files.
timeseries
    Classes for output from timeseries comparisons.

Subpackages
-----------
styling
    Modules and classes for styling output.
"""

from .timeseries import TimeseriesRefTargetOutput
