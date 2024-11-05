import pytest
from src.ascii_art_TNH.ascii_art import parse_input

def test_parse_input_single_word():
    user_input = "cat"
    expected_output = ["cat"]
    assert parse_input(user_input) == expected_output

def test_parse_input_multiple_words():
    user_input = "cat dog"
    expected_output = ["cat", "dog"]
    assert parse_input(user_input) == expected_output

def test_parse_input_trailing_spaces():
    user_input = "  cat  dog  "
    expected_output = ["cat", "dog"]
    assert parse_input(user_input) == expected_output

def test_parse_input_empty_string():
    user_input = ""
    expected_output = []
    assert parse_input(user_input) == expected_output

def test_parse_input_only_spaces():
    user_input = "     "
    expected_output = []
    assert parse_input(user_input) == expected_output