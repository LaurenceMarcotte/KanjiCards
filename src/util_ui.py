# -*- coding: utf-8 -*-
from typing import Callable, Tuple, Iterator
import sys
import re

from util import Profile, Selector

import pygame
from pygame_textinput.textinput import TextInput

pygame.init()

SCREEN_HEIGHT = 640
SCREEN_WIDTH = 600
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT_INPUT_BOX = pygame.font.Font(None, 32)
SMALL_FONT = pygame.font.SysFont('Arial', 20)
BIG_FONT = pygame.font.SysFont('Arial', 40)
KANJI_FONT = pygame.font.Font("./media/Cyberbit.ttf", 80)
KANA_FONT = pygame.font.Font("./media/Cyberbit.ttf", 40)
KANA_FONT_INPUT = pygame.font.Font("./media/Cyberbit.ttf", 32)
SMALL_KANA = pygame.font.Font("./media/Cyberbit.ttf", 20)


class Button:
    def __init__(self, x: int, y: int, size: Tuple[int], buttonText: str, font, onClickFunction: Callable = None) -> None:
        self.x = x
        self.y = y
        self.width = size[0]
        self.height = size[1]
        self.buttonText = buttonText
        self.clicked = False

        self.onClickFunction = onClickFunction

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

        self.alreadyPressed = False

    def process(self, screen):
        mousePos = pygame.mouse.get_pos()
        
        self.change_color("normal")
        if self.buttonRect.collidepoint(mousePos):
            self.change_color("hover")

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.change_color("pressed")
                if not self.alreadyPressed:
                    self.onClickFunction()
                    self.alreadyPressed = True
            else: 
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)

    def change_color(self, state):
        self.buttonSurface.fill(self.fillColors[state])


# Taken from https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame
# Credits to skrx (first answer)
class InputBox:
    def __init__(self, x, y, w, h, font, text="") -> None:
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.textInput = TextInput(font, self.color)
        self.active = False

    def update(self, events):
        if self.active:
            self.textInput.update(events)

    def draw(self, screen):
        # Blit the text.
        textSurf = self.textInput.get_surface()
        screen.blit(textSurf, (self.rect.x+5, self.rect.y + self.rect.height//2 - textSurf.get_rect().height/2-2))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
            self.textInput.font_color = self.color

    def get_text(self):
        return self.textInput.input_text.replace("|", "")

    # def __init__(self, x, y, w, h, text=''):
    #     self.rect = pygame.Rect(x, y, w, h)
    #     self.color = COLOR_INACTIVE
    #     self.text = text
    #     self.txt_surface = FONT_INPUT_BOX.render(text, True, self.color)
    #     self.active = False

    # def handle_event(self, event):
    #     if event.type == pygame.MOUSEBUTTONDOWN:
    #         # If the user clicked on the input_box rect.
    #         if self.rect.collidepoint(event.pos):
    #             # Toggle the active variable.
    #             self.active = not self.active
    #         else:
    #             self.active = False
    #         # Change the current color of the input box.
    #         self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
    #     if event.type == pygame.KEYDOWN:
    #         if self.active:
    #             if event.key == pygame.K_RETURN:
    #                 return
    #             #     print(self.text)
    #             #     self.text = ''
    #             elif event.key == pygame.K_BACKSPACE:
    #                 self.text = self.text[:-1]
    #             else:
    #                 self.text += event.unicode
    #             # Re-render the text.
    #             self.txt_surface = FONT_INPUT_BOX.render(self.text, True, self.color)
        
    # def update(self):
    #     # Resize the box if the text is too long.
    #     width = max(200, self.txt_surface.get_width()+10)
    #     self.rect.w = width

    # def draw(self, screen):
    #     # Blit the text.
    #     screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y + self.rect.height/2 - 10))
    #     # Blit the rect.
    #     pygame.draw.rect(screen, self.color, self.rect, 2)

    # def reset_text(self):
    #     self.text = ""
    #     self.txt_surface = FONT_INPUT_BOX.render(self.text, True, self.color)



class Controller:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.screenPage = "menu"
        self.create_pages = {"menu": self.create_menu_objects, "signIn": self.create_signIn_objects, 
                             "signUp": self.create_signUp_objects, "profile": self.create_profile_objects,
                             "learn": self.create_learn_objects, "revise": self.create_revise_objects}
        self.page_objects = {"text": [], "button": [], "inputbox": []}
        self.change_page("menu")
        self.userProfile = None

    def reset_page(self):
        self.page_objects = {"text": [], "button": [], "inputbox": []}

    def change_page(self, newPage: str):
        pygame.time.delay(100)
        self.screenPage = newPage
        self.create_pages[newPage]()

    def signIn(self, username: str = None):
        if username is None:
            input_box = self.page_objects["inputbox"][0]
            username = input_box.get_text()
        print(username)
        if Profile.exists(username):
            self.userProfile = Profile.load(username)
            self.change_page("profile")
        else:
            error = SMALL_FONT.render(f"Error: This username {username} does not exist. Please check the spelling.", True, (255, 0, 0))
            self.page_objects["text"].append((error, [SCREEN_WIDTH/2 - error.get_rect().width/2, 400]))
            # input_box.reset_text()

    def signUp(self, username: str = None):
        if username is None:
            input_box = self.page_objects["inputbox"][0]
            username = input_box.get_text()

        if Profile.exists(username):
            error = SMALL_FONT.render(f"The username [{username}] already exists. Please user another one.", True, (255, 0, 0))
            self.page_objects["text"].append((error, [SCREEN_WIDTH/2 - error.get_rect().width/2, 400]))
            # input_box.reset_text()
        else:
            self.userProfile = Profile(username)
            self.change_page("profile")

    def create_menu_objects(self):
        self.reset_page()
        text = BIG_FONT.render("Kanji Cards", True, (20, 20, 20))
        buttonwidth = 120
        buttonSignIn = Button(SCREEN_WIDTH/2 - buttonwidth/2, 280, (buttonwidth, 80), "Sign In", BIG_FONT, lambda : self.change_page("signIn"))
        buttonSignUp = Button(SCREEN_WIDTH/2 - buttonwidth/2, 400, (buttonwidth, 80), "Sign Up", BIG_FONT, lambda : self.change_page("signUp"))
        
        textFirstTime = SMALL_FONT.render("First time?", True, (20,20,20))

        self.page_objects["text"] = [(text, [SCREEN_WIDTH/2 - text.get_rect().width/2, 100]), (textFirstTime, [SCREEN_WIDTH/2 - textFirstTime.get_rect().width/2, 375])]
        self.page_objects["button"] = [buttonSignIn, buttonSignUp]
        # self.page_objects = [text, buttonSignIn, textFirstTime, buttonSignUp]

    def create_signIn_objects(self):
        self.reset_page()
        text = BIG_FONT.render("Kanji Cards", True, (20, 20, 20))
        text_username = SMALL_FONT.render("Username:", True, (20,20,20))
        iwidth = 200
        input_box = InputBox(SCREEN_WIDTH/2 - iwidth/2, 280, iwidth, 45, FONT_INPUT_BOX)
        buttonwidth = 100
        buttonSignIn = Button(SCREEN_WIDTH/2 - buttonwidth/2, 340, (buttonwidth, 40), "Log in", SMALL_FONT, self.signIn)

        self.page_objects["text"] = [(text, [SCREEN_WIDTH/2 - text.get_rect().width/2, 100]), (text_username, [SCREEN_WIDTH/2 - text_username.get_rect().width/2, 255])]
        self.page_objects["button"] = [buttonSignIn]
        self.page_objects["inputbox"] = [input_box]
        # self.page_objects = [self.page_objects[0], text_username, input_box, buttonSignIn]  

    def create_signUp_objects(self):
        self.reset_page()
        text = BIG_FONT.render("Kanji Cards", True, (20, 20, 20))
        text_username = SMALL_FONT.render("Username:", True, (20,20,20))
        iwidth = 200
        input_box = InputBox(SCREEN_WIDTH/2 - iwidth/2, 280, iwidth, 45, FONT_INPUT_BOX)
        buttonwidth = 100
        buttonSignIn = Button(SCREEN_WIDTH/2 - buttonwidth/2, 340, (buttonwidth, 40), "Create profile", SMALL_FONT, self.signUp)
        self.page_objects["text"] = [(text, [SCREEN_WIDTH/2 - text.get_rect().width/2, 100]), (text_username, [SCREEN_WIDTH/2 - text_username.get_rect().width/2, 255])]
        self.page_objects["button"] = [buttonSignIn]
        self.page_objects["inputbox"] = [input_box]
    
    def create_profile_objects(self):
        self.reset_page()
        username = BIG_FONT.render(self.userProfile.username, True, (20, 20, 20))
        usernamePos = [20, 20]

        lesson = SMALL_FONT.render(f"You have completed lesson {self.userProfile.get_lesson()}.", True, (20, 20, 20))
        lessonPos = [SCREEN_WIDTH/2 - lesson.get_rect().width/2, 150]

        self.page_objects["text"] = [(username, usernamePos), (lesson, lessonPos)]
        buttonwidth = 200
        buttonLearn = Button(SCREEN_WIDTH/2 - buttonwidth/2, 280, (buttonwidth, 40), "Learn new kanji", SMALL_FONT, lambda : self.change_page("learn"))
        buttonwidth = 250
        buttonRevise = Button(SCREEN_WIDTH/2 - buttonwidth/2, 380, (buttonwidth, 40), "Review what you've learned", SMALL_FONT, lambda: self.revise())

        self.page_objects["button"] = [buttonLearn, buttonRevise]

    def revise(self):
        if self.userProfile.get_lesson() == 0:
            error = SMALL_FONT.render("You cannot revise yet as you have not learned any word.", True, (255, 0, 0))
            self.page_objects["text"].append((error, [SCREEN_WIDTH/2 - error.get_rect().width/2, 430]))
        else:
            self.change_page("revise")

    def create_revise_objects(self):
        self.reset_page()
        iter_words = Selector.revise(self.userProfile)
        id, word, kanji, furigana, french, choice = next(iter_words)
        texts = {"fr": [french, "Enter the word in kanji:", "Enter the word in kana:"], 
                 "furi": [furigana, "Enter the word in kanji:", "Enter the word in french:"],
                 "jp": [kanji, "Enter the word in kana:", "Enter the word in french:"]}
        text1 = KANA_FONT.render(texts[choice][0], True, (20, 20, 20))
        text1Pos = [SCREEN_WIDTH/2 - text1.get_rect().width/2, 100]
        text2 = SMALL_FONT.render(texts[choice][1], True, (20, 20, 20))
        text2Pos = [SCREEN_WIDTH/2 - text2.get_rect().width/2, 160]
        text3 = SMALL_FONT.render(texts[choice][2], True, (20, 20, 20))
        text3Pos = [SCREEN_WIDTH/2 -text3.get_rect().width/2, 255]
        self.page_objects["text"] = [(text1, text1Pos), (text2, text2Pos), (text3, text3Pos)]

        iwidth = 200
        input1 = InputBox(SCREEN_WIDTH/2 - iwidth/2, 190, iwidth, 45, KANA_FONT_INPUT)
        input2 = InputBox(SCREEN_WIDTH/2 - iwidth/2, 285, iwidth, 45, KANA_FONT_INPUT)
        self.page_objects["inputbox"] = [input1, input2]
        
        buttonwidth = 200
        button = Button(SCREEN_WIDTH/2 - buttonwidth/2, 420, (buttonwidth, 40), "Verify", SMALL_FONT, lambda : self.verify(id, word, kanji, furigana, french, choice, iter_words))
        self.page_objects["button"] = [button]

    def verify(self, id, word, kanji, furigana, french, choice, iterator):
        answer1 = self.page_objects["inputbox"][0].get_text()
        answer2 = self.page_objects["inputbox"][1].get_text()
        print(answer1)
        print(answer2)
        print(id)
        correct = False
        if choice == "fr":
            if (answer1 == kanji or answer1 == "".join(word)) and answer2 == furigana:
                correct = True
        elif choice == "furi":
            if (answer1 == kanji or answer1 == "".join(word)) and answer2.lower() in french.lower().split("|"):
                correct = True
        elif choice == "jp":
            if answer1 == furigana and answer2.lower() in french.lower().split("|"):
                correct = True
        if correct:
            error = BIG_FONT.render("Correct!", True, (0, 255, 0))
            self.page_objects["text"].append((error, [SCREEN_WIDTH/2 - error.get_rect().width/2, 420]))
            self.userProfile.revise_word(id, self.userProfile.get_box_word(id) + 1)
        else:
            error = SMALL_FONT.render("Wrong!\n The correct answer is:", True, (255, 0, 0))
            self.page_objects["text"].append((error, [SCREEN_WIDTH/2 - error.get_rect().width/2, 420]))
            true_answer = SMALL_KANA.render(kanji + "\n" + furigana + "\n" + french, True, (20, 20, 20))
            self.page_objects["text"].append((true_answer, [SCREEN_WIDTH/2 - true_answer.get_rect().width/2, 465]))
            self.userProfile.revise_word(id, self.userProfile.get_box_word(id) - 1)
        buttonwidth = 200
        button = Button(SCREEN_WIDTH/2 - buttonwidth/2, 540, (buttonwidth, 40), "Next", SMALL_FONT, lambda : self.revise_next_word(iterator))
        self.page_objects["button"] = [button]

    def revise_next_word(self, iterator: Iterator):
        id, word, kanji, furigana, french, choice = next(iterator)
        texts = {"fr": [french, "Enter the word in kanji:", "Enter the word in kana:"], 
                 "furi": [furigana, "Enter the word in kanji:", "Enter the word in french:"],
                 "jp": [kanji, "Enter the word in kana:", "Enter the word in french:"]}
        text1 = KANA_FONT.render(texts[choice][0], True, (20, 20, 20))
        text1Pos = [SCREEN_WIDTH/2 - text1.get_rect().width/2, 100]
        text2 = SMALL_FONT.render(texts[choice][1], True, (20, 20, 20))
        text2Pos = [SCREEN_WIDTH/2 - text2.get_rect().width/2, 160]
        text3 = SMALL_FONT.render(texts[choice][2], True, (20, 20, 20))
        text3Pos = [SCREEN_WIDTH/2 -text3.get_rect().width/2, 255]
        self.page_objects["text"] = [(text1, text1Pos), (text2, text2Pos), (text3, text3Pos)]

        iwidth = 200
        input1 = InputBox(SCREEN_WIDTH/2 - iwidth/2, 190, iwidth, 45, KANA_FONT_INPUT)
        input2 = InputBox(SCREEN_WIDTH/2 - iwidth/2, 285, iwidth, 45, KANA_FONT_INPUT)
        self.page_objects["inputbox"] = [input1, input2]
        
        buttonwidth = 200
        button = Button(SCREEN_WIDTH/2 - buttonwidth/2, 420, (buttonwidth, 40), "Verify", SMALL_FONT, lambda : self.verify(id, word, kanji, furigana, french, choice, iterator))
        self.page_objects["button"] = [button]


    def learn_next_word(self, iterator: Iterator):
        try:
            kanji, furigana, french = next(iterator)
            kanjiText = KANJI_FONT.render(kanji, True, (20, 20, 20))
            kanjiPos = [SCREEN_WIDTH/2 - kanjiText.get_rect().width/2, 100]
            furiganaText = KANJI_FONT.render(furigana, True, (20, 20, 20))
            furiganaPos = [SCREEN_WIDTH/2 - furiganaText.get_rect().width/2, 200]
            frenchText = KANJI_FONT.render(french, True, (20, 20, 20))
            frenchPos = [SCREEN_WIDTH/2 - frenchText.get_rect().width/2, 280]
            self.page_objects["text"] = [(kanjiText, kanjiPos), (furiganaText, furiganaPos), (frenchText, frenchPos)]
        except StopIteration:
            text = BIG_FONT.render("Congrats!", True, (20, 20, 20))
            text2 = SMALL_FONT.render("You have learned all the words in this lesson.", True, (20, 20, 20))
            self.page_objects["text"] = [(text, [SCREEN_WIDTH/2 - text.get_rect().width/2, 100]), (text2, [SCREEN_WIDTH/2 - text2.get_rect().width/2, 200])]
            buttonwidth = 250
            newbutton = Button(SCREEN_WIDTH/2 - buttonwidth/2, 380, (buttonwidth, 40), "Go back to profile", SMALL_FONT, lambda: self.change_page("profile"))
            self.page_objects["button"] = [newbutton]

    def create_learn_objects(self):
        self.reset_page()
        iter_words = Selector.learn(self.userProfile.get_lesson() + 1, self.userProfile)
        kanji, furigana, french = next(iter_words)
        # print(kanji, furigana, french)

        kanjiText = KANJI_FONT.render(kanji, True, (20, 20, 20))
        kanjiPos = [SCREEN_WIDTH/2 - kanjiText.get_rect().width/2, 100]
        furiganaText = KANJI_FONT.render(furigana, True, (20, 20, 20))
        furiganaPos = [SCREEN_WIDTH/2 - furiganaText.get_rect().width/2, 200]
        frenchText = KANJI_FONT.render(french, True, (20, 20, 20))
        frenchPos = [SCREEN_WIDTH/2 - frenchText.get_rect().width/2, 300]
        self.page_objects["text"] = [(kanjiText, kanjiPos), (furiganaText, furiganaPos), (frenchText, frenchPos)]

        buttonwidth = 200
        button = Button(SCREEN_WIDTH/2 - buttonwidth/2, 420, (buttonwidth, 40), "Next", SMALL_FONT, lambda : self.learn_next_word(iter_words))
        self.page_objects["button"] = [button]

    def update_input_box(self, input_box, events):
        input_box.update(events)

    def draw(self):
        for text, pos in self.page_objects["text"]:
            self.screen.blit(text, pos)
        
        for button in self.page_objects["button"]:
            button.process(self.screen)
        
        for input_box in self.page_objects["inputbox"]:
            input_box.draw(self.screen)

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                if self.userProfile is not None:
                    self.userProfile.save()
                pygame.quit()
                sys.exit()
            for input_box in self.page_objects["inputbox"]:
                input_box.handle_event(event)

            if event.type == pygame.USEREVENT and self.screenPage != "revise" and len(self.page_objects["button"]) == 1:
                self.page_objects["button"][0].change_color("pressed")
                self.page_objects["button"][0].onClickFunction(event.Text)
        for input_box in self.page_objects["inputbox"]:
            self.update_input_box(input_box, events)