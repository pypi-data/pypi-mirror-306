import pandas as pd
from dataclasses import dataclass, field
import os
import pkg_resources
from typing import Optional, List

pd.options.mode.chained_assignment = None


# Read in list of high abundance batches to ignore
bad_batch_path = pkg_resources.resource_filename('proteome_data_prep', 
                                                 'data/bad_batches.txt')

with open(bad_batch_path, 'r') as file:
    bad_batches = file.read()
bad_batches = bad_batches.strip()
bad_batches = set(bad_batches.split("\n"))

@dataclass
class DataContainer:
    path: str

    # To be computed
    filetype: Optional[str] = field(default=None)  # diann or encyclopedia
    datatype: Optional[str] = field(default=None)  # protein or peptide
    raw_df: Optional[pd.DataFrame] = field(default=None)
    batches: Optional[List] = field(default=None)
    normalized_df: Optional[pd.DataFrame] = field(default=None)
    z_scores: Optional[pd.DataFrame] = field(default=None)
    # all_data: Optional[pd.DataFrame] = field(default=None)
    # # only for peptide data:
    # melted_z_scores: Optional[pd.DataFrame] = field(default=None)
    
    def __post_init__(self):
        """Initialize the DataContainer by detecting file type and data type."""
        self._detect_filetype()
        self._detect_datatype()

    def _detect_filetype(self):
        """Detect the file type based on the file path."""
        if self.filetype is None:
            self.filetype = "encyclopedia" if "encyclopedia" in self.path \
                else "diann"
            
    def _detect_datatype(self):
        """Detect the data type based on the file path."""
        if self.datatype is None:
            if "pr_matrix" in self.path or "peptides" in self.path:
                self.datatype = "peptide"
            elif "pg_matrix" in self.path or "proteins" in self.path:
                self.datatype = "protein"
            else:
                raise ValueError("Unable to determine data type from path.")
