from pathlib import Path
import pandas as pd

def load_clean_data(config):
    base_path = Path(config["base_path"])
    csv_file = base_path / config["paths"]["clean_data"] / config["data"]["clean"]["path"]
    columns_config = config["data"]["clean"]["columns"]

    dtype_map = {}
    parse_dates = []

    for col, dtype in columns_config.items():
        if "datetime" in dtype:
            parse_dates.append(col)
        elif "string" in dtype:
            dtype_map[col] = "string"
        else:
            dtype_map[col] = dtype

    df = pd.read_csv(csv_file, dtype=dtype_map, parse_dates=parse_dates)
    return df
