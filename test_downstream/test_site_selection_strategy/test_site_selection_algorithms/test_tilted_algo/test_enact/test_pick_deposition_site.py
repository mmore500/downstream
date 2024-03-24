import pytest

from downstream.pylib import hanoi
from downstream.pylib.site_selection_eval import make_surface_history_df
from downstream.site_selection_strategy.site_selection_algorithms.tilted_algo import (
    pick_deposition_site,
)
from downstream.site_selection_strategy.site_selection_algorithms.tilted_algo._impl import (
    get_hanoi_num_reservations,
)

expected8 = [
    0,  # 0:0
    1,  # 1:1
    5,  # 2:0
    2,  # 3:2
    4,  # 4:0
    6,  # 5:1
    7,  # 6:0
    3,  # 7:3
    0,  # 8:0
    1,  # 9:1
    5,  # 10:0
    7,  # 11:2
    0,  # 12:0
    6,  # 13:1
    5,  # 14:0
    4,  # 15:4
    0,  # 16:0
    1,  # 17:1
    0,  # 18:0
    2,  # 19:2
    0,  # 20:0
    6,  # 21:1
    0,  # 22:0
    3,  # 23:3
    0,  # 24:0
    1,  # 25:1
    0,  # 26:0
    7,  # 27:2
    0,  # 28:0
    6,  # 29:1
    0,  # 30:0
    5,  # 31:5
    0,  # 32:0
    1,  # 33
    0,  # 34
    2,  # 35
    0,  # 36
    1,  # 37
    0,  # 38
    3,  # 39
    0,  # 40
    1,  # 41
    0,  # 42
    7,  # 43
    0,  # 44
    1,  # 45
    0,  # 46
    4,  # 47
    0,  # 48
    1,  # 49
    0,  # 50
    2,  # 51
    0,  # 52
    1,  # 53
    0,  # 54
    3,  # 55
    0,  # 56
    1,  # 57
    0,  # 58
    7,  # 59
    0,  # 60
    1,  # 61
    0,  # 62
    6,  # 63
    0,  # 64
    1,  # 65
    0,  # 66
    2,  # 67
    0,  # 68
    1,  # 69
    0,  # 70
    3,  # 71
    0,  # 72
    1,  # 73
    0,  # 74
    2,  # 75
    0,  # 76
    1,  # 77
    0,  # 78
    4,  # 79
    0,  # 80
    1,  # 81
    0,  # 82
    2,  # 83
    0,  # 84
    1,  # 85
    0,  # 86
    3,  # 87
    0,  # 88
    1,  # 89
    0,  # 90
    2,  # 91
    0,  # 92
    1,  # 93
    0,  # 94
    5,  # 95
    0,  # 96
    1,  # 97
    0,  # 98
    2,  # 99
    0,  # 100
    1,  # 101
    0,  # 102
    3,  # 103
    0,  # 104
    1,  # 105
    0,  # 106
    2,  # 107
    0,  # 108
    1,  # 109
    0,  # 110
    4,  # 111
    0,  # 112
    1,  # 113
    0,  # 114
    2,  # 115
    0,  # 116
    1,  # 117
    0,  # 118
    3,  # 119
    0,  # 120
    1,  # 121
    0,  # 122
    2,  # 123
    0,  # 124
    1,  # 125
    0,  # 126
    7,  # 127
    0,  # 128
]


def test_pick_deposition_site8():
    surface_size = 8
    for rank in range(len(expected8)):
        assert pick_deposition_site(rank, surface_size) == expected8[rank]


expected16 = [
    0,  # 0:0
    1,  # 1:1
    9,  # 2:0
    2,  # 3:2
    6,  # 4:0
    10,  # 5:1
    13,  # 6:0
    3,  # 7:3
    5,  # 8:0
    7,  # 9:1
    8,  # 10:0
    11,  # 11:2
    12,  # 12:0
    14,  # 13:1
    15,  # 14:0
    4,  # 15:4
    0,  # 16:0
    1,  # 17:1
    9,  # 18:0
    8,  # 19:2
    6,  # 20:0
    10,  # 21:1
    13,  # 22:0
    12,  # 23:3
    0,  # 24:0
    7,  # 25:1
    9,  # 26:0
    15,  # 27:2
    6,  # 28:0
    14,  # 29:1
    13,  # 30:0
    5,  # 31:5
    0,  # 32:0
    1,  # 33:1
    9,  # 34:2
    2,  # 34:2
]


def test_pick_deposition_site16():
    surface_size = 16
    for rank in range(len(expected16)):
        assert pick_deposition_site(rank, surface_size) == expected16[rank]


@pytest.mark.parametrize(
    "surface_size, num_generations",
    [
        (8, 255),
        (16, 2**12),
        (32, 2**12),
        (64, 2**12),
    ],
)
def test_layering(surface_size: int, num_generations: int):
    df = make_surface_history_df(
        pick_deposition_site, surface_size, num_generations
    )

    for (hanoi_value, rank), group in df.groupby(
        [
            "hanoi value",
            "rank",
        ],
    ):
        hanoi_value, rank = int(hanoi_value), int(rank)  # native python ints
        if rank == -1:
            continue
        if hanoi_value == -1:
            continue
        assert hanoi_value >= 0 and rank >= 0

        count = hanoi.get_incidence_count_of_hanoi_value_through_index(
            hanoi_value, rank
        )
        assert count >= 1
        num_reservations = min(
            get_hanoi_num_reservations(rank + 1, surface_size),
            get_hanoi_num_reservations(rank, surface_size),
        )
        assert num_reservations >= 1
        target_count = min(count, num_reservations)
        # should have expected hanoi population
        assert (
            len(group) >= target_count
        )  # may be larger if not yet eliminated

        incidences = {
            hanoi.get_hanoi_value_incidence_at_index(rank)
            for rank in group["deposition rank"]
        }
        # should always have top half of incidences
        for i in range((len(incidences) + 1) // 2):
            lookup = count - i - 1
            assert lookup >= 0
            assert lookup in incidences
