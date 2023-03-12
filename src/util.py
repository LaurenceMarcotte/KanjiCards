# -*- coding: utf-8 -*-
import os
from typing import List, Tuple
from datetime import datetime
from enum import Enum
import json
import random

import pandas as pd

CORPUS = pd.read_csv("./media/corpus.csv", delimiter=";", encoding="utf-8")

CORPUS["kanji"] = CORPUS["kanji"].str.split(",")
CORPUS["furigana"] = CORPUS["furigana"].str.split(",")

KANJI_TO_IDS = CORPUS[CORPUS["word"]==0][["id", "kanji"]]
KANJI_TO_IDS["kanji"] = KANJI_TO_IDS["kanji"].apply(lambda r: r[0])
KANJI_TO_IDS = KANJI_TO_IDS.set_index("kanji")
CORPUS = CORPUS.set_index("id")

# print(KANJI_TO_IDS)
# print(CORPUS)

def identify_known_kanji(kanjis: List[str], furiganas: List[str], userProfile: 'Profile'):
    word = ""
    for kanji, kana in zip(kanjis, furiganas):
        kanjiID = KANJI_TO_IDS.loc[kanji]['id'] if kanji in KANJI_TO_IDS.index else None
        learned = userProfile.is_learned(kanjiID) if kanjiID is not None else False
        if learned:
            word += kanji
        else:
            word += kana

    return word


class Boxes(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 5
    FIVE = 10
    SIX = 15
    SEVEN = 25
    EIGHT = 30

    def __le__(self, __x: 'Boxes') -> bool:
        return self.value <= __x.value

    def __lt__(self, __x: 'Boxes') -> bool:
        return self.value < __x.value
    
    def __eq__(self, __x: 'Boxes') -> bool:
        return self.value == __x.value
    
    def __add__(self, __x: int) -> 'Boxes':
        boxes = list(iter(Boxes))
        idx = boxes.index(self)
        new_idx = idx + __x
        if new_idx > 8:
            new_idx = 8
        return boxes[new_idx]
    
    def __sub__(self, __x: int) -> 'Boxes':
        boxes = list(iter(Boxes))
        idx = boxes.index(self)
        new_idx = idx - __x
        if new_idx < 0:
            new_idx = 0
        return boxes[new_idx]
    

class Profile:
    lesson: int = 0
    username: str
    wordLearned: pd.DataFrame

    def __init__(self, username: str, lesson: int = 0, wordLearned: pd.DataFrame = pd.DataFrame()) -> None:
        self.username = username
        self.lesson = lesson
        self.wordLearned = wordLearned

    def is_learned(self, id: int):
        if len(self.wordLearned) == 0:
            return False
        return id in self.wordLearned.index
    
    @staticmethod
    def exists(username: str, folder: str = "./cache"):
        filename = username + ".json"
        file = os.path.join(folder, filename)
        if os.path.isfile(file):
            return True
        return False
    
    @staticmethod
    def load(username: str, folder: str = "./cache"):
        filename = username + ".json"
        file = os.path.join(folder, filename)
        with open(file, "r", encoding="utf-8") as f:
            f = json.load(f)
        profileCSV = pd.read_csv(f["wordlearned"], encoding="utf-8", index_col="id")

        profileCSV["box"]=profileCSV["box"].apply(lambda r: eval(r))
        profileCSV["lastSeen"] = pd.to_datetime(profileCSV["lastSeen"], format="%Y-%m-%d")
        return Profile(username, f["lesson"], profileCSV)
    
    def save(self, folder: str = "./cache"):
        filename = self.username + ".json"
        file = os.path.join(folder, filename)
        wordLearnedFile = os.path.join(folder, self.username + ".csv")
        if not os.path.isdir(folder):
            os.mkdir(folder)
        self.wordLearned["lastSeen"] = self.wordLearned["lastSeen"].dt.strftime("%Y-%m-%d")
        self.wordLearned.to_csv(wordLearnedFile, header=True, index=True)
        with open(file, "w", encoding = "utf-8") as f:
            json.dump({"lesson": self.lesson, "wordlearned": wordLearnedFile}, f)

    def new_word_learned(self, newWord: int):
        print(self.wordLearned)
        size = len(self.wordLearned)
        if size == 0:
            self.wordLearned = pd.DataFrame([[newWord, datetime.today(), Boxes.ONE]], columns=["id", "lastSeen", "box"])
            self.wordLearned = self.wordLearned.set_index("id")
        else:
            self.wordLearned.loc[newWord] = [datetime.today(), Boxes.ONE]

    def update_profile(self, newWords: List[int]):
        for newWord in newWords:
            self.new_word_learned(newWord)

    def get_lesson(self):
        return self.lesson
    
    def get_datalearned(self):
        return self.wordLearned.copy()
    
    def revise_word(self, wordID: int, newBox: 'Boxes'):
        self.wordLearned.at[wordID, "lastSeen"] = pd.Timestamp.today()
        self.wordLearned.at[wordID, "box"] = newBox

    def get_box_word(self, wordID: int):
        return self.wordLearned.iloc[wordID]["box"]
    

class Selector:
    
    def learn(lessonNumber: int, userProfile: Profile):
        lesson = CORPUS[CORPUS["lesson"]==lessonNumber]
        kanjis = lesson[lesson["word"]==0]
        newWords = lesson[lesson["word"]==1]

        print(f"Let's start with the kanji for lesson {lessonNumber}.")
        for kanjiID, row  in kanjis.iterrows():
            kanji, furigana, french = row['kanji'], row['furigana'], row['french']
            if not userProfile.is_learned(kanjiID):
                yield u"".join(kanji), u"".join(furigana), french
                # print("".join(kanji))
                # print("".join(furigana))
                # print(french)
                # enter = input("Press Enter for the next one")
                userProfile.new_word_learned(kanjiID)
        
        print("Now, let's see some words with these new kanjis.")
        for wordID, row in newWords.iterrows():
            word, furigana, french = row['kanji'], row['furigana'], row['french']
            kanjiToPrint = identify_known_kanji(word, furigana, userProfile)
            yield kanjiToPrint, "".join(furigana), french
            # print(kanjiToPrint)
            # print("".join(furigana))
            # print(french)
            # enter = input("Press Enter for the next one")
            userProfile.new_word_learned(wordID)

        userProfile.lesson = lessonNumber

    
    def revise(userProfile: Profile):
        data = userProfile.get_datalearned()
        data["countdown"] = data["box"].apply(lambda b: b.value) - (pd.Timestamp.today() - data["lastSeen"]).dt.days
        word_to_revise = data[data["countdown"]<=1]
        word_to_revise = word_to_revise.sort_values(by="box")
        print(word_to_revise)
        selected = word_to_revise[word_to_revise["box"].isin([Boxes.ONE, Boxes.TWO, Boxes.THREE, Boxes.FOUR])]
        print(selected)
        sampled = word_to_revise[word_to_revise["box"].isin([Boxes.FIVE, Boxes.SIX, Boxes.SEVEN, Boxes.EIGHT])]
        if len(sampled) > 0:
            sampled = sampled.groupby(by="box").sample(n=3, replace=False)
            selected = pd.concat([selected, sampled])

        selected = selected.sample(frac=1)
        choices = ['fr', 'jp', 'furi']
        for i in range(len(selected)):
            id = selected.iloc[i].name
            choice = random.choice(choices)
            word, furigana, french = CORPUS.loc[id]["kanji"], CORPUS.loc[id]["furigana"], CORPUS.loc[id]["french"]
            kanjiToPrint = identify_known_kanji(word, furigana, userProfile)
            furigana = "".join(furigana)
            yield id, word, kanjiToPrint, furigana, french, choice
            # correct = False
            # if choice == "fr":
            #     print(french)
            #     answer1 = input("Enter the word in kanji:\n")
            #     answer2 = input("Enter the word in furigana:\n")
            #     if (answer1 == kanjiToPrint or answer1 == "".join(word)) and answer2 == furigana:
            #         correct = True
            # elif choice == "furi":
            #     print(furigana)
            #     yield id, french
            #     answer1 = input("Enter the word in kanji:\n")
            #     answer2 = input("Enter the word in french:\n")
            #     if (answer1 == kanjiToPrint or answer1 == "".join(word)) and answer2.lower() in french.lower().split("|"):
            #         correct = True
            # elif choice == "jp":             
            #     print(kanjiToPrint)
            #     yield id, kanjiToPrint
            #     answer1 = input("Enter the word in french:\n")
            #     answer2 = input("Enter the word in furigana:\n")
            #     if answer1.lower() in french.lower().split("|") and answer2 == furigana:
            #         correct = True
            # box = selected.iloc[i]["box"]
            # if correct:
            #     print("Correct!")
            #     userProfile.revise_word(id, box + 1)
            # else:
            #     print(f"Wrong, the answer is:\n {kanjiToPrint} \n {furigana} \n {french}")
            #     userProfile.revise_word(id, box - 1)
            print(userProfile.get_datalearned())


