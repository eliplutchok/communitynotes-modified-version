import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_column_distribution_tsv(file_name, column_prefix, bins, ax, stats_file):
    # Load the data with tab as delimiter
    data = pd.read_csv(file_name, delimiter='\t')

    # Find columns starting with the specified prefix
    relevant_columns = [col for col in data.columns if col.startswith(column_prefix)]

    # Replace 'nan' strings and blanks with NaN, then convert to numeric
    for col in relevant_columns:
        data[col] = data[col].replace({'nan': np.nan, '': np.nan})
        data[col] = pd.to_numeric(data[col], errors='coerce')

    # Filter rows where all relevant columns are rational numbers
    valid_rows = data.dropna(subset=relevant_columns)

    # Sum these columns for each valid row
    valid_rows['summed_values'] = valid_rows[relevant_columns].sum(axis=1, skipna=False)

    # Calculate range, mean, and standard deviation for valid rows
    value_range = valid_rows['summed_values'].max() - valid_rows['summed_values'].min()
    mean_value = valid_rows['summed_values'].mean()
    std_dev = valid_rows['summed_values'].std()

    # Write the results to a text file
    with open(stats_file, 'a') as f:
        f.write(f"File: {file_name}, Prefix: {column_prefix}\n")
        f.write(f"Number of valid rows (all relevant columns rational): {valid_rows.shape[0]}\n")
        f.write(f"Range: {value_range}, Mean: {mean_value}, Standard Deviation: {std_dev}\n\n")

    # Plot the distribution on the provided axes
    ax.hist(valid_rows['summed_values'], bins=bins, edgecolor='black')
    ax.set_xlabel('Summed Values')
    ax.set_ylabel('Frequency')
    ax.set_title(f'{column_prefix} (Range: {round(value_range, 4)}, Mean: {round(mean_value, 4)}, STD: {round(std_dev, 4)})')

# Create a figure with 4 subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
stats_file = 'distribution_stats.txt'

# Clear the statistics file before writing new content
open(stats_file, 'w').close()

# Call your function for each dataset and subplot
numFactors = 2
interceptRegularizationDampener = numFactors
plot_column_distribution_tsv(f"scored_notes_{numFactors}_{interceptRegularizationDampener}.tsv", 'coreNoteFactor', 1000, axs[0, 0], stats_file)
plot_column_distribution_tsv(f"helpfulness_scores_{numFactors}_{interceptRegularizationDampener}.tsv", 'coreRaterFactor', 1000, axs[0, 1], stats_file)
plot_column_distribution_tsv(f"scored_notes_{numFactors}_{interceptRegularizationDampener}.tsv", 'coreNoteIntercept', 1000, axs[1, 0], stats_file)
plot_column_distribution_tsv(f"helpfulness_scores_{numFactors}_{interceptRegularizationDampener}.tsv", 'coreRaterIntercept', 1000, axs[1, 1], stats_file)

# Adjust layout and save the figure
plt.tight_layout()
plt.savefig(f'combined_plots_{numFactors}_{interceptRegularizationDampener}.png')
plt.show()
