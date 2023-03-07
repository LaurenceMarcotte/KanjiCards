import os
from typing import List, Tuple, Union
from datetime import datetime
from enum import Enum
import json

import pandas as pd

CORPUS = pd.read_csv("../media/corpus.csv", delimiter=";", encoding="utf-8")

CORPUS["kanji"] = CORPUS["kanji"].str.split(",")
CORPUS["furigana"] = CORPUS["furigana"].str.split(",")

KANJI_TO_IDS = CORPUS[CORPUS["word"]==0][["id", "kanji"]]
KANJI_TO_IDS["kanji"] = KANJI_TO_IDS["kanji"].apply(lambda r: r[0])
KANJI_TO_IDS = KANJI_TO_IDS.set_index("kanji")

# print(KANJI_TO_IDS)


class Boxes(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 5
    FIVE = 10
    SIX = 15
    SEVEN = 25
    EIGHT = 30
   

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
        return id in self.wordLearned['id'].to_list()
    
    @staticmethod
    def load(username: str, folder: str = "../cache"):
        filename = username + ".json"
        file = os.path.join(folder, filename)
        with open(file, "r", encoding="utf-8") as f:
            f = json.load(f)
        profileCSV = pd.read_csv(f['wordlearned'], encoding="utf-8")

        profileCSV['box']=profileCSV['box'].apply(lambda r: eval(r))
        
        return Profile(username, f['lesson'], profileCSV)
    
    def save(self, folder: str = "../cache"):
        filename = self.username + ".json"
        file = os.path.join(folder, filename)
        wordLearnedFile = os.path.join(folder, self.username + ".csv")
        if not os.path.isdir(folder):
            os.mkdir(folder)
        self.wordLearned.to_csv(wordLearnedFile, header=True, index=False)
        with open(file, "w", encoding = "utf-8") as f:
            json.dump({"lesson": self.lesson, "wordlearned": wordLearnedFile}, f)

    def new_word_learned(self, newWord: int):
        # print(self.wordLearned)
        size = len(self.wordLearned)
        if size == 0:
            self.wordLearned = pd.DataFrame([[newWord, datetime.today().strftime("%Y-%m-%d"), Boxes.ONE]], columns=['id', 'lastSeen', 'box'])
        else:
            self.wordLearned.loc[size] = [newWord, datetime.today().strftime("%Y-%m-%d"), Boxes.ONE]

    def update_profile(self, newWords: List[int]):
        for newWord in newWords:
            self.new_word_learned(newWord)

    def get_lesson(self):
        return self.lesson
    

class Selector:
    
    def learn(lessonNumber: int, userProfile: Profile):
        lesson = CORPUS[CORPUS["lesson"]==lessonNumber]
        kanjis = lesson[lesson["word"]==0]
        newWords = lesson[lesson["word"]==1]

        print(f"Let's start with the kanji for lesson {lessonNumber}.")
        for _, row  in kanjis.iterrows():
            kanjiID, kanji, furigana, french = row['id'], row['kanji'], row['furigana'], row['french']
            if not userProfile.is_learned(kanjiID):
                print("".join(kanji))
                print("".join(furigana))
                print(french)
                enter = input("Press Enter for the next one")
                userProfile.new_word_learned(kanjiID)
        
        print("Now, let's see some words with these new kanjis.")
        for _, row in newWords.iterrows():
            wordID, word, furigana, french = row['id'], row['kanji'], row['furigana'], row['french']
            kanjiToPrint = ""
            for kanji, kana in zip(word, furigana):
                kanjiID = KANJI_TO_IDS.loc[kanji]['id'] if kanji in KANJI_TO_IDS.index else None
                learned = userProfile.is_learned(kanjiID) if kanjiID is not None else False
                if learned:
                    kanjiToPrint += kanji
                else:
                    kanjiToPrint += kana
            print(kanjiToPrint)
            print("".join(furigana))
            print(french)
            enter = input("Press Enter for the next one")
            userProfile.new_word_learned(wordID)

        userProfile.lesson = lessonNumber

    
    def revise(userProfile: Profile):
        pass

# class Learnable:
#     lastSeen: datetime
#     box: Boxes
#     french: str
#     id: int


# class Kanji(Learnable):
#     kanji: str
#     furigana: List(str)

#     def __init__(self, kanji: str, sound: Union[List[str], str]) -> None:
#         self.kanji = kanji
#         self.furigana = list(sound) if isinstance(sound, str) else sound

#     def get_furigana(self, item: int):
#         return self.furigana[item]

#     def get_idx(self, sound: str):
#         return self.furigana.index(sound)

#     def get_kanji(self):
#         return self.kanji

#     def __eq__(self, __o: object) -> bool:
#         return self.kanji == __o
    
# class Word(Learnable):
#     japanese: List[Tuple[Kanji, int]] = []

#     def __init__(self, kanjis: List[str], furigana: List[str], kanjiCorpus: List[Kanji], french: str, 
#                  lastSeen: date = None, box: Boxes = Boxes.ONE) -> None:

#         if len(kanjis) != len(furigana):
#             raise ValueError("There should be as many kanjis as groups of furiganas.")

#         for kanji, f in zip(kanjis, furigana):
#             if kanji in kanjiCorpus:
#                 kanji_obj = kanjiCorpus[kanjiCorpus.index(kanji)]
#             else:
#                 kanji_obj = Kanji(kanji, f)
            
#             furi_idx = kanji_obj.get_idx(f)
#             self.japanese.append((kanji_obj, furi_idx))
        
#         self.french = french
#         self.lastSeen = lastSeen
#         self.box = box

#     def update_score(self):
#         pass

#     def print(self, lang: str, profile: Profile):
#         word = ""
#         if lang == "jp":
#             for k, idx in self.japanese:
#                 if profile.is_kanji_learned(k):
#                     word += k.get_kanji()
#                 else:
#                     word += k.get_furigana(idx)

#         elif lang == "fr":
#             word += self.french

#         return word

    
