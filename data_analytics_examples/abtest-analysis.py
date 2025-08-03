import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

# baseline_rate=0.06: Expected conversion rate of the control group (e.g., 6%)
# effect_size=0.02 Minimum uplift (difference) you want to detect (e.g., +2% improvement)
# alpha=0.05: Significance level: max p-value you accept for "statistical significance" (typically 0.05)
# power=0.8:  Statistical power: probability of detecting a true effect if it exists (typically 0.80 or 80%)

# α (alpha) = probability of a Type I error
# → false positive (rejecting H₀ when it’s actually true)
# → common value: 0.05

# β (beta) = probability of a Type II error
# → false negative (failing to reject H₀ when it’s actually false)

# Power = 1 - \beta
# → probability of correctly detecting a true effect

# beta = 1 - power               # β = 0.20
# z_beta = norm.ppf(1 - beta)    # 1 - 0.20 = 0.80 → z ≈ 0.84

def run_ab_test(baseline_rate=0.06, effect_size=0.02, alpha=0.05, power=0.8):
    # Step 1: Calculate required sample size

    z_alpha = norm.ppf(1 - alpha)
    # z_alpha: z-score corresponding to the chosen significance level (α)
    # For α = 0.05, this gives z ≈ 1.645 (one-tailed), or 1.96 (two-tailed)

    z_beta = norm.ppf(power)
    # z_beta: z-score corresponding to the desired statistical power (1 - β)
    # For power = 0.80, this gives z ≈ 0.84

    pooled_prob = baseline_rate
    # pooled_prob: the expected conversion rate under the null hypothesis (i.e., in control group)

    std_dev = np.sqrt(2 * pooled_prob * (1 - pooled_prob))
    # std_dev: combined standard deviation assuming equal variances in A and B groups
    # Multiplied by 2 because we assume equal sample size and binomial distribution in both groups

    sample_size = int(np.ceil(((z_alpha + z_beta) * std_dev / effect_size) ** 2))
    # sample_size: required number of users in each group (A and B)
    # This formula estimates how many samples are needed to detect the specified effect size
    # with the chosen significance level and statistical power

    # Step 2: Simulate test results
    n_A = n_B = sample_size
    conversions_A = int(n_A * baseline_rate)
    conversions_B = int(n_B * (baseline_rate + effect_size))
    p_A = conversions_A / n_A
    p_B = conversions_B / n_B
    uplift = p_B - p_A

    # Step 3: Statistical analysis

    # SE (Standard Error) of the difference in proportions
    # This quantifies the uncertainty in the estimated difference (uplift)
    # Formula: sqrt( (p1*(1-p1)/n1) + (p2*(1-p2)/n2) )
    SE = np.sqrt((p_A * (1 - p_A)) / n_A + (p_B * (1 - p_B)) / n_B)

    # z-score: standardized value of the observed difference (uplift)
    # This tells us how many standard errors away the observed result is from "no difference"
    z = uplift / SE

    # p-value (one-tailed): probability of observing this z or greater, assuming null hypothesis is true
    # This evaluates whether the observed uplift is statistically significant
    p_value = 1 - norm.cdf(z)  # one-tailed test: testing if B > A

    # z_crit: critical z-value for a 95% confidence interval (two-tailed)
    # 0.975 corresponds to the upper 97.5% cutoff (used to capture middle 95%)
    z_crit = norm.ppf(0.975)

    # Confidence interval: range of plausible values for the true uplift
    # CI = observed uplift ± margin of error
    ci_lower = uplift - z_crit * SE
    ci_upper = uplift + z_crit * SE

    # Decision rule: is the result statistically significant?
    # If p-value < alpha (e.g. 0.05), we reject the null hypothesis
    significant = p_value < alpha

    # Step 4: Visualization
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.hlines(1, ci_lower, ci_upper, colors='blue', linewidth=3, label='95% Confidence Interval')
    ax.plot(uplift, 1, 'o', color='black', label=f'Observed uplift ({uplift*100:.2f}%)')
    ax.axvline(0, color='red', linestyle='--', label='No difference (0%)')
    ax.set_xlim(-0.01, 0.06)
    ax.set_yticks([])
    ax.set_xlabel('Difference in Conversion Rate (B − A)')
    ax.set_title('A/B Test Result: 95% Confidence Interval')
    ax.legend()
    plt.grid(True, axis='x')
    plt.tight_layout()
    plt.show()

    # Step 5: Return results
    results = {
        "Required Sample Size per Group": sample_size,
        "Conversion Rate A (green)": round(p_A, 4),
        "Conversion Rate B (red)": round(p_B, 4),
        "Observed Uplift (B - A)": round(uplift, 4),
        "Z-score": round(z, 3),
        "P-value (one-tailed)": round(p_value, 4),
        "95% Confidence Interval": [round(ci_lower, 4), round(ci_upper, 4)],
        "Statistically Significant (p < α)?": significant
    }

    for key, value in results.items():
        print(f"{key}: {value}")

# Run the function
run_ab_test()