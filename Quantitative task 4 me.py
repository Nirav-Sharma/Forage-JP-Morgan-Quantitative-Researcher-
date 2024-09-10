import pandas as pd
import numpy as np
from math import log

# Load the dataset
df = pd.read_csv('Task 3 and 4_Loan_Data.csv')

# Extract the relevant data
x = df['default'].to_list()  # Default status (binary: 1 = default, 0 = no default)
y = df['fico_score'].to_list()  # FICO scores
n = len(x)
print(f"Number of records: {n}")

# Initialize the default and total arrays for FICO scores (300 to 850)
fico_min = 300
fico_max = 850
score_range = fico_max - fico_min + 1

default = [0] * score_range
total = [0] * score_range

# Fill the default and total arrays
for i in range(n):
    fico_score = int(y[i])
    idx = fico_score - fico_min
    default[idx] += x[i]
    total[idx] += 1

# Calculate cumulative sums for defaults and totals
for i in range(1, score_range):
    default[i] += default[i-1]
    total[i] += total[i-1]

# Log-likelihood function
def log_likelihood(n, k):
    p = k / n
    if p == 0 or p == 1:
        return 0
    return k * log(p) + (n - k) * log(1 - p)

# Parameters for segmentation
r = 10  # Number of segments
dp = [[[-float('inf'), 0] for _ in range(score_range)] for _ in range(r + 1)]

# Dynamic Programming to find the best segmentation
for i in range(r + 1):
    for j in range(score_range):
        if i == 0:
            dp[i][j][0] = 0  # Initialize base case
        else:
            for k in range(j):
                if total[j] == total[k]:
                    continue
                current_ll = log_likelihood(total[j] - total[k], default[j] - default[k])
                if dp[i][j][0] < dp[i - 1][k][0] + current_ll:
                    dp[i][j][0] = dp[i - 1][k][0] + current_ll
                    dp[i][j][1] = k  # Store the split point

# Output the optimal log-likelihood
best_log_likelihood = dp[r][score_range - 1][0]
print(f"Best Log-Likelihood for {r} segments: {round(best_log_likelihood, 4)}")

# Backtrack to find the split points
k = score_range - 1
segments = []
while r > 0:
    segments.append(k + fico_min)
    k = dp[r][k][1]
    r -= 1

segments.reverse()
print("FICO score split points:", segments)
