import pandas as pd
import re
from typing import List

def detect_id_columns(df: pd.DataFrame) -> List[str]:
    """
    Detect the identifier columns based on the type of data provided.

    This method checks the type of the input data, which can be a 
    DataContainer or a DataFrame, and returns a list of relevant 
    identifier column names based on the filetype and datatype 
    specified in the DataContainer.

    Parameters:
    ----------
    data :  pd.DataFrame
        The input data from which to detect ID columns. 
        Can be either a DataContainer or a DataFrame.

    Returns:
    -------
    List[str]
        A list of identifier column names.

    Raises:
    ------
    TypeError
        If the provided data is neither a DataContainer nor a DataFrame.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Expected DataFrame. Got {type(df)}")
        
    if "Protein.Ids" in df.columns:
        if "Precursor.Id" in df.columns:
            id_cols = ["Protein.Ids", "Genes", "Precursor.Id"]
        else:
            id_cols = ["Protein.Ids", "Genes"]
    elif "Peptide" in df.columns:
        id_cols = ["Peptide", "Protein"]
    else:
        id_cols = ["Protein"]
    
    if "Is TF" in df.columns:
        id_cols.append("Is TF")
    
    return id_cols

def get_quant_columns(df: pd.DataFrame) -> List[str]:
    return [col for col in df.columns
            if (col.endswith(".d") or col.endswith(".mzML"))]

def extract_batch_num(filename: str) -> str:
    """Extract the batch number from a string.

    example: "MSR1340_SET10REP1E4_DMSO_DIA.d" -> "SET10REP1"

    Args:
        filename (str): The filename (or other string) to parse

    Returns:
        str: The batch number
    """
    batch = re.search(r'SET\d+(-\d+)?REP\d+(-\d+)?',
                        filename,
                        re.IGNORECASE)
    if isinstance(batch, re.Match):
        return batch[0]