import pytest
from src.ascii_art_TNH import ascii_art

def test_one():
    assert ascii_art.print_art("cow") == r"""

\|/          (__)    
     `\------(oo)
       ||    (__)      
       ||w--||     \|/
   \|/


"""

def test_two():
    assert ascii_art.print_art("dog") == r"""

     |\_/|                  
     | @ @
     |   <>              _  
     |  _/\------____ ((| |))
     |               `--' |   
 ____|_       ___|   |___.' 
/_/_____/____/_______|


"""

def test_three():
    assert ascii_art.print_art("frog") == r"""

           .--._.--.
          ( O     O )
          /   . .   \
         .`._______.'.
        /(           )\
      _/  \  \   /  /  \_
   .~   `  \  \ /  /  '   ~.
  {    -.   \  V  /   .-    }
_ _`.    \  |  |  |  /    .'_ _
>_       _} |  |  | {_       _<
 /. - ~ ,_-'  .^.  `-_, ~ - .\
         '-'|/   \|`-`


"""


