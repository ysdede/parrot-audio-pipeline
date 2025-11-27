
from similarity.damerau import Damerau

# tr_usr.dic dosyasını oku
with open("C:/Users/steam/AppData/Roaming/Notepad++/plugins/config/Hunspell/tr_TR.usr", "r", encoding="utf-8") as f:
    dictionary_words = f.read().split("\n")

# error_words_new.txt dosyasını oku
with open("error_words_new.txt", "r") as f:
    error_words = f.read().split("\n")

def damerau_levenshtein(word, dictionary):
    damerau = Damerau()
    return [(kelime, damerau.distance(word, kelime)) for kelime in dictionary]

error_correct_list = []

for word in error_words:
    similarities = damerau_levenshtein(word, dictionary_words)
    best_match = min(similarities, key=lambda x: x[1])  # En düşük benzerlik skoruna sahip olanı seç
    error_correct_list.append((word, best_match[0]))  # Hatalı kelime ve en benzer doğru kelimeyi listeye ekle
    print(f"{word} -> {best_match[0]}")
