import pytest
from src.ascii_art_TNH import ascii_art

def test_one():
    assert ascii_art.print_art("cow") == r"""

\|/          (__)    
     `\------(oo)         moo
       ||    (__)      
       ||w--||     \|/
   \|/


"""


