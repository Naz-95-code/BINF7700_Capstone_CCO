import os
import matplotlib.pyplot as plt

def load(file):
    values = []
    with open(file) as f:
        for line in f:
            line = line.strip()
            if line:
                values.append(int(line))
    return values

real_breast = load("data/txt/real_breast_counts.txt")
real_prostate = load("data/txt/real_prostate_counts.txt")

real_breast_filtered = [x for x in real_breast if x <= 150]
real_prostate_filtered = [x for x in real_prostate if x <= 150]

os.makedirs("../figures", exist_ok=True)

plt.figure()
plt.hist(real_breast_filtered, bins=30, edgecolor="black")
plt.xlim(0, 150)
plt.title("TCGA Breast Mutation Burden")
plt.xlabel("Mutation Count")
plt.ylabel("Number of Samples")
plt.tight_layout()
plt.savefig("../figures/real_breast_histogram.png")
plt.close()

plt.figure()
plt.hist(real_prostate_filtered, bins=30, edgecolor="black")
plt.xlim(0, 150)
plt.title("TCGA Prostate Mutation Burden")
plt.xlabel("Mutation Count")
plt.ylabel("Number of Samples")
plt.tight_layout()
plt.savefig("../figures/real_prostate_histogram.png")
plt.close()

print("Saved in figures/")
