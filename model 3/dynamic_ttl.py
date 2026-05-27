# dynamic_ttl.py

"""
Dynamic TTL Model
"""


def calculate_dynamic_ttl(
    tx_count,
    flap_count,
    occupied
):
    """
    Dynamic TTL calculation.

    Higher TX count -> larger TTL
    Higher flap count -> lower TTL
    Higher occupancy -> lower TTL
    """

    base_ttl = 300

    tx_bonus = tx_count * 5

    flap_penalty = flap_count * 20

    occupancy_penalty = occupied * 10

    ttl = (
        base_ttl
        + tx_bonus
        - flap_penalty
        - occupancy_penalty
    )

    ttl = max(30, min(ttl, 600))

    return ttl