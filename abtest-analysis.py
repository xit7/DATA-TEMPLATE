import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

def run_ab_test(baseline_rate=0.06, effect_size=0.02, alpha=0.05, power=0.8):
    # Step 1: Calculate required sample size
    z_alpha = norm.ppf(1 - alpha)
    z_beta = norm.ppf(power)
    pooled_prob = baseline_rate
    std_dev = np.sqrt(2 * pooled_prob * (1 - pooled_prob))
    sample_size = int(np.ceil(((z_alpha + z_beta) * std_dev / effect_size) ** 2))

    # Step 2: Simulate test results
    n_A = n_B = sample_size
    conversions_A = int(n_A * baseline_rate)
    conversions_B = int(n_B * (baseline_rate + effect_size))
    p_A = conversions_A / n_A
    p_B = conversions_B / n_B
    uplift = p_B - p_A

    # Step 3: Statistical analysis
    SE = np.sqrt((p_A * (1 - p_A)) / n_A + (p_B * (1 - p_B)) / n_B)
    z = uplift / SE
    p_value = 1 - norm.cdf(z)
    z_crit = norm.ppf(0.975)
    ci_lower = uplift - z_crit * SE
    ci_upper = uplift + z_crit * SE
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