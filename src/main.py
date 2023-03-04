from util import Kanji, Word, Profile

class Selector:
    pass

if __name__ == "__main__":
    answer = input("Do you have an existing profile? Y/N")
    if answer.lower() == "y":
        username = input("Enter your username: ")
        userProfile = Profile.load_profile(username)
    elif answer.lower() == "n":
        input("Please enter the username you want to use: ")
        userProfile = Profile()

