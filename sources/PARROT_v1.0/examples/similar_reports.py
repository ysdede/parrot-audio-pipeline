# pip install sentence-transformers faiss-cpu pandas
from sentence_transformers import SentenceTransformer, util
import faiss, pandas as pd, numpy as np

#update the file path
file_path="PARROT_v1_0.jsonl"

#loading the dataset
df = pd.read_json(file_path, lines=True)

#embeddings based on the original reports
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")
emb_multilingual = model.encode(df['report'].tolist(), batch_size=128, show_progress_bar=True)
index_multilingual = faiss.IndexFlatIP(emb_multilingual.shape[1]); index_multilingual.add(emb_multilingual.astype('float32'))

#embeddings based on their translation
emb_english = model.encode(df['translation'].tolist(), batch_size=128, show_progress_bar=True)
index_english = faiss.IndexFlatIP(emb_english.shape[1]); index_english.add(emb_english.astype('float32'))

#matching the query to original reports
query = "left-side ischemic stroke"
q_emb = model.encode([query])
D, I = index_multilingual.search(np.array(q_emb, dtype='float32'), k=5)
print("Corresponsing reports based on the multilingual embeddings:\n")
for rank, idx in enumerate(I[0], 1):
    print(f"{rank}. ({df.iloc[idx]['language']}) {df.iloc[idx]['report']}…")
    
#matching the query to translations
D, I = index_english.search(np.array(q_emb, dtype='float32'), k=5)
print("Corresponsing reports based on the translation embeddings:\n")
for rank, idx in enumerate(I[0], 1):
    print(f"{rank}. ({df.iloc[idx]['translation']}…")
