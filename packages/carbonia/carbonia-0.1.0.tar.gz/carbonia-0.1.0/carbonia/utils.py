from tableauhyperapi import HyperProcess, Connection, Telemetry, TableDefinition, SqlType, Inserter, TableName, CreateMode
import pandas as pd
import logging
import json
import yaml
import os 
from dotenv import load_dotenv
from openai import OpenAI

def find_columns_labels(source_df, api_key=None, contextual_columns_nb=1, model = "gpt-4o-mini"):
    df_head = source_df.head().to_json(orient='records')  
    Category_name_possibilities = ["Sub_category", "Category", "Sub_family", "Family", "sub_domain", "domain"]   
    example_json = {"date_column": "Date", "amount_column": "Amount", "unit_column": "Currency", "description_column": "Description", "contextual_columns": Category_name_possibilities[:contextual_columns_nb]}
    prompt = f"""
    You are given a DataFrame with the following head: {df_head}. Your task is to identify and provide the column names that best represent the following information:

    1. **Date of Purchase**: The column that represents the date on which the purchase was made.
    2. **Amount**: The column that specifies the amount (money for example) involved in the purchase.
    3. **Unit**: The column that indicates the unit of the article purchased.
    4. **Description**: A column that describe the article in a way understandable by a human, the values in these column should be a text description, not a number.
    5. **Contextual Columns**: If it exists, {contextual_columns_nb} columns that provide additional context to the purchase, else an empty list.

    Please consider both the column labels and the values they contain to ensure accurate identification. 
    Assign them as:

    - "date_column"
    - "amount_column"
    - "unit_column"
    - "description_column"
    - "contextual_columns"

    Provide your response in a valid JSON format following this schema: {json.dumps(example_json)}
    """

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"]) or OpenAI(api_key=api_key)
    success = False

    while not success:
        chat_completion = client.chat.completions.create(
                    model=model,
                    response_format={"type": "json_object"},
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": json.dumps(df_head)}
                    ]
                )
        
        data = chat_completion.choices[0].message.content
        data_json = json.loads(data)
        success = True
    #If one of the elements is empty, print a warning
    for key in data_json.keys():
        if not data_json[key]:
            logging.warning(f"Warning: {key} is empty")
    return data_json

def load_global_env():
    env_path = os.path.expanduser('~/global_env/.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        raise FileNotFoundError(f"No global .env file found at {env_path}")

def setup_logging():
    """Set up logging configuration."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_file_paths(base_path: str, suffix: str) -> str:
    """Generate file paths with given suffix."""
    return base_path.replace("." + base_path.split(".")[-1], suffix)
def emphasize_and_combine_columns(df: pd.DataFrame, source_columns_emphasis: list, source_columns_to_embed: list) -> pd.DataFrame:
    """
    Emphasizes the specified columns by adding asterisks around non-empty strings, 
    replaces "**" with an empty string, and combines the specified columns into one.

    Args:
    df (pd.DataFrame): The input DataFrame.
    source_columns_emphasis (list): The columns to emphasize.
    source_columns_to_embed (list): The columns to combine into a single column.

    Returns:
    pd.DataFrame: The modified DataFrame with emphasized and combined columns.
    """
    df[source_columns_emphasis] = df[source_columns_emphasis].fillna("")
    df[source_columns_emphasis] = df[source_columns_emphasis].apply(lambda x: "*" + x + "*")
    df[source_columns_emphasis] = df[source_columns_emphasis].replace(r'^\*{2}$', '', regex=True)
    df["combined"] = df[source_columns_to_embed].apply(lambda x: ' '.join(x.astype(str)), axis=1)
    return df

def hierarchical_selection(source_df,source_columns_to_embed, merged_column, reverse_col=False):
    source_df_copy = source_df.copy()
    source_columns_to_embed = source_columns_to_embed[::-1]
    source_df_copy[merged_column] = source_df_copy[source_columns_to_embed[0]]
    for col in source_columns_to_embed[1:]:
        source_df_copy[merged_column] = source_df_copy[merged_column].combine_first(source_df_copy[col])

    return source_df_copy

def pre_process_source_df(source_columns_to_embed, source_df):

    source_df = source_df.dropna(subset=source_columns_to_embed,how = 'all')
    # Remove numbers from the specified columns
    for column in source_columns_to_embed:
        source_df[column] = source_df[column].str.replace(r'\d+', '', regex=True)
    return source_df

def update_dataframe_with_correction(source_df, corrected_df, key_column):
    '''Update the source DataFrame with corrected values from the corrected DataFrame coming from a manual correction.'''
    source_df_copy = source_df.copy()
    corrected_df_copy = corrected_df.copy()
    
    # Reset index to ensure no duplicate labels interfere with the merge
    source_df_copy.reset_index(drop=True, inplace=True)
    corrected_df_copy.reset_index(drop=True, inplace=True)
    
    # Merging dataframes on the key_column
    merged_df = pd.merge(source_df_copy, corrected_df_copy, on=key_column, how='left', suffixes=('', '_corrected'))
    
    # List of columns to update
    columns_to_update = [col for col in corrected_df_copy.columns if col != key_column]
    
    # Update the columns in source_df_copy with values from corrected_df
    for col in columns_to_update:
        source_df_copy[col] = merged_df.apply(
            lambda row: row[f'{col}_corrected'] if pd.notnull(row[f'{col}_corrected']) else row[col], axis=1
        )
    
    return source_df_copy
    

def get_sqltype(dtype):
    """Convert pandas dtype to Tableau Hyper SQLType."""
    if pd.api.types.is_integer_dtype(dtype):
        return SqlType.big_int()
    elif pd.api.types.is_float_dtype(dtype):
        return SqlType.double()
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return SqlType.timestamp()
    elif pd.api.types.is_bool_dtype(dtype):
        return SqlType.bool()
    else:
        return SqlType.text()

def df_to_hyper(df, output_path):
    """Export a pandas DataFrame to a Tableau Hyper file."""
    
    # Ensure all data is in the correct format before insertion
    receiver_data = []
    for _, row in df.iterrows():
        row_data = []
        for value in row:
            if pd.isnull(value):  # Handle NaN values
                row_data.append(None)
            else:
                row_data.append(value)
        receiver_data.append(row_data)
    
    # Define the table schema dynamically based on DataFrame columns
    table_definition = TableDefinition(
        table_name=TableName("Extract", "Extract"),
        columns=[
            TableDefinition.Column(col, get_sqltype(dtype)) for col, dtype in zip(df.columns, df.dtypes)
        ]
    )

    # Start the Hyper process and create the Hyper file
    with HyperProcess(telemetry=Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
        with Connection(endpoint=hyper.endpoint, database=output_path, create_mode=CreateMode.CREATE_AND_REPLACE) as connection:
            connection.catalog.create_schema("Extract")
            connection.catalog.create_table(table_definition)
            with Inserter(connection, table_definition) as inserter:
                inserter.add_rows(receiver_data)
                inserter.execute()
    

def assign_columns(api_key, columns, source_df):
                
    success = False
    attempts = 3
    for attempt in range(attempts):
        column_label = find_columns_labels(source_df.drop(columns=["embedding"], errors='ignore'), api_key, contextual_columns_nb=columns["contextual_nb_columns"])
        
        #Change key name of "description_column" to "source_columns_to_embed"
        column_label["source_columns_to_embed"] = column_label.pop("description_column")
        column_label["source_columns_emphasis"] = column_label["source_columns_to_embed"]
        column_label["source_columns_to_embed"] = [column_label["source_columns_to_embed"]] + column_label["contextual_columns"]
        column_label.pop("contextual_columns")
        for key in column_label:
            if not (columns[key]):
                columns[key] = column_label[key]

        success = all(columns[key] for key in column_label)
        if success:
            break
        else:
            logging.warning(f"Failed to assign all columns. Check if you have the following columns in your data: {column_label.keys()}, Retrying...")

    return columns

import re
import unicodedata
def normalize_text(text):
    """Normalize and clean the text string by:
    - Removing excessive whitespace
    - Stripping non-printable characters
    - Replacing special characters
    - Normalizing unicode characters to ASCII
    """
    # Normalize unicode characters to their closest ASCII equivalent
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    
    # Remove non-printable characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading and trailing whitespace
    text = text.strip()
    
    return text

def check_and_normalize_series(series):
    """Check and normalize a pandas Series of strings."""
    return series.apply(lambda x: normalize_text(str(x)))

