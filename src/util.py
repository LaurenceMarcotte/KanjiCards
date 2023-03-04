import os
from typing import List, Tuple, Union
from datetime import date
from enum import Enum

class Kanji:
    kanji: str
    furigana: List(str)

    def __init__(self, kanji: str, sound: Union[List[str], str]) -> None:
        self.kanji = kanji
        self.furigana = list(sound) if isinstance(sound, str) else sound

    def get_furigana(self, item: int):
        return self.furigana[item]

    def get_idx(self, sound: str):
        return self.furigana.index(sound)

    def get_kanji(self):
        return self.kanji

    def __eq__(self, __o: object) -> bool:
        return self.kanji == __o
    
class Profile:
    lesson: int = 0
    username: str
    kanjiLearned: List[Kanji] = []
    wordData: List[object] = []

    def __init__(self, username: str) -> None:
        self.username = username

    def is_kanji_learned(self, kanji):
        return kanji in self.kanjiLearned
    
    @staticmethod
    def load_profile(username: str, folder: str = "./cache/"):
        filename = username + ".csv"
        file = os.path.join(folder, filename)
        with open(file, "r", encoding="utf-8"):
            pass

class Boxes(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 5
    FIVE = 10
    SIX = 15
    SEVEN = 25
    EIGHT = 30
    

class Word:
    japanese: List[Tuple[Kanji, int]] = []
    french: str
    lastSeen: date
    box: Boxes

    def __init__(self, kanjis: List[str], furigana: List[str], kanjiCorpus: List[Kanji], french: str, 
                 lastSeen: date = None, box: Boxes = Boxes.ONE) -> None:

        if len(kanjis) != len(furigana):
            raise ValueError("There should be as many kanjis as groups of furiganas.")

        for kanji, f in zip(kanjis, furigana):
            if kanji in kanjiCorpus:
                kanji_obj = kanjiCorpus[kanjiCorpus.index(kanji)]
            else:
                kanji_obj = Kanji(kanji, f)
            
            furi_idx = kanji_obj.get_idx(f)
            self.japanese.append((kanji_obj, furi_idx))
        
        self.french = french
        self.lastSeen = lastSeen
        self.box = box

    def update_score(self):
        pass

    def print(self, lang: str, profile: Profile):
        word = ""
        if lang == "jp":
            for k, idx in self.japanese:
                if profile.is_kanji_learned(k):
                    word += k.get_kanji()
                else:
                    word += k.get_furigana(idx)

        elif lang == "fr":
            word += self.french

        return word

    
