import pytest
from src.ascii_art_TNH.ascii_art import get_noise
from src.ascii_art_TNH.noises import animal_noises

class TestNoises: 
    #Fixtures
    @pytest.fixture
    def setup_animal_noises(self):
        """
        A fixture to set up the dictionary of expected animals noises to compare against 'get_noise'.
        """
        noises = animal_noises
        yield animal_noises

    def test_sanity_check(self, setup_animal_noises):
        """
        Sanity check to ensure fixture is set up correctly and that `get_noise` is callable.
        """
        assert setup_animal_noises, "Expected setup_animal_noises to be a non-empty dictionary"
        assert callable(get_noise), "Expected `get_noise` to be a callable function"

    def test_get_noise_valid(self, setup_animal_noises):
        """
        Test that `get_noise` returns the correct animal name for known sounds.
        """
        for sound, expected_animal in setup_animal_noises.items():
            actual = get_noise(sound)
            assert actual == expected_animal, f"Expected `get_noise('{sound}')` to return '{expected_animal}', but got '{actual}'"

    def test_get_noise_invalid(self):
        """
        Test that `get_noise` returns None or an appropriate value for unknown sounds.
        """
        unknown_sounds = ["bark", "woooo", "baaah", "unknown"]
        for sound in unknown_sounds:
            actual = get_noise(sound)
            assert actual is None, f"Expected `get_noise('{sound}')` to return None, but got '{actual}'"
    
    def test_content(self, setup_animal_noises):
        """
        Verify that the sound returned by `get_noise` is part of the predefined noises dictionary.
        """
        for sound in setup_animal_noises.keys():
            actual = get_noise(sound)
            assert actual in setup_animal_noises.values(), f"Expected '{actual}' to be in the animal noises dictionary but got '{actual}'"


        