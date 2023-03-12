# -*- coding: utf-8 -*-
import sys
import pygame

from util import Profile, Selector
from util_ui import Controller, SCREEN_HEIGHT, SCREEN_WIDTH


    

if __name__ == "__main__":

    # pygame.init()
    fps = 60
    fpsClock = pygame.time.Clock()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Kanji Cards")

    font = pygame.font.SysFont('Arial', 40)

    screenController = Controller(screen)

    while True:
        screen.fill((202, 228, 241))

        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         sys.exit()

        screenController.handle_events()

        screenController.draw()

        pygame.display.flip()
        fpsClock.tick(fps)


    # answer = input("Do you have an existing profile? Y/N \n")
    # if answer.lower() == "y":
    #     username = input("Enter your username:\n")
    #     userProfile = Profile.load(username)
    # elif answer.lower() == "n":
    #     username = input("Please enter the username you want to use:\n")
    #     userProfile = Profile(username)
    # print(userProfile.wordLearned)
    # lesson = userProfile.get_lesson()
    # if lesson == 0:
    #     print(f"Welcome {username}, would you like to start learning? Y/N")
    #     answer = input("")
    #     if answer.lower() == "y":
    #         Selector.learn(lesson + 1, userProfile)
    #     elif answer.lower() == "n":
    #         print("You have not learned any word yet, you cannot revise. Start again when you are ready.")
    # elif lesson > 0:
    #     print(f"Welcome back {username}, would you like to: \n (1) learn new words \n (2) revise the words you have seen in previous lessons \n Enter 1 or 2")
    #     answer = input("")
    #     if answer == "1":
    #         Selector.learn(lesson + 1, userProfile)
    #     elif answer == "2":
    #         Selector.revise(userProfile)

    # userProfile.save()


    

    # p = pd.read_csv("../media/corpus.csv", delimiter=";", encoding="utf-8")
    # print(p)
    # p['kanji']=p['kanji'].str.split(",")
    # print(p)
    # p['furigana'] = p['furigana'].str.split(",")
    # print(p.iloc[1]['kanji'])

