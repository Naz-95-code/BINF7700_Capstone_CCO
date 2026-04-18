import numpy as np
import matplotlib.pyplot as plt
import sys

input_path = sys.argv[1]
output_path = sys.argv[2]

# Load data
data = np.loadtxt(input_path)

# Plot (NO scaling)
plt.figure()
plt.hist(data, bins=30, density=True)
plt.xlim(0, 150)

plt.title("Oncogan Breast Mutation Burden")
plt.xlabel("Mutation Count")
plt.ylabel("Density")

plt.savefig(output_path)
plt.close()

print("Synthetic breast plot saved to:", output_path)
