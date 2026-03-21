import numpy as np
import matplotlib.pyplot as plt
import sys

# Input & output
input_path = sys.argv[1]
output_path = sys.argv[2]

# Load data
data = np.loadtxt(input_path)

# Normalize (scale to TCGA-like range)
scaled = data / np.max(data) * 150

# Plot (normalized)
plt.hist(scaled, bins=30, density=True)
plt.title("Synthetic Breast Mutation Burden (Normalized)")
plt.xlabel("Mutation Count")
plt.ylabel("Density")

# Save
plt.savefig(output_path)
plt.close()

print("Breast plot saved to:", output_path)
