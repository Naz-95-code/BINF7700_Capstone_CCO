import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load data
data = pd.read_csv("../results/signature_exposures.tsv", sep="\t", index_col=0)

# Remove empty columns
data = data.loc[:, (data != 0).any(axis=0)]

# Log transform
data_log = np.log1p(data)

# Normalize per sample
data_norm = data_log.div(data_log.sum(axis=1), axis=0)

# Plot
plt.figure(figsize=(22,14)) 

ax = sns.heatmap(
    data_norm,
    cmap="viridis",
    cbar_kws={'label': 'Normalized Contribution'}
)


plt.xticks(rotation=45, ha='right', fontsize=10)   # signatures
plt.yticks(rotation=0, fontsize=9)                 # samples

# Titles
plt.title("COSMIC Signature Contributions (Log + Normalized)", fontsize=16)
plt.xlabel("Signatures", fontsize=12)
plt.ylabel("Samples", fontsize=12)

plt.tight_layout()

# Save high quality
plt.savefig("../results/signature_heatmap_improved.png", dpi=400, bbox_inches='tight')

plt.close()
