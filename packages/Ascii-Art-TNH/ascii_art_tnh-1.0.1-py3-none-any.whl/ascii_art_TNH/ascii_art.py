import src.ascii_art_TNH.noises as noises
import src.ascii_art_TNH.gallery as gallery
from .noises import animal_noises #testing this
import random

def ascii_art(user_input):
  # Type of the input-make sure string
  # Strip trailing spaces
  animal_array = parse_input(user_input)
  if random.random() < 0.05:
    print(print_art("cow"))
  if len(animal_array) == 0:
    wrong_input("nothing", 0)
    return
  for animal in animal_array:
    # If animal is in the gallery
    if animal in gallery.animals and animal in noises.animal_noises:
      print(print_art(animal))
      print(get_noise(animal))
    else:
      # If animal is not in the gallery
      print(wrong_input(animal, len(animal_array)))

def parse_input(user_input):
  inputs = []
  inputs = user_input.split(" ")
  clean_input = []
  for input in inputs:
    if input != "" and input.isalpha():
      clean_input.append(input.lower())
  return clean_input

def print_art(animal):
  #match animal with art
  #calls print_noise or wrong_input
  return(gallery.animals.get(animal))


def get_noise(animal):
   #match animal with noise
  return animal_noises.get(animal)

def wrong_input(animals, length):
  #if multiple animals were inputed, print flowers
  #if one animal, print flower
  # reference: https://www.asciiart.eu/plants/flowers
  print("Sorry we do not have art of", ", ".join(animals))
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
  if(length>1):
    return flowers
  elif (length==0):
    return vase
  else:
    return flower
  