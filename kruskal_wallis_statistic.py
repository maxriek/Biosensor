# Authors: Max Riekeles, Berke Santos, Nicholas Adams
# Script developed with the help of AI (Perplexity.AI) for the Kruskal-Wallis H Test
# Last Update: 01 December 2024

from scipy import stats

def kruskal_wallis_test(samples):
    """Perform Kruskal-Wallis H Test on multiple independent samples."""
    stat, p_value = stats.kruskal(*samples)
    return stat, p_value

def main():
    # Example data: replace these with your actual counts at different time points
    sample_1 = [17.14285714, 24, 24, 7.058823529, 7, 12, 9, 11, 17.14285714]
    # Control 0.1 h
    sample_2 = [12.97297297, 13.51351351, 13.71428571, 12.77777778, 11.42857143, 15.42857143, 17.2972973]
    # Control 1 h
    sample_3 = [11.25, 11.4893617, 10.86956522, 8.62745098, 12, 11.11111111, 17.54385965, 17.77777778, 16.36363636]
    # Control 4 h
    sample_4 = [10.28571429, 8.571428571, 8.333333333, 4.528301887, 5.384615385, 6, 7.450980392, 5.714285714, 4, 4.705882353]
    # Control 24 h
    sample_5 = [18.0952381, 19, 21.9047619, 17.14285714, 16.15384615, 20.71428571, 16, 12.30769231, 12]
    # 100 mg/L 0.1 h
    sample_6 = [9.433962264, 9.230769231, 8.518518519, 12.94117647, 11.17647059, 12.43243243, 4.571428571, 6.285714286, 6.857142857]
    # 100 mg/L 1 h
    sample_7 = [7.692307692, 8, 10, 13, 13.5, 15.6097561, 9.565217391, 9.565217391, 11.91489362]
    # 100 mg/L 4 h
    sample_8 = [3.333333333, 3.272727273, 1.454545455, 2.413793103, 2.75862069, 3.728813559, 5, 6.12244898, 6.666666667, 8.235294118, 6.060606061, 5.454545455]
    # 100 mg/L 24 h
    sample_9 = [6.666666667, 16, 8, 23.80952381, 9.333333333, 23.80952381, 12, 13.33333333, 10.66666667, 9, 11.57894737, 7, 9.523809524, 12.38095238, 10.90909091]
    # 200 mg/L 0.1 h
    sample_10 = [10, 13, 15.78947368, 12.57142857, 12.72727273, 8, 20.42553191, 17.27272727, 16.17021277, 15.83333333]
    # 200 mg/L 1 h
    sample_11 = [13.77777778, 10.45454545, 7.272727273, 7.272727273, 9.696969697, 8.484848485, 8.235294118, 10.96774194, 12.5, 10.34482759, 10.66666667]
    # 200 mg/L 4 h
    sample_12 = [3.448275862, 2.857142857, 6.666666667, 6.451612903, 5.185185185, 4, 6.101694915, 6.666666667, 4.745762712, 5.128205128, 5.974025974, 8.35443038]
    # 200 mg/L 24 h

    # Perform Kruskal-Wallis H Test on different number of sample groups (minimum: 2)
    print("Kruskal-Wallis H Test for all samples:")
    h_stat, p_value_kw = kruskal_wallis_test([sample_8,sample_12])
    #kruskal_wallis_test([sample_1,sample_2,sample_3,sample_4,sample_5,sample_6,sample_7,sample_8,sample_9,sample_10,sample_11,sample_12])
    print(f"H-statistic: {h_stat}, P-value: {p_value_kw}")

if __name__ == "__main__":
    main()
