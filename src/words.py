from typing import List, Tuple, Union

class Kanji:
    kanji: str
    furigana: List(str)
    learned: bool

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

    def is_learned(self):
        return self.learned


class Word:
    japanese: List[Tuple[Kanji, int]] = []
    french: str
    score: float
    success: int
    seen_days: int
    last_seen: int

    def __init__(self, kanjis: List[str], furigana: List[str], kanjiCorpus: List[Kanji], french: str, score: float = None,
                 success: int = None, seen_days: int = None, last_seen: int = None) -> None:

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
        self.score = score
        self.success = success
        self.seen_days = seen_days
        self.last_seen = last_seen

    def update_score(self):
        pass

    def print(self, lang: str):
        word = ""
        if lang == "jp":
            for k, idx in self.japanese:
                if k.is_learned():
                    word += k.get_kanji()
                else:
                    word += k.get_furigana(idx)

        elif lang == "fr":
            word += self.french

        return word