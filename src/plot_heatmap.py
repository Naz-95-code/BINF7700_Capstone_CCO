import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

# Load data
data = pd.read_csv("../results/signature_exposures.tsv", sep="\t", index_col=0)

# Remove empty columns
data = data.loc[:, (data != 0).any(axis=0)]

# Log transform
data_log = np.log1p(data)

# Normalize per sample
data_norm = data_log.div(data_log.sum(axis=1), axis=0)

# Create cancer type labels from sample names
sample_names = data_norm.index.astype(str)
cancer_type = ["breast" if "breast" in s.lower() else "prostate" for s in sample_names]

# Sort: Breast first, then Prostate
data_norm["cancer_type"] = cancer_type
data_norm = data_norm.sort_values("cancer_type")
cancer_type = data_norm["cancer_type"].tolist()
data_norm = data_norm.drop(columns="cancer_type")

# 🔥 FIND EXACT SPLIT POSITION (CORRECT FIX)
split_index = cancer_type.index("prostate")

# Assign colors
row_colors = ["#F28C28" if ct == "breast" else "#2ca02c" for ct in cancer_type]

# Plot
plt.figure(figsize=(22,14))

ax = sns.heatmap(
    data_norm,
    cmap="viridis",
    cbar_kws={
        'label': 'Normalized Contribution',
        'shrink': 0.6,
        'aspect': 20
    },
    yticklabels=False
)

# Bold SBS labels
ax.set_xticklabels(
    ax.get_xticklabels(),
    rotation=45,
    ha='right',
    fontsize=10,
    fontweight='bold'
)

# Highlight important signatures
key_signatures = {"SBS1", "SBS3", "SBS5", "SBS8", "SBS13", "SBS40"}

for label in ax.get_xticklabels():
    if label.get_text() in key_signatures:
        label.set_color("red")
        label.set_fontsize(12)
        label.set_fontweight("bold")

# Add left color strip
for i, color in enumerate(row_colors):
    ax.add_patch(
        plt.Rectangle(
            (-1.8, i),
            1.2,
            1,
            color=color,
            transform=ax.transData,
            clip_on=False
        )
    )

# ADD WHITE SEPARATOR EXACTLY BETWEEN BREAST & PROSTATE
ax.hlines(
    split_index,
    xmin=-2,
    xmax=data_norm.shape[1],
    colors='white',
    linewidth=5
)

# Titles
plt.title("COSMIC Signature Contributions (Log + Normalized)", fontsize=16)
plt.xlabel("Signatures (SBS1–SBS90)", fontsize=12)
plt.ylabel("Samples", fontsize=12)

# Legend
legend_elements = [
    Patch(facecolor='#F28C28', label='Breast Cancer'),
    Patch(facecolor='#2ca02c', label='Prostate Cancer')
]

plt.legend(
    handles=legend_elements,
    loc='upper left',
    bbox_to_anchor=(1.02, 1),
    borderaxespad=0
)

# Layout fix (prevents overlap with colorbar)
plt.tight_layout(rect=[0, 0, 0.85, 1])

# Save
plt.savefig("../results/signature_heatmap_improved.png", dpi=400, bbox_inches='tight')

plt.close()
