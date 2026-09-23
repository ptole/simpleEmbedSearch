import pymupdf4llm
import os
import sys
import json

from sentence_transformers import SentenceTransformer

NBLOCK = 1024

if len(sys.argv) < 2:
    sys.exit("Please give path to the archive folder, and optionally blocksize for parsing text")

path = sys.argv[1]
filename = os.path.split(sys.argv[1])[-1].split('.')[0]

if len(sys.argv > 2):
    NVBLOCK = int(sys.argv[2])

md = pymupdf4llm.to_markdown(path)
with open(filename+".md", "w") as fh:
    fh.write(md)
    
model = SentenceTransformer('./mdl.model')

out = {"entries": []}


txt = md



for idx in range( 0, len(txt) - NBLOCK, 64 ):
    block = txt[idx:idx+NBLOCK]
    embeddings = model.encode(block)
    entry = {"text": block, "pos": idx, "file": filename, "embedding": embeddings.tolist()}
    out["entries"].append( entry )

with open(filename+".json", "w") as fh:
    json.dump( out, fh, sort_keys = True)
