import numpy as np
import sys

file_path = sys.argv[1]

data = np.loadtxt(file_path)

print("Variance:", np.var(data))
print("Standard Deviation:", np.std(data))
