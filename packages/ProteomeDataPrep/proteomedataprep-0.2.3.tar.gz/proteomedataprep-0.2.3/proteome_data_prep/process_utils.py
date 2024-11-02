import re
import pandas as pd
from dataclasses import dataclass, field
import json
import os
import pkg_resources
from typing import Optional, List, Dict, Union
import numpy as np
from .data_loader import DataLoader
from .data_container import DataContainer

from .data_utils import *

pd.options.mode.chained_assignment = None
pd.set_option('future.no_silent_downcasting', True)


@dataclass
class Processor:

    dropna_percent_threshold: float = 50

    label_screens: bool = False
    screen_split: Dict[Union[tuple, str], str] = field(default_factory= 
                               # MSR numbers by which to split screens
                               lambda: {(0, 5863): "THP-1 1K",  
                               (5863, 1e16): "Anborn"})
    label_tfs: bool = True
    tf_list: Optional[List[str]] = None
    gene_info_by_acc: Optional[Dict] = None


    def __post_init__(self):
        """
        Post-initialization for class attribute validation and setup.

        This method performs checks and setup actions immediately after
        object initialization, verifying that required configurations are 
        set and initializing the transcription factor (TF) list.

        Raises:
            ValueError: If `label_screens` is True and `screen_split` is None.
                This ensures that a dictionary is provided to label screens 
                when screen labeling is enabled.
            
            Warning: If `dropna_percent_threshold` is 1 or lower, indicating
                that the threshold should be a percentage (greater than 1)
                rather than a portion. A value of 1 or less may exclude columns
                unless they are 99% or more complete.

        Sets:
            self.tf_list: Calls `load_tf_list()` to initialize the transcription
                factor list for use within the class.
        """
        if self.label_screens:
            if self.screen_split is None:
                raise ValueError("Provide a dictionary to label screens.")
            
        if self.dropna_percent_threshold <= 1.0:
            raise Warning(f"dropna_percent_threshold is a percent. " 
                          "Not a portion. Passing a value of 1 or less will " 
                          "exlude columns unless they are 99%+ not NaN.")
        
        self.tf_list = self.load_tf_list()
    
    def process_and_normalize(
            self, data_container: DataContainer,
            normalize_abundance: bool = True,
            label_tfs: bool = False,
            label_screens: bool = False,
            keep_filename: bool = False
            ) -> DataContainer:
        """
        Process and normalize data from a `DataContainer` by performing
        log transformation, optional labeling, and median normalization.

        Args:
            data_container (DataContainer): Container object holding the raw
                DataFrame (`raw_df`) to be processed and normalized.
            normalize_abundance (bool): If True, performs median normalization
                on the transformed data for abundance adjustment.
            label_tfs (bool): If True, labels transcription factors (TFs) 
                within the dataset.
            label_screens (bool): If True, labels specific screens by applying
                `_get_screen` method for grouping purposes.
            keep_filename (bool): If False, removes the "Filename" column after
                extracting compound names from filenames.

        Returns:
            DataContainer: The input `DataContainer` with its `normalized_df`
                attribute updated to include the processed and normalized data.

        Process Overview:
            1. Applies log transformation to `raw_df`.
            2. Labels TFs if `label_tfs` is True.
            3. Normalizes abundance based on the median if `normalize_abundance`
            is True.
            4. Labels screens by grouping if `label_screens` is True.
            5. Extracts compound names from filenames, adding to the "Compound"
            column, and optionally removes the "Filename" column.
        """

        log_df = self.log_transform(data_container.raw_df)

        if label_tfs:
            log_df = self.label_tfs
        
        normalized_df = self.median_normalize_df(
            log_df, 
            normalize_abundance=normalize_abundance
        )
        
        normalized_df["Compound"] = normalized_df["Filename"].apply(
            self.get_compound_name
        )

        if label_screens:
            normalized_df["screen"] = (
                normalized_df["Filename"].apply(self._get_sceen)
            )

        if not keep_filename:
            normalized_df = normalized_df.drop(columns=["Filename"])

        data_container.normalized_df = normalized_df

        return data_container

    
    def log_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Perform log transformation on quantitative columns, handling zeros
        and `None` values, and retaining identifier columns.

        This method identifies quantitative columns for transformation,
        replaces zeros and `None` values with `NaN`, applies a log transformation,
        and then recombines the results with identifier columns. Finally, it
        drops columns exceeding the NaN threshold.

        Args:
            df (pd.DataFrame): Input DataFrame with raw data, containing both
                identifier and quantitative columns.

        Returns:
            pd.DataFrame: DataFrame with log-transformed quantitative data
                and original identifier columns.

        Process Overview:
            1. Identifies quantitative columns for log transformation.
            2. Replaces 0 and `None` values with `NaN` in quantitative columns.
            3. Applies natural logarithm to quantitative columns.
            4. Retains identifier columns alongside transformed data.
            5. Drops columns exceeding the NaN threshold using `_drop_nan_cols`.
        """
        quant_cols = get_quant_columns(df)

        id_cols = detect_id_columns(df)
        
        # Replace 0 and None with np.nan across the selected columns
        df_safe = df[quant_cols].replace(
            {0: np.nan, None: np.nan}
            ).astype(float)
        log_df = np.log(df_safe)

        log_df = pd.concat([df[id_cols], log_df], axis=1)

        log_df = self._drop_nan_cols(log_df)

        return log_df

    def median_normalize_df(self, 
                            log_df: pd.DataFrame, 
                            normalize_abundance: bool=True
                            ) -> pd.DataFrame:
        """
        Median normalize a DataFrame by adjusting quantitative columns
        and optionally re-centering abundance values.

        This method performs median normalization on quantitative columns
        within `log_df`. It calculates the overall median of non-empty columns,
        subtracts the column medians to normalize data, melts the DataFrame for
        a single "Abundance" column, and optionally re-centers abundance values.

        Args:
            log_df (pd.DataFrame): DataFrame with log-transformed quantitative
                columns and identifier columns.
            normalize_abundance (bool): If True, re-centers abundance values
                by adding back the overall median.

        Returns:
            pd.DataFrame: A normalized DataFrame with "Abundance" and (if 
                `normalize_abundance` is True) "Normalized Abundance" columns.

        Process Overview:
            1. Identifies non-empty quantitative columns for normalization.
            2. Calculates the overall median for non-empty columns.
            3. Normalizes columns by subtracting their individual medians.
            4. Melts the DataFrame to provide a single "Abundance" column.
            5. Adds the overall median back to abundance values if
            `normalize_abundance` is True, creating "Normalized Abundance".
        """
        quant_cols = get_quant_columns(log_df)

        non_empty_cols = log_df[
            quant_cols].columns[log_df[quant_cols].notna().any()
        ]
        
        # Calculate the overall median for non-empty columns only
        overall_median = log_df[non_empty_cols].median().median()
        
        # Normalize by subtracting the median for each column
        log_df[non_empty_cols] = (
            log_df[non_empty_cols] - log_df[non_empty_cols].median()
        )

        # Melt to get a single abundance column, drop nans
        melted_df = self.melt_df(log_df)
        melted_df.dropna(inplace=True)

        # Add back in overall median so log abundance values are
        # more "realistic"
        if normalize_abundance:
            melted_df["Normalized Abundance"] = (
                melted_df["Abundance"] + overall_median
            )
   
        return melted_df
    
    def melt_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Reshape the DataFrame to have a single "Abundance" column and peptide
        columns as rows, facilitating analysis.

        This method melts the input DataFrame so that each peptide becomes a row,
        with identifier columns preserved, and the abundance values are stored
        in a single "Abundance" column.

        Args:
            df (pd.DataFrame): Input DataFrame with peptide columns and
                identifier columns.

        Returns:
            pd.DataFrame: A melted DataFrame with:
                - Identifier columns intact,
                - A "Filename" column indicating original column names,
                - An "Abundance" column containing the values for each peptide.
        
        Process Overview:
            1. Detects identifier columns to retain as independent columns.
            2. Melts the DataFrame, converting peptide columns to rows.
            3. Renames the resulting columns to "Filename" and "Abundance".
        """
        # Restructure df so columns are peptides
        id_vars = detect_id_columns(df)    
        melt_df = df.melt(id_vars=id_vars, # Melt so filename is col.
                        var_name="Filename",
                        value_name="Abundance")
        return melt_df


    def _drop_nan_cols(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Drop columns from the DataFrame that exceed a specified NaN percentage.

        This method calculates the percentage of missing values in each column
        and drops those that meet or exceed the `dropna_percent_threshold`.

        Args:
            df (pd.DataFrame): Input DataFrame from which columns with excessive
                NaN values will be removed.

        Returns:
            pd.DataFrame: A DataFrame with columns dropped based on the NaN
                percentage threshold.

        Process Overview:
            1. Calculates the percentage of NaN values per column.
            2. Identifies columns exceeding the `dropna_percent_threshold`.
            3. Drops these columns and returns the modified DataFrame.
        """

        # Calculate the percentage of NaN values for each column
        nan_percentage = df.isnull().sum() * 100 / len(df)
        
        # Identify columns to drop
        cols_to_drop = nan_percentage[
            nan_percentage >= self.dropna_percent_threshold
        ].index
        
        df = df.drop(columns=cols_to_drop)
        
        return df

    def load_tf_list(self) -> List[str]:
        """
        Load a list of transcription factors (TFs) from a JSON file.

        This method loads transcription factor gene names from a JSON file
        (`acc_by_tf_gene.json`) located in the `proteome_data_prep/data/` 
        directory. If the file is missing or contains invalid JSON, it raises
        an appropriate error.

        Returns:
            List[str]: A list of transcription factor gene names extracted from
                    the JSON file.

        Raises:
            FileNotFoundError: If the JSON file cannot be found at the specified
                            path.
            ValueError: If there is an error decoding JSON content from  file.
        """
        tf_path = pkg_resources.resource_filename(
            'proteome_data_prep',
            'data/acc_by_tf_gene.json'
        )
        
        try:
            with open(tf_path, 'r') as file:
                acc_by_tf_gene = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {tf_path} was not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Error decoding JSON from the file {tf_path}.")
        
        return list(acc_by_tf_gene.keys())


    @staticmethod
    def load_gene_info():
        """
        Load gene information from a JSON file.

        This static method loads gene information from a JSON file 
        (`gene_info_by_acc.json`) located in the `proteome_data_prep/data/` 
        directory. The file is expected to map accession IDs to gene 
        information, which is returned as a dictionary.

        Returns:
            dict: A dictionary containing gene information by accession ID, 
                loaded from the JSON file.

        Raises:
            FileNotFoundError: If the JSON file cannot be located at the 
                            specified path.
            json.JSONDecodeError: If the JSON content cannot be decoded 
                            properly.
            """
        gene_info_path = pkg_resources \
            .resource_filename('proteome_data_prep',
                                'data/gene_info_by_acc.json')
        with open(gene_info_path, 'r') as file:
            return json.load(file)
        
    def _is_tf(self, gene: str) -> bool:
        """
        Check if any gene in a given string is a transcription factor (TF).

        This method checks whether any of the genes in the input string are
        transcription factors by comparing them against `self.tf_list`. The 
        input gene string is expected to contain gene names separated by 
        semicolons (`;`), which are split and checked individually.

        Args:
            gene (str): A semicolon-separated string of gene names to check 
                        against the transcription factor list.

        Returns:
            bool: True if any gene in the input string is found in 
                        `self.tf_list`, otherwise False.
        """
        gene_list = gene.split(';')
        return any(gene in self.tf_list for gene in gene_list)

    def label_tfs(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Label genes in the DataFrame as transcription factors (TFs).

        This method adds a new column, "Is TF", to the input DataFrame. It
        applies the `_is_tf` method to the "Genes" column, marking each gene
        as a transcription factor (True) or not (False) based on the presence
        of genes in `self.tf_list`.

        Args:
            df (pd.DataFrame): Input DataFrame containing a "Genes" column
                            with gene names to be labeled as TFs.

        Returns:
            pd.DataFrame: The input DataFrame with an additional "Is TF" column,
                        indicating whether each gene is a transcription factor.
        """
        df["Is TF"] = df["Genes"].apply(self._is_tf)
        return df

    def get_compound_name(self, s: str) -> str:
        """
        Extract a compound name from a given string based on predefined 
        patterns.

        This method identifies and standardizes compound names within a string 
        by matching specific patterns (e.g., "TAL####", "DMSO", "PRTC"). 
        It returns a standardized compound name if a match is found or raises 
        an exception if no recognizable compound pattern is detected.

        Args:
            s (str): Input string from which to extract the compound name. This 
                    may be a filename or other identifier containing the 
                    compound name pattern.

        Returns:
            str: The standardized compound name if recognized.

        Raises:
            Exception: If no recognizable compound pattern is found in the input 
                    string, an exception is raised.
        """

        # Look for compounds with the name TAL####
        if "TAL" in s.upper():
            tal_num = re.search(r'TAL\d+(-\d+)?', s)[0]
            # Strip leading zeros if present
            num = int(re.search(r'\d+(-\d+)?', tal_num)[0])
            new_name = "TAL" + str(num)
            return new_name
        elif "DMSO" in s.upper():
            return "DMSO"
        elif "PRTC" in s.upper():
            return "PRTC"
        elif "nuclei" in s.lower():
            return "NUC"
        elif "nuc" in s.lower(): # cases where it is labeled as NUC2
            nuc_num = re.search(r'NUC\d+(-\d+)?', s)
            if nuc_num is None:
                return "NUC"
            else:
                return nuc_num[0]
        elif "dbet" in s.lower():
            return "dBET6"
        elif "FRA" in s.upper():
            return "FRA"
        elif "none" in s.lower():
            return "None"
        else:
            raise Exception(f"Unable to extract compound from filename {s}.")
    
    def _get_screen(self, msr_str):
        if msr_str.startswith("MSR"):
            try:        
                msr = re.search(r'MSR\d+(-\d+)?', msr_str)[0]
            except:
                raise ValueError(f"Unable to match MSR for filename {msr_str}.")
            
            msr = int(re.search(r'\d+(-\d+)?', msr)[0])
        
            for msr_range, screen_name in self.screen_split.items():
                if isinstance(msr_range, tuple):
                    if msr_range[0] <= msr < msr_range[1]:
                        return screen_name
            raise ValueError(f"Unable to determine screen for MSR {str(msr)}.")
        else:
            screen_name = msr_str.split("_")[0]
            try:
                screen = self.screen_split[screen_name]
            except KeyError:
                raise KeyError(f"Screen name {screen_name} not in screen_dict.")
            return screen

    @staticmethod
    def convert_encyclopedia_file(data_container: DataContainer
                                  ) -> DataContainer:
        """
        Convert an encyclopedia file format to resemble a DIANN file format.

        This method takes a `data_container` containing an encyclopedia file,
        reformats it to match the DIANN structure, and updates gene and protein
        information. Specifically, it renames columns to align with DIANN 
        format, applies gene information, and separates gene names and protein 
        IDs.

        Args:
            data_container (DataContainer): Container object holding the raw
                DataFrame (`raw_df`) with encyclopedia-formatted data.

        Returns:
            DataContainer: The updated `data_container` with:
                - Reformatted DataFrame (`raw_df`) in DIANN format,
                - "Genes" and "Protein.Ids" columns populated with extracted
                gene names and protein IDs,
                - Filetype attribute set to "diann".
        """
        gene_info_by_acc = Processor.load_gene_info()
    
        rename_dict = {"Peptide": "Precursor.Id",
                    "Protein": "Protein.Ids"}
        df = data_container.raw_df 
        df = df.rename(columns=rename_dict)

        # Apply _extract_gene_info 
        gene_info = df["Protein.Ids"].apply(
            lambda x: Processor._extract_gene_info(x, gene_info_by_acc)
        )
        
        # Split the gene_info result by the underscore
        df["Genes"] = gene_info.apply(lambda x: x.split('_')[0])  # Get the gene name
        df["Protein.Ids"] = gene_info.apply(lambda x: x.split('_')[1])  # Get the protein IDs
        
        data_container.raw_df = df
        data_container.filetype = "diann"
        return data_container
    
    @staticmethod
    def _extract_gene_info(protein_ids, gene_info_by_acc):
        """
        Extract gene and protein information from a protein ID string.

        This method processes a semicolon-separated string of protein IDs,
        retrieves gene information using a provided mapping, and returns a
        standardized string containing both gene names and cleaned protein IDs.

        Args:
            protein_ids (str): A semicolon-separated string of protein IDs, each
                            formatted as "sp|<id>|<name>".
            gene_info_by_acc (dict): A dictionary mapping base protein IDs to 
                                    gene information. Each entry maps an ID
                                    to a dictionary with an 'id' field 
                                    containing the gene name.

        Returns:
            str: A single string formatted as "GeneName_CleanProteinIDs", where
                "GeneName" is a semicolon-separated list of unique gene names,
                and "CleanProteinIDs" is a semicolon-separated list of 
                protein IDs without isoform details.

        Process Overview:
            1. Splits the input `protein_ids` string by semicolons to create
            a list of individual protein IDs.
            2. Extracts the base protein ID (without isoforms) from each 
            protein string.
            3. Uses `gene_info_by_acc` to look up the gene name for each base 
            ID. If no gene information is found, assigns 'Unknown'.
            4. Builds a set of gene names and a list of cleaned protein IDs
            (without isoform suffixes).
            5. Returns a formatted string "GeneName_CleanProteinIDs", where 
            gene names and protein IDs are each separated by semicolons.
            
        Example:
            Input:
                protein_ids = "sp|Q9Y2L5-2|TPPC8_HUMAN;sp|Q9Y2L5|TPPC8_HUMAN"
                gene_info_by_acc = {'Q9Y2L5': {'id': 'TRAPPC8'}}
            
            Output:
                "TRAPPC8_Q9Y2L5-2;Q9Y2L5"
      
            Process:
                0. sp|Q9Y2L5-2|TPPC8_HUMAN;sp|Q9Y2L5|TPPC8_HUMAN
                1. [ sp|Q9Y2L5-2|TPPC8_HUMAN, sp|Q9Y2L5|TPPC8_HUMAN ]
                2. Q9Y2L5-2
                3. Q9Y2L5
                4. {'name': 'TPPC8_HUMAN', 'id': 'TRAPPC8'}
                5. 'TRAPPC8'
                6. TRAPPC8_Q9Y2L5-2;Q9Y2L5
        """
        protein_list = protein_ids.split(';') # 1

        gene_ids = set() 
        clean_proteins = [] 
        
        for protein in protein_list:
            if '|' in protein:
                protein_id = protein.split('|')[1] # 2
            else:
                protein_id = protein
                
            base_protein_id = protein_id.split('-')[0] # 3

            gene_info = gene_info_by_acc.get(base_protein_id, {}) # 4
            gene_name = gene_info.get('id', 'Unknown') # 5
            if gene_name is None:
                gene_name = "None"

            gene_ids.add(gene_name)
            clean_proteins.append(protein_id)
        
        genes = ';'.join(sorted(gene_ids))
        return genes + "_" +';'.join(clean_proteins)  # 6
   