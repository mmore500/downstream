import pandas as pd

from hsurf.pylib import hanoi
from hsurf.site_selection_strategy.site_selection_algorithms.tilted_hadamard_order_site_rungs_algo._impl import (
    get_num_reservations_provided,
    get_surface_rank_capacity,
)


# helper for get_reservation_index_elimination_rank test
def make_num_reservations_provided_df(surface_size: int) -> pd.DataFrame:
    num_generations = min(
        2**12,
        get_surface_rank_capacity(surface_size) - 1,
    )
    records = []
    max_hanoi_value = hanoi.get_max_hanoi_value_through_index(
        num_generations - 1
    )
    for hanoi_value in range(max_hanoi_value):
        first_incidence_rank = hanoi.get_index_of_hanoi_value_nth_incidence(
            hanoi_value, 0
        )
        for rank in range(first_incidence_rank, num_generations):
            num_reservations_provided = get_num_reservations_provided(
                hanoi_value=hanoi_value,
                surface_size=surface_size,
                rank=rank,
            )
            incidence_count = (
                hanoi.get_incidence_count_of_hanoi_value_through_index(
                    hanoi_value,
                    rank,
                )
            )
            assert incidence_count
            records.append(
                {
                    "rank": rank,
                    "hanoi value": hanoi_value,
                    "hanoi incidence": incidence_count - 1,
                    "num reservations provided": num_reservations_provided,
                }
            )

    return pd.DataFrame.from_records(records)
