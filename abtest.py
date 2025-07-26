import numpy as np
from scipy.stats import norm

# --------------------------
# 1. SETUP: Input Parameters (defined BEFORE the test)
# --------------------------

# Assumptions:
baseline_rate = 0.06          # Control (green button) conversion rate
effect_size = 0.02            # Minimum uplift you care about (e.g., +2%)
alpha = 0.05                  # Significance level (one-tailed)
power = 0.8                   # Desired statistical power

# --------------------------
# 2. CALCULATE: Required Sample Size (per group)
# --------------------------

# Convert to z-scores
z_alpha = norm.ppf(1 - alpha)
z_beta = norm.ppf(power)

# Pooled standard deviation estimate
pooled_prob = baseline_rate
std_dev = np.sqrt(2 * pooled_prob * (1 - pooled_prob))

# Sample size formula for two proportions (simplified)
sample_size = ((z_alpha + z_beta) * std_dev / effect_size) ** 2
sample_size = int(np.ceil(sample_size))

# --------------------------
# 3. SIMULATE: Run A/B test with synthetic results
# --------------------------

# Let's say we run the test with this sample size
n_A = sample_size
n_B = sample_size

# Simulated outcomes
conversions_A = int(n_A * baseline_rate)
conversions_B = int(n_B * (baseline_rate + effect_size))

p_A = conversions_A / n_A
p_B = conversions_B / n_B
uplift = p_B - p_A

# --------------------------
# 4. ANALYZE: Z-score, p-value, CI
# --------------------------

# Standard error
SE = np.sqrt((p_A * (1 - p_A)) / n_A + (p_B * (1 - p_B)) / n_B)

# Z-score
z = uplift / SE

# One-tailed p-value (testing if B > A)
p_value = 1 - norm.cdf(z)

# 95% Confidence Interval
z_crit = norm.ppf(0.975)
ci_lower = uplift - z_crit * SE
ci_upper = uplift + z_crit * SE

# --------------------------
# Output
# --------------------------
results = {
    "Required Sample Size per Group": sample_size,
    "Simulated Conversion Rate A (green)": round(p_A, 4),
    "Simulated Conversion Rate B (red)": round(p_B, 4),
    "Observed Uplift (B - A)": round(uplift, 4),
    "Z-score": round(z, 3),
    "P-value (one-tailed)": round(p_value, 4),
    "95% Confidence Interval": [round(ci_lower, 4), round(ci_upper, 4)],
    "Statistically Significant (p < 0.05)?": p_value < 0.05
}

for key, value in results.items():
        print(f"{key}: {value}")