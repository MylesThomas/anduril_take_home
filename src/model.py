import os
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

def run_monte_carlo(df, config, version="v1.0"):
    sim_cfg = config['simulation']['monte_carlo']
    n_sims = sim_cfg['n_simulations']
    seed = sim_cfg['random_seed']
    targets = {t['year']: t['revenue_target'] for t in sim_cfg['targets']}
    years = sorted(df['revenue_year'].unique())

    p = df['probability_of_award_smart50'].values
    rev = df['revenue_amount'].values
    rng = np.random.default_rng(seed)

    wins = rng.random((len(p), n_sims)) < p[:, None]
    rev_matrix = wins * rev[:, None]

    sim_sums = {}
    for yr in years:
        mask = (df['revenue_year'] == yr).values
        sim_sums[yr] = rev_matrix[mask].sum(axis=0)

    # Build summary DataFrame
    summary = []
    for yr in years:
        sims = sim_sums[yr]
        tgt = targets.get(yr, np.nan)
        summary.append({
            'Year': yr,
            'Target ($B)': tgt / 1e9,
            'Mean Forecast ($B)': sims.mean() / 1e9,
            'Std Dev ($B)': sims.std(ddof=1) / 1e9,
            'P(Meet Target)': (sims >= tgt).mean()
        })

    summary_df = pd.DataFrame(summary)

    # Save summary with versioned filename
    base_path = Path(config['base_path'])
    output_path = Path(config["paths"]["output_data"])
    output_file_base = config['simulation']['monte_carlo']['output']['summary_stats']
    output_file = base_path / output_path / f"{Path(output_file_base).stem}_{version}.csv"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    summary_df.to_csv(output_file, index=False)

    return sim_sums, targets, years, summary_df

def plot_simulation_results(sim_sums, targets, years, config, version="v1.0"):
    base_path = Path(config['base_path'])
    output_path = Path(config["paths"]["output_data"])
    dist_plot_base = config['simulation']['monte_carlo']['output']['distributions_plot']
    dist_plot_path = base_path / output_path / f"{Path(dist_plot_base).stem}_{version}.png"
    dist_plot_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))
    color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
    year_colors = {yr: color_cycle[i % len(color_cycle)] for i, yr in enumerate(years)}

    _, _, _ = plt.hist(sim_sums[years[0]], bins=50, alpha=0)
    y_max = plt.ylim()[1]
    plt.clf()

    for yr in years:
        sims = sim_sums[yr]
        color = year_colors[yr]
        mean_val = sims.mean()
        tgt = targets[yr]
        shortfall = tgt - mean_val
        pct_increase = shortfall / mean_val * 100
        pct_achieved = mean_val / tgt * 100

        plt.hist(sims, bins=50, alpha=0.4, color=color, label=f"{yr} distribution")
        plt.axvline(tgt, color=color, linestyle='--', linewidth=2, label=f"{yr} target")

        plt.text(
            mean_val,
            y_max * 0.85 - (years.index(yr) * y_max * 0.06),
            f"Mean: ${mean_val:,.0f}\n"
            f"Target: ${tgt:,.0f}\n"
            f"Shortfall: ${shortfall:,.0f}\n"
            f"({pct_increase:.1f}% below target)\n"
            f"Achieved: {pct_achieved:.1f}%",
            color=color,
            ha='center',
            va='top',
            fontsize=9,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9, edgecolor=color)
        )

    plt.legend(title='Year / Target', ncol=2)
    plt.xlabel('Simulated Revenue ($)')
    plt.ylabel('Frequency')
    plt.gca().xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{x/1e9:.1f}B"))
    plt.title(f'Monte Carlo Revenue Distributions (mc model {version})')
    plt.tight_layout()
    plt.xlim(0, 30e9)
    plt.savefig(dist_plot_path)
    plt.show()
