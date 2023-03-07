from util import Profile, Selector


if __name__ == "__main__":
    answer = input("Do you have an existing profile? Y/N \n")
    if answer.lower() == "y":
        username = input("Enter your username:\n")
        userProfile = Profile.load(username)
    elif answer.lower() == "n":
        username = input("Please enter the username you want to use:\n")
        userProfile = Profile(username)
    print(userProfile.wordLearned)
    lesson = userProfile.get_lesson()
    if lesson == 0:
        print(f"Welcome {username}, would you like to start learning? Y/N")
        answer = input("")
        if answer.lower() == "y":
            Selector.learn(lesson + 1, userProfile)
        elif answer.lower() == "n":
            print("You have not learned any word yet, you cannot revise. Start again when you are ready.")
    elif lesson > 0:
        print(f"Welcome back {username}, would you like to: \n (1) learn new words \n (2) revise the words you have seen in previous lessons \n Enter 1 or 2")
        answer = input("")
        if answer == "1":
            Selector.learn(lesson + 1, userProfile)
        elif answer == "2":
            Selector.revise(userProfile)

    userProfile.save()


    

    # p = pd.read_csv("../media/corpus.csv", delimiter=";", encoding="utf-8")
    # print(p)
    # p['kanji']=p['kanji'].str.split(",")
    # print(p)
    # p['furigana'] = p['furigana'].str.split(",")
    # print(p.iloc[1]['kanji'])

