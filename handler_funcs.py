import pandas as pd

def convert_numberobj_to_float(df, column): 
    """
    Converts a currency column in a pandas df to float from object type

    args: 
    df (pd.dataframe): the dataframe containing column
    column (str) : name of column to convert

    returns: 
    df with coverted column

    """
    # Remove currency symbols and commas
    df[column] = df[column].astype(str).str.replace(r'[$,]', '', regex=True)

    # Convert to numeric, coercing errors (invalid values become NaN)
    df[column] = pd.to_numeric(df[column], errors='coerce')

    # Replace NaN with 0
    df[column] = df[column].fillna(0)

    return df

