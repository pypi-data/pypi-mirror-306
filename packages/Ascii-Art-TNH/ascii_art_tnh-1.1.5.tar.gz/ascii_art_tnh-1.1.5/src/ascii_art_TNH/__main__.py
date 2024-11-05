from ascii_art import *
def main():
    while(True):
      user_input = input("Enter an animal or 'exit': ")
      if user_input == "exit":
         break
      ascii_art(user_input)

if __name__ == "__main__":
    main()