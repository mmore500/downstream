import pytest

from downstream._auxlib._iter_chunks import iter_chunks


@pytest.fixture()
def seq():
    return [1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_chunk_size_one(seq):
    for chunk in iter_chunks(seq, 1):
        assert chunk in [[1], [2], [3], [4], [5], [6], [7], [8], [9]]


def test_chunk_size_two(seq):
    for chunk in iter_chunks(seq, 2):
        assert chunk in [[1, 2], [3, 4], [5, 6], [7, 8], [9]]


def test_chunk_size_greater_than_length(seq):
    for chunk in iter_chunks(seq, 10):
        assert chunk == [1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_empty_sequence():
    assert list(iter_chunks([], 5)) == []


def test_non_list_sequence():
    assert list(iter_chunks("123456", 2)) == ["12", "34", "56"]


def test_chunking_integers():
    input_list = [1, 2, 3, 4, 5, 6]
    chunk_size = 2
    expected_output = [[1, 2], [3, 4], [5, 6]]
    output = list(iter_chunks(input_list, chunk_size))
    assert output == expected_output


def test_chunking_strings():
    input_list = ["apple", "banana", "cherry", "date"]
    chunk_size = 2
    expected_output = [["apple", "banana"], ["cherry", "date"]]
    output = list(iter_chunks(input_list, chunk_size))
    assert output == expected_output


def test_chunk_size_larger_than_input_list():
    input_list = [1, 2, 3, 4]
    chunk_size = 10
    expected_output = [[1, 2, 3, 4]]
    output = list(iter_chunks(input_list, chunk_size))
    assert output == expected_output


def test_chunk_size_larger_than_input_list_with_start():
    input_list = [1, 2, 3, 4]
    chunk_size = 10
    expected_output = [[2, 3, 4]]
    output = list(iter_chunks(input_list, chunk_size, 1))
    assert output == expected_output


def test_chunk_size_equal_to_one():
    input_list = [1, 2, 3, 4]
    chunk_size = 1
    expected_output = [[1], [2], [3], [4]]
    output = list(iter_chunks(input_list, chunk_size))
    assert output == expected_output


def test_start_parameter():
    input_list = [1, 2, 3, 4, 5, 6]
    chunk_size = 2
    start = 2
    expected_output = [[3, 4], [5, 6]]
    output = list(iter_chunks(input_list, chunk_size, start))
    assert output == expected_output


def test_chunk_size_does_not_divide_input_length():
    input_list = [1, 2, 3, 4, 5]
    chunk_size = 2
    expected_output = [
        [1, 2],
        [3, 4],
        [
            5,
        ],
    ]
    output = list(iter_chunks(input_list, chunk_size))
    assert output == expected_output


def test_chunk_size_equal_to_input_length():
    input_list = [1, 2, 3, 4, 5]
    chunk_size = 5
    expected_output = [[1, 2, 3, 4, 5]]
    output = list(iter_chunks(input_list, chunk_size))
    assert output == expected_output


def test_chunk_size_does_not_divide_input_length_with_start():
    input_list = [1, 2, 3, 4, 5]
    chunk_size = 2
    start = 1
    expected_output = [[2, 3], [4, 5]]
    output = list(iter_chunks(input_list, chunk_size, start))
    assert output == expected_output


def test_chunk_size_equal_to_input_length_with_start():
    input_list = [1, 2, 3, 4, 5]
    chunk_size = 5
    start = 1
    expected_output = [[2, 3, 4, 5]]
    output = list(iter_chunks(input_list, chunk_size, start))
    assert output == expected_output


def test_chunk_size_divides_input_length_with_start_2():
    input_list = [1, 2, 3, 4, 5]
    chunk_size = 2
    start = 2
    expected_output = [
        [3, 4],
        [
            5,
        ],
    ]
    output = list(iter_chunks(input_list, chunk_size, start))
    assert output == expected_output


def test_start_equals_length():
    input_list = [1, 2, 3, 4, 5]
    chunk_size = 2
    start = len(input_list)
    expected_output = []
    output = list(iter_chunks(input_list, chunk_size, start))
    assert output == expected_output
