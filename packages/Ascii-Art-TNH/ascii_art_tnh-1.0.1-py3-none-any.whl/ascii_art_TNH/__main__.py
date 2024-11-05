import src.ascii_art_TNH.ascii_art as art
def main():
    while(True):
      user_input = input("Enter an animal or 'exit': ")
      if user_input == "exit":
         break
      art.ascii_art(user_input)


if __name__ == "__main__":
    main()