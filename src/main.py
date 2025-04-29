import pandas as pd
from pathlib import Path
import logging
from utils import load_yaml, Timer
from data_loader import load_clean_data
from model import run_monte_carlo, plot_simulation_results

def setup_logging(config):
    log_file_path = Path(config["base_path"]) / config["logging"]["path"]
    log_file_path.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, config["logging"].get("level", "INFO").upper()),
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file_path),
            logging.StreamHandler()
        ]
    )

def main():
    # Path setup
    base_path = Path(__file__).resolve().parent.parent
    config_path = base_path / "config/data.yaml"

    config = load_yaml(config_path)
    config["base_path"] = str(base_path)

    setup_logging(config)
    logger = logging.getLogger(__name__)
    logger.info("Started main.py")

    timer = Timer()

    # Load cleaned data
    df = load_clean_data(config)

    # Filter out Upside
    upside_df = df[df['forecast_category'] == 'Upside']
    df = df[df['forecast_category'] != 'Upside']

    # --- Run V1 Simulation ---
    version = "v1.0"
    sim_sums, targets, years, summary_df = run_monte_carlo(df, config, version)
    print(summary_df)
    plot_simulation_results(sim_sums, targets, years, config, version)

    # --- Run V2 Simulation (with Upside) ---
    df = pd.concat([df, upside_df], ignore_index=True)
    version = "v2.0"
    sim_sums, targets, years, summary_df = run_monte_carlo(df, config, version)
    print(summary_df)
    plot_simulation_results(sim_sums, targets, years, config, version)

    timer.stop()

if __name__ == "__main__":
    main()
