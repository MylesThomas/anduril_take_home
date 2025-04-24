import re
import time
from typing import Dict

import numpy as np
import pandas as pd
import yaml

def load_yaml(filepath: str) -> Dict:
    """
    Load a YAML file and return its contents as a dictionary.

    Args:
        filepath (str): Path to the YAML file.

    Returns:
        dict: Parsed YAML content.
    """
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

def to_snake_case(s: str) -> str:
    """Convert a string to snake_case."""
    return re.sub(r'[\W]+', '_', s).strip('_').lower()

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names to snake_case."""
    df.columns = [to_snake_case(col) for col in df.columns]
    return df

class Timer:
    def __init__(self):
        self.start_time = time.time()
        self.end_time = None

    def stop(self):
        self.end_time = time.time()
        elapsed_time = self.end_time - self.start_time
        elapsed_minutes = int(elapsed_time // 60)
        elapsed_seconds = int(elapsed_time % 60)
        print(f"Elapsed time: {elapsed_minutes} minutes and {elapsed_seconds} seconds")

    def ping(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        elapsed_minutes = int(elapsed_time // 60)
        elapsed_seconds = int(elapsed_time % 60)
        print(
            f"Elapsed time: {elapsed_minutes} minutes and {elapsed_seconds} seconds",
            end="\r"
        )
