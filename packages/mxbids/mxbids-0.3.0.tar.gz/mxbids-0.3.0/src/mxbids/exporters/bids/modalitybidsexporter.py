"""modalitybidsexporter.py
A class for exporting BIDS modalities.
"""
# Package Header #
from ...header import *

# Header #
__author__ = __author__
__credits__ = __credits__
__maintainer__ = __maintainer__
__email__ = __email__


# Imports #
# Standard Libraries #

# Third-Party Packages #

# Local Packages #
from ...modalities import Modality
from ..modalityexporter import ModalityExporter


# Definitions #
# Classes #
class ModalityBIDSExporter(ModalityExporter):
    """A class for exporting BIDS modalities."""

    # Attributes #
    exporter_name: str = "BIDS"
    export_exclude_names: set[str, ...] = {"meta"}


# Assign Exporter
Modality.exporters["BIDS"] = (ModalityBIDSExporter, {})
