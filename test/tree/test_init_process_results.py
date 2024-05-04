"""Testing the Tree Init Module 
"""
from tree import process_results


def test_process_results_empty_tuple_retuns():
    input_tuple = tuple()
    result_str = process_results(input_tuple)
    assert result_str == 'No operations ran.'


def test_process_results_two_succeeded_returns_success_message():
    input_tuple = (True, True)
    result_str = process_results(input_tuple)
    assert result_str == 'All 2 operations succeeded.'


def test_process_results_two_failed_returns_failed_message():
    input_tuple = (False, False)
    result_str = process_results(input_tuple)
    assert result_str == 'All 2 operations failed.'


def test_process_results_half_succeeded_returns_message():
    input_tuple = (True, False)
    result_str = process_results(input_tuple)
    assert result_str == '1 out of 2 operations succeeded: 50.0%'
