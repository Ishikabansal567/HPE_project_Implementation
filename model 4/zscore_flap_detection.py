# zscore_flap_detection.py

"""Model 4: Flap Detection using Z-Score"""


import math


def calculate_mean(values):

    return sum(values) / len(values)


def calculate_std(values, mean):

    variance = 0

    for value in values:

        variance += (value - mean) ** 2

    variance = variance / len(values)

    return math.sqrt(variance)


def evaluate_zscore_flap(
    flap_rate_mac,
    global_flap_rates,
    threshold=2.0
):

    mu_flap = calculate_mean(global_flap_rates)

    sigma_flap = calculate_std(
        global_flap_rates,
        mu_flap
    )

    if sigma_flap == 0:

        z_score = 0.0

    else:

        z_score = (
            flap_rate_mac - mu_flap
        ) / sigma_flap

    decision = (
        "BLOCK (Abnormal Activity)"
        if z_score > threshold
        else "ALLOW"
    )

    return {

        "z_score": round(z_score, 4),

        "mean_rate": round(mu_flap, 4),

        "std_dev": round(sigma_flap, 4),

        "decision": decision,
    }


if __name__ == "__main__":

    print("\n--- Testing Model 4 ---")

    global_rates = [1.2, 2.0, 1.5, 0.8, 2.3, 1.1, 14.5]

    stable_node = evaluate_zscore_flap(
        flap_rate_mac=1.5,
        global_flap_rates=global_rates
    )

    print(f"""
Stable Host

Z-Score : {stable_node['z_score']}

Decision : {stable_node['decision']}
""")

    flapping_node = evaluate_zscore_flap(
        flap_rate_mac=14.5,
        global_flap_rates=global_rates
    )

    print(f"""
Flapping Host

Z-Score : {flapping_node['z_score']}

Decision : {flapping_node['decision']}
""")