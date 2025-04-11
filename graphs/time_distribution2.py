import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os

# === Settings ===
folder1 = '/home/matt/Desktop/AACT/llama3.1:8b/ctflogs'   # <<<<< First CSV folder
folder2 = '/home/matt/Desktop/AACT/qwq/ctflogs'  # <<<<< Second CSV folder
time_column = 'reasoning time'                # <<<<< Column name (must be the same in both)
file_pattern = '*.csv'
save_plot_as = 'duration_distribution_comparison.png'

# === Function to Load CSVs ===
def load_duration_data(folder_path, time_column):
    csv_files = glob.glob(os.path.join(folder_path, file_pattern))
    if not csv_files:
        raise ValueError(f"No CSV files found in {folder_path}")
    
    dfs = []
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            if time_column in df.columns:
                dfs.append(df[[time_column]])
            else:
                print(f"Warning: {file} does not contain column '{time_column}'")
        except Exception as e:
            print(f"Error reading {file}: {e}")
    
    if not dfs:
        raise ValueError(f"No valid CSV files with the specified time column in {folder_path}")
    
    combined_df = pd.concat(dfs, ignore_index=True)
    return combined_df

# === Load both datasets ===
data1 = load_duration_data(folder1, time_column)
data2 = load_duration_data(folder2, time_column)

# === Plot distributions with KDE curves ===
plt.figure(figsize=(14, 7))

# Plot histograms + KDE curves
sns.histplot(data1[time_column], bins=50, kde=True, label='Dataset 1', color='blue', alpha=0.4)
sns.histplot(data2[time_column], bins=50, kde=True, label='Dataset 2', color='orange', alpha=0.4)

plt.xlabel('Duration (seconds)')
plt.ylabel('Frequency')
plt.title('Distribution of Step Durations (in Seconds)')
plt.legend()
plt.tight_layout()
plt.grid(True)

# Save and show
plt.savefig(save_plot_as)
plt.show()

print(f"Plot saved as {save_plot_as}")
