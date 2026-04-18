import pandas as pd
import matplotlib.pyplot as plt

file_path = "../results/tcga_breast_counts.txt"
df = pd.read_csv(file_path, sep=" ", header=None, names=["Sample", "Mutation_Count"])

plt.figure()

# SAME SCALE AS SYNTHETIC
plt.hist(df["Mutation_Count"], bins=30, density=True)

# MATCH AXIS
plt.xlim(0, 150)

plt.xlabel("Mutation Count")
plt.ylabel("Density")
plt.title("TCGA Breast Mutation Burden (Normalized)")

plt.savefig("../results/tcga_breast_histogram.png")

print("TCGA histogram saved")

