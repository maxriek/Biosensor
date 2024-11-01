# Python script by Berke Santos and Max Riekeles (developed with the help of AI)

########################################################################################################################
########################################################################################################################

from scipy import stats
import numpy as np

# Given values for four different sets (mean1, mean2, std1, std2, n1, n2 for each set)
means1 = [6.92, 50.53, 0.69, 0.85]
means2 = [6.64, 51.68, 0.71, 0.99]
stds1 = [2.66, 22.42, 0.28, 0.82]
stds2 = [2.64, 24.03, 0.27, 1.03]
n1 = n2 = 9  # Sample size of each group (assumed same for all sets)

# Significance level
alpha = 0.05

# Loop through each set of values
for i in range(len(means1)):
    mean1 = means1[i]
    mean2 = means2[i]
    std1 = stds1[i]
    std2 = stds2[i]

    # Calculate t-value
    t_value = (mean1 - mean2) / np.sqrt((std1 ** 2 / n1) + (std2 ** 2 / n2))

    # Calculate degrees of freedom for Welch's t-test
    df = ((std1 ** 2 / n1 + std2 ** 2 / n2) ** 2) / (
                (std1 ** 2 / n1) ** 2 / (n1 - 1) + (std2 ** 2 / n2) ** 2 / (n2 - 1))

    # Calculate p-value (two-tailed)
    p_value = stats.t.sf(np.abs(t_value), df) * 2

    # Output results for each set
    print(f"Set {i + 1}:")
    print(f"  Mean1 = {mean1}, Mean2 = {mean2}")
    print(f"  Std1 = {std1}, Std2 = {std2}")
    print(f"  T-value: {t_value:.3f}")
    print(f"  P-value: {p_value:.3e}")
    print(f"  Degrees of Freedom (Welch's): {df:.3f}")

    # Determine significance based on p-value and t-value
    if p_value < alpha:
        print(f"  The p-value is less than {alpha}, indicating a statistically significant difference.")
    else:
        print(f"  The p-value is greater than or equal to {alpha}, indicating no statistically significant difference.")

    # Optional rough check on the t-value
    if abs(t_value) > 2:
        print("  The t-value is relatively large, supporting a significant difference.")
    else:
        print("  The t-value is relatively small, suggesting no significant difference.")

    print()  # Blank line for readability between sets
