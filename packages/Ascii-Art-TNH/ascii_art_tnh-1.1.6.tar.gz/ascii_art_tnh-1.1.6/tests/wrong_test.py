import pytest
from src.ascii_art_TNH.ascii_art import wrong_input

class Tests:
  def test_wrong_input_multi1(self):
      result = wrong_input("ant bunny",2)
      flowers = r"""
              ,,,                      ,,,
        {{{}}    ,,,             {{{}}    ,,,
      ,,, ~Y~    {{{}},,,      ,,, ~Y~    {{{}},,,
    {{}}} |/,,,  ~Y~{{}}}    {{}}} |/,,,  ~Y~{{}}}
      ~Y~ \|{{}}}/\|/ ~Y~  ,,, ~Y~ \|{{}}}/\|/ ~Y~  ,,,
      \|/ \|/~Y~  \|,,,|/ {{}}}\|/ \|/~Y~  \|,,,|/ {{}}}
      \|/ \|/\|/  \{{{}}/  ~Y~ \|/ \|/\|/  \{{{}}/  ~Y~
      \|/\\|/\|/ \\|~Y~//  \|/ \|/\\|/\|/ \\|~Y~//  \|/
      \|//\|/\|/,\\|/|/|// \|/ \|//\|/\|/,\\|/|/|// \|/
  jgs^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  """
      assert result.strip() == flowers.strip()
  def test_wrong_input_nothing(self):
      result = wrong_input("noting", 0)
      vase = r"""
          *
      *  *r*  *
    * *a* ^Y^ *i* *
  *m*^Y^*^\^*^Y^*s*
  ^Y^*\*e*/*l*/*^Y^
  *\*t*|Y^\^Y|*l*/*
  *s*|Y^\\^/^//^Y|*a*
  ^Y^\\_^\\\//^_//^Y^
  ^\_^\_\_\//_/_/^_/^
  ^^\_^\_\\/_/^_/^^
    ^^\_ \// _/^^
        \_\_/
          /|\
        /\\/\
  """
      assert result.strip() == vase.strip()
  def test_wrong_input_single1(self):
     result = wrong_input("sheep", 1)
     flower = r""" 
                .-.'  '.-.
            .-(   \  /   )-.
          /   '..oOOo..'   \
  ,       \.--.oOOOOOOo.--./
  |\  ,   (   :oOOOOOOo:   )
  _\.\/|   /'--'oOOOOOOo'--'\
  '-.. ;/| \   .''oOOo''.   /
  .--`'. :/|'-(   /  \   )-'
  '--. `. / //'-'.__.'-;
    `'-,_';//      ,  /|
          '((       |\/./_
            \\  . |\; ..-'
            \\ |\: .'`--.
              \\, .' .--'
              ))'_,-'`
        jgs  //-'
            // 
            //
          |/
    """
     assert result.strip() == flower.strip()
  def test_wrong_input_single2(self):
     result = wrong_input("nonexistent", 1)
     flower = r""" 
                .-.'  '.-.
            .-(   \  /   )-.
          /   '..oOOo..'   \
  ,       \.--.oOOOOOOo.--./
  |\  ,   (   :oOOOOOOo:   )
  _\.\/|   /'--'oOOOOOOo'--'\
  '-.. ;/| \   .''oOOo''.   /
  .--`'. :/|'-(   /  \   )-'
  '--. `. / //'-'.__.'-;
    `'-,_';//      ,  /|
          '((       |\/./_
            \\  . |\; ..-'
            \\ |\: .'`--.
              \\, .' .--'
              ))'_,-'`
        jgs  //-'
            // 
            //
          |/
    """
     assert result.strip() == flower.strip()