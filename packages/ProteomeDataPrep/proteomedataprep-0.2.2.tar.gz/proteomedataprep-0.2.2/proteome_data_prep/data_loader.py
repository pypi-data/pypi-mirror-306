import polars as pl
import pandas as pd
import re
import boto3
from dataclasses import dataclass
import numpy as np
from typing import Optional, List, Union, Literal

from .data_container import *
from .data_utils import *

pd.options.mode.chained_assignment = None

@dataclass
class DataLoader():


    def load_data(self, 
               path: str,
               filetype: Optional[str] = None,
               datatype: Optional[str] = None,
               target: Optional[str] = None,
               batch: Optional[str] = None,
               get_batches: bool = False,
               include_stripped_sequence: bool = False) -> DataContainer:
        """
        Load data from a specified path and return a DataContainer instance.

        Parameters:
        ----------
        path : str
            The file path to load data from.
        filetype : Optional[str]
            The type of file (e.g., "diann" or "encyclopedia"). If None, 
            it will be inferred from the path.
        datatype : Optional[str]
            The type of data (e.g., "protein" or "peptide"). If None, 
            it will be inferred from the path.
        target : Optional[str]
            Specific target to filter the data.
        batch : Optional[str]
            Batch to filter the data.
        get_batches : bool
            Whether to retrieve batch information.
        include_stripped_sequence : bool
            Whether to include stripped sequences. Raises TypeError if
            the datatype is "protein".

        Returns:
        -------
        DataContainer
            An instance of DataContainer containing the loaded data.
        """
        
        # Instantiate DataContainer
        data_container = DataContainer(path,
                                       filetype=filetype,
                                       datatype=datatype)
        
        if data_container.datatype == "protein" and include_stripped_sequence:
            raise TypeError("Stipped sequences are only available for peptide"
                            " files.")

        if get_batches:
            data_container.batches = self.get_batches(data_container.path)
        
        lazy_df = self._load_lazy_df(path)

        # Filter for targets, if provided
        if target is not None:
            lazy_df = self._filter_targets(data_container.filetype, 
                                           lazy_df,
                                           target)

        # Collect all column names for filtering
        df = self._select_columns_of_interest(data_container, 
                    lazy_df,
                    include_stripped_sequence=include_stripped_sequence,
                    batch=batch)
        
        # Collect the DataFrame
        df = df.collect(streaming=True).to_pandas()

        df = self.clean_data(df)

        data_container.raw_df = df

        return data_container
    
    def clean_data(self, df:pd.DataFrame) -> pd.DataFrame:
        id_cols = detect_id_columns(df)

        df = df.convert_dtypes()

        for col in id_cols:
            df[col] = df[col].astype("category")
        
        return df
    
    @staticmethod
    def extract_unique_genes(df: pd.DataFrame) -> list[str]:
        """
        Extract unique gene names from a DataFrame column.

        This method retrieves unique gene names from the "Genes" column
        of the provided DataFrame. The gene names are expected to be
        separated by semicolons (`;`). The method handles cases where
        multiple genes are listed for a single entry.

        Parameters:
        ----------
        df : pd.DataFrame
            A DataFrame containing a column named "Genes", where each
            entry may contain one or more gene names separated by
            semicolons.

        Returns:
        -------
        list
            A list of unique gene names extracted from the "Genes" column.

        Notes:
        -----
        NaN values in the "Genes" column will be ignored during the
        extraction process.
        """
        return list({
            gene for genes in df["Genes"].dropna()for gene in genes.split(";")
            })
    
    def _filter_targets(self, filetype: str, 
                        lazy_df: pl.LazyFrame, 
                        target: Union[str, list, set, np.ndarray]
                        ) -> pl.LazyFrame:
        """Filter the DataFrame based on target genes.

        Parameters:
        ----------
        filetype : str
            The type of the data file ("diann" or "encyclopedia").
        lazy_df : pl.LazyFrame
            A lazy DataFrame containing the data to be filtered.
        target : Union[str, list, set, np.ndarray]
            The target gene(s) to filter for. Can be a single gene or a collection.

        Returns:
        -------
        pl.LazyFrame
            The filtered lazy DataFrame.

        Raises:
        ------
        TypeError
            If target is not a string, list, set, or array.
        NotImplementedError
            If target filtering is requestedf for an encyclopedia file.
        """
        if not isinstance(target, (list, str, set, np.ndarray)):
            raise TypeError("Target must be a string, list, set, or array.")
        
        if isinstance(target, str):
            target = [target]

        if filetype == "diann" and target is not None:
            return lazy_df.filter(pl.col("Genes").is_in(target))
        elif filetype == "encycolopedia" and target is not None:
            raise NotImplementedError("Target filtering for encyclopedia data" \
                                      " has yet to be implemented.")
    
    def _get_run_columns(self, all_columns: List[str],
                         batch: Union[str, List[str]]) -> List[str]:
        """
        Retrieve columns from all_columns that match the specified batch.

        This method filters the list of columns to include only those that
        contain any of the specified batch identifiers and are not in the 
        list of bad batches.

        Parameters:
        ----------
        all_columns : List[str]
            A list of column names to filter.
        
        batch : Union[str, List[str]]
            A single batch identifier or a list of batch identifiers to match 
            against the column names.

        Returns:
        -------
        List[str]
            A list of column names that match the specified batch and are not 
            in the bad_batches.

        Raises:
        ------
        TypeError
            If batch is not a string or a list of strings.
        """
        if not isinstance(batch, (list, str)):
            raise TypeError("Batch should be a string or a list of strings.")

        if isinstance(batch, str):
            batch = [batch]

        return [
            col for col in all_columns
            if any(b in col for b in batch) and col not in bad_batches
        ]
        
    def _select_columns_of_interest(self,
                                    data_container,
                                    lazy_df,
                                    include_stripped_sequence: bool = False,
                                    batch: Optional[Union[str, List[str]]] \
                                        = None) -> pl.LazyFrame:
        """
        Select columns of interest from the given lazy DataFrame based on the 
        provided batch and other conditions.

        This method filters the columns of the lazy DataFrame to include 
        identifier columns and relevant data columns based on the specified 
        batch. If a batch is not provided, it retrieves all columns that 
        meet certain criteria. It can also optionally include the stripped 
        sequence column for DIANN file types.

        Parameters:
        ----------
        data_container : DataContainer
            An instance of DataContainer containing metadata about the data.

        lazy_df : LazyFrame
            A lazy DataFrame from which to select columns.

        include_stripped_sequence : bool, optional
            Whether to include the "Stripped.Sequence" column for DIANN data. 
            Default is False.

        batch : Optional[Union[str, List[str]]], optional
            A single batch identifier or a list of batch identifiers to filter 
            the columns. Default is None.

        Returns:
        -------
        LazyFrame
            A lazy DataFrame containing only the selected columns of interest.

        Raises:
        ------
        ValueError
            If the provided data container does not contain a valid file type.
        """
        # Detect identifier columns
        id_cols = self._detect_datacontainer_id_columns(data_container)
        all_columns = lazy_df.collect_schema().names()

        if batch:
            selected_cols = id_cols + self._get_run_columns(all_columns, batch)
        else: # get all columns
            selected_cols = id_cols + [col for col in all_columns \
                                      if (col.endswith(".d") \
                                          or col.endswith(".mzML")) \
                                        and col not in bad_batches]
            
        if data_container.filetype == "diann" and include_stripped_sequence:
            selected_cols.append("Stripped.Sequence")

        return lazy_df.select(selected_cols)
    
    def _detect_datacontainer_id_columns(self, 
                                         data: DataContainer) -> List[str]:
        """
        Detect the identifier columns based on the type of data provided.

        This method checks the type of the input data, which can be a 
        DataContainer or a DataFrame, and returns a list of relevant 
        identifier column names based on the filetype and datatype 
        specified in the DataContainer.

        Parameters:
        ----------
        data : DataContainer
            The input data from which to detect ID columns. 

        Returns:
        -------
        List[str]
            A list of identifier column names.

        Raises:
        ------
        TypeError
            If the provided data is neither a DataContainer.
        """
        if not isinstance(data, DataContainer):
            raise TypeError(f"Expected DataContainer, got {type(data)}")
        
        if isinstance(data, DataContainer):
            if data.filetype == "diann":
                if data.datatype == "protein":
                    return ["Protein.Ids", "Genes"]
                else:
                    return ["Protein.Ids", "Genes", "Precursor.Id"]
            else: # encyclopedia
                if data.datatype == "protein":
                    return ["Protein"]
                else:
                    return ["Peptide", "Protein"]

    @staticmethod
    def _detect_file_format(path: str) -> Literal["csv", "tsv"]:
        """
        Detect the file format based on the file extension.

        This method checks the file extension of the given path 
        and returns the corresponding file format. It supports 
        CSV and TSV formats.

        Parameters:
        ----------
        path : str
            The file path to check for format detection.

        Returns:
        -------
        Literal["csv", "tsv"]
            The detected file format.

        Raises:
        ------
        ValueError
            If the file format is unsupported.
        """
        if path.endswith(".csv"):
            return "csv"
        elif path.endswith(".tsv") or path.endswith(".txt"):  # Encyclopedia paths may end with .txt
            return "tsv"
        else:
            raise ValueError(f"Unsupported file format for file: {path}")
        
    @staticmethod
    def _load_lazy_df(path: str) -> pl.LazyFrame:
        """
        Loads a lazy DataFrame from a specified file path.

        This method detects the file format (CSV or TSV) and 
        initializes a lazy DataFrame using Polars. It handles 
        loading from S3 paths by applying appropriate storage options.

        Parameters
        ----------
        path : str
            The path to the data file (CSV or TSV) to load.

        Returns
        -------
        pl.LazyFrame
            A lazy DataFrame representation of the loaded data.

        Raises
        ------
        ValueError
            If the file format is unsupported.
        """
        file_format = DataLoader._detect_file_format(path)
        sep = "," if file_format == "csv" else "\t"
        if path.startswith("s3"):
            storage=DataLoader.get_storage_options()
            lazy_df = pl.scan_csv(path,
                        separator=sep,
                        storage_options=storage,
                        infer_schema_length=10000,
                        )
        else:
            lazy_df = pl.scan_csv(path,
                        separator=sep,
                        infer_schema_length=10000,
                        )
        
        return lazy_df
    

    @staticmethod
    def get_batches(path):
        """
        Extracts unique batch numbers from the column names of a lazy DataFrame.

        This method loads a lazy DataFrame from the specified path and 
        retrieves unique batch numbers by examining the column names.

        Parameters
        ----------
        path : str
            The path to the data file from which to load the DataFrame.

        Returns
        -------
        list
            A list of unique batch numbers extracted from the column names.
        """
        lazy_df = DataLoader._load_lazy_df(path)
        column_names = lazy_df.collect_schema().names()

        batches = {extract_batch_num(column) \
                   for column in column_names}
        
        return list(batches)

    @staticmethod
    def get_storage_options() -> dict[str, str]:
        """Get AWS credentials to enable polars scan_parquet functionality.
        """
        credentials = boto3.Session().get_credentials()
        return {
            "aws_access_key_id": credentials.access_key,
            "aws_secret_access_key": credentials.secret_key,
            "session_token": credentials.token,
            "aws_region": "us-west-2",
        }