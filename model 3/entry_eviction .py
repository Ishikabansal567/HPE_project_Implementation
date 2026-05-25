# model3_entry_eviction.py

"""Model 3: Entry Priority Score (Who Gets Evicted First?)"""


def calculate_eviction_priority(
    age,
    ttl_max,
    tx_count,
    flap_count,
    weights=[0.4, 0.3, 0.3]
):
    """
    Computes eviction priority score.
    Higher score = evict this entry first.
    """

    w1, w2, w3 = weights

    term_age = age / ttl_max if ttl_max > 0 else 0

    term_tx = 1 / tx_count if tx_count > 0 else float("inf")

    priority_score = (
        (w1 * term_age)
        + (w2 * term_tx)
        + (w3 * flap_count)
    )

    return round(priority_score, 4)