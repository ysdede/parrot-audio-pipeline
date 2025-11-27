def jaccard_similarity(str1, str2):
    # Split two strings into words
    words_str1 = set(str1.lower().split())
    words_str2 = set(str2.lower().split())

    # Find intersection and union sets
    intersection = words_str1.intersection(words_str2)
    union = words_str1.union(words_str2)

    # Calculate Jaccard similarity score
    return len(intersection) / len(union)

# Example sentences
str1 = "Köpeğim parkta koşuyor"
str2 = "Köpeğim bahçede koşuyor"

# Calculate Jaccard similarity and print
similarity_score = jaccard_similarity(str1, str2)
print(f"Jaccard Similarity: {similarity_score}")
