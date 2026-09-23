import tkinter as tk
from tkinter import filedialog

import os
import sys
import json
import numpy as np
print("Loading the model")
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('./mdl.model')
directory = ""
phrase = ""
archive = []
results = []

def pickdir():
    directory = filedialog.askdirectory()
    dirloc.insert(tk.END, directory)
    files = os.listdir(directory)
    # Filtering only the files.
    files = [f for f in files if os.path.isfile(directory+'/'+f)]
    for f in files:
        if ".json" in f:
            with open(f,"r") as fh:
                content = json.load(fh)
                archive.append(content)

def findsimilarities():
    phrase = query.get()
    A = embeddings = model.encode(phrase).tolist()

    best = 0
    best_entry = ""
    for data in archive:
        for entry in data["entries"]:
            B = list(entry["embedding"])
            kosini = np.dot( A, B ) / (np.linalg.norm(A) * np.linalg.norm(B) )
            if (kosini > best):
                best = kosini
                best_entry = entry
                results.insert(0,best_entry)
                
    l = 10
    if len(results) < 10:
        l = len(results)-1
        
    for i in range(l):
        print("#"+str(i)+": ---------------------")
        print(results[i]['text'])
    
    text_widget.delete('1.0', tk.END)
    text_widget.insert(tk.END, "File: "+best_entry["file"] + "\nPosition:" + str(best_entry["pos"]))



root = tk.Tk()

root.title('SES')

tk.Label(root, text="Path to archive").grid(row=0, column=0)
tk.Label(root, text="Query").grid(row=3, column=0)

dirloc = tk.Entry(root)
query = tk.Text(root, height=10, width=100)

dirloc.grid(row=1, column=0)
query.grid(row=4, column=0)

dir_button = tk.Button(root, text="Select dir", width=20, command=lambda:pickdir())
dir_button.grid(row=2,column=0)

srch_button = tk.Button(root, text="Search", width=20, command=lambda:findsimilarities())
srch_button.grid(row=5, column=0)




text_widget = tk.Text(root, height=15, width=100)
text_widget.grid(row=6, column=0)

text_widget.insert(tk.END,"Waiting for a query")

root.mainloop()




