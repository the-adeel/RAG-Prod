from document import document

words = document[0].split()
chunks = []
chunk_size = 5
overlap = 2

step = chunk_size - overlap

for i in range(0, len(words), step):
    chunk = " ".join(words[i:i+chunk_size])
    chunks.append(chunk)

print(chunks)