import json
import re
import time
from multiprocessing import Pool, cpu_count

corpus_path = "aggregated_sentences-raw-2nd.csv"
error_words_path = "error_words.txt"
# error_words_path = "error_words_short_test.txt"

def count_occurrences(args):
    words, corpus = args
    results = []
    print(f"Worker starts processing chunk with first word '{words[0]}' and last word '{words[-1]}'")
    for i, word in enumerate(words):
        count = corpus.count(f" {word} ")
        results.append((word, count))
        # if i % 10 == 0:  # Print a message every 10 words processed
        if count > 0:
            print(f"{word:<32} {count:<6} {i+1}/{len(words)}")
    return results

def chunkify(lst, n):
    k, m = divmod(len(lst), n)
    print(k, m, len(lst), n)

    ewc = []

    for i in range(0, len(lst) - k, k):
        ewc.append(lst[i : i + k])
        print(f"Appending: {i} : {i + k}")

    if m > 0:
        ewc[-1].extend(lst[-m:])

    for i, chunk in enumerate(ewc):
        print(f"Chunk {i} {len(chunk)} {chunk[0]:<32} -> {chunk[-1]:<32}")
    
    return ewc


def main(corpus, error_words):
    start_time = time.time()

    num_processes = 10  # cpu_count()
    error_word_chunks = chunkify(error_words, num_processes)

    tasks = [(chunk, corpus) for chunk in error_word_chunks]

    with Pool(num_processes) as pool:
        results = pool.map(count_occurrences, tasks)
    
    # flatten result and sort words by occurrencies
    results_flatten = [item for sublist in results for item in sublist]
    results_flatten.sort(key=lambda x: x[1], reverse=True)
    # drop word count <= 1
    # sum of result ellements
    total_occurrences = sum([item[1] for item in results_flatten])

    WER = 0

    try:
        WER = 1 - total_occurrences / len(corpus.split())
    except:
        pass

    results_flatten = [item for item in results_flatten if item[1] > 1]

    # count words in corpus
    corpus_words = corpus.split()

    # save result as json
    with open("error_words_occurrences.json", "w", encoding="utf-8") as file:
        json.dump(results_flatten, file, indent=4, ensure_ascii=False)

    elapsed_time = time.time() - start_time
    """Total corpus words: 30086796, total error words: 97995, total occurrences: 171272, WER: 0.9943"""
    """Total corpus words: 30087085, total error words: 97213, total occurrences: 167119, WER: 0.9944"""
    """Total corpus words: 30087611, total error words: 96124, total occurrences: 161626, WER: 0.9946"""
    try:
        print(f"Total corpus words: {len(corpus_words)}, total error words: {len(error_words)}, total occurrences: {total_occurrences}, WER: {WER:.4f}")
    except:
        pass

    print(f"Total processing time: {elapsed_time/60:.2f} mins")

if __name__ == "__main__":
    with open(error_words_path, "r", encoding="utf-8") as file:
        error_words = file.read().splitlines()

    with open(corpus_path, "r", encoding="utf-8") as file:
        corpus = file.read()

    main(corpus, error_words)
