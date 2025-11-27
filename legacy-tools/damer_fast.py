from similarity.damerau import Damerau
import multiprocessing

def damerau_levenshtein(word, dictionary):
    damerau = Damerau()
    return [(kelime, damerau.distance(word, kelime)) for kelime in dictionary]

def process_error_word(idx, word, dictionary):
    similarities = damerau_levenshtein(word, dictionary)
    best_match = min(similarities, key=lambda x: x[1])  # En düşük benzerlik skoruna sahip olanı seç
    print(f"{idx} {word} -> {best_match[0]}")
    return idx, word, best_match[0]

def main(dictionary_words, error_words):
    # CPU çekirdek sayısını al
    num_cores = 6  # multiprocessing.cpu_count()

    # İşlem havuzu oluştur
    pool = multiprocessing.Pool(processes=num_cores)

    error_correct_list = []

    # Batch boyutunu ayarla
    batch_size = 100

    # Hatalı kelimeleri batch'lere böl
    batches = [error_words[i:i+batch_size] for i in range(0, len(error_words), batch_size)]

    # Her bir batch'i işlem havuzuna gönder
    results = pool.starmap(process_error_word, [(idx, word, dictionary_words) for idx, batch in enumerate(batches) for word in batch])

    # Sonuçları indeks sırasına göre sırala
    results.sort(key=lambda x: x[0])

    # Hatalı ve doğru kelimeleri TSV dosyasına yaz
    with open("error_word_corrections.tsv", "w", encoding="utf-8") as tsv_file:
        tsv_file.write("Index\tHatalı Kelime\tDoğru Kelime\n")
        for idx, error_word, corrected_word in results:
            tsv_file.write(f"{idx}\t{error_word}\t{corrected_word}\n")

if __name__ == "__main__":
    # tr_usr.dic dosyasını oku
    with open("C:/Users/steam/AppData/Roaming/Notepad++/plugins/config/Hunspell/tr_TR.usr", "r", encoding="utf-8") as f:
        dictionary_words = f.read().split("\n")

    # error_words_new.txt dosyasını oku
    with open("error_words_new.txt", "r") as f:
        error_words = f.read().split("\n")

    main(dictionary_words, error_words)
