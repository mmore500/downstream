from .....pylib import hanoi


def get_surface_rank_capacity(surface_size: int) -> int:
    """For how many depositions is the site selection algorithm defined for a
    surface with `surface_size`?

    At the returned rank, calls to this site selection algorithm are invalid
    and should be refused. Generational depth of experiments should be kept
    below this threshold, or alternate continuation arrangements will need to
    be made (outside the scope of the algorithm).
    """
    return hanoi.get_index_of_hanoi_value_nth_incidence(surface_size, 0)
