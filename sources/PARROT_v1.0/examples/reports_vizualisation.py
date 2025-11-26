# pip install sentence-transformers umap-learn matplotlib pandas datasets
from sentence_transformers import SentenceTransformer
import umap, pandas as pd, plotly.express as px, numpy as np
import json, textwrap

#update the file path
file_path="PARROT_v1_0.jsonl"

#loading the dataset
df = pd.read_json(file_path, lines=True)

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

#embeddings based on their translation
emb_english = model.encode(df['translation'].tolist(), batch_size=128, show_progress_bar=True)

proj  = umap.UMAP(n_neighbors=15, min_dist=0.1, metric="cosine",
                  random_state=42).fit_transform(emb_english)
df["x"], df["y"] = proj[:,0], proj[:,1]

def make_hover(row, maxlen=240):
    snippet = textwrap.shorten(row["translation"].replace("\n", " "), width=maxlen, placeholder="…")
    return f"<b>ID:</b> {row['no']}<br><b>Lang:</b> {row['language']}<br><br>{snippet}"

df["hover"] = df.apply(make_hover, axis=1)

#create the plot
fig = px.scatter(
    df,
    x="x", y="y",
    color="language",
    hover_name="no",
    hover_data={"hover":True, "x":False, "y":False, "language":False},
    opacity=0.8,
    height=600,
)
fig.update_traces(marker=dict(size=6, line=dict(width=0)))
fig.update_traces(hovertemplate="%{customdata[0]}<extra></extra>")  # use pre-built HTML
fig.update_layout(
    title="UMAP of Radiology Reports",
    showlegend=True,
    margin=dict(l=0, r=0, t=40, b=0),
)

#save the plot
fig.write_html("/home/bastien/rad_reports_umap.html",                
               full_html=True,              # keep the HTML wrapper
               include_plotlyjs="cdn")      # or "directory" / "embed")
print("✅ Saved: rad_reports_umap.html")