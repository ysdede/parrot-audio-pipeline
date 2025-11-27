import Levenshtein

# Compute similarity ratio between two strings using Levenshtein distance

def similarity(word1, word2):
    return Levenshtein.ratio(word1, word2)

# Example sentences (English translation)
c1 = "A cystic formation possibly belonging to a Nabothian cyst was observed in the cervical location, measuring approximately 1.5 cm."
c2 = "A cystic formation possibly belonging to a Nabothian cyst was observed in the cervical location, measuring approximately 1.5 cm."

print(similarity(c1, c2))
