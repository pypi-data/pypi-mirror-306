import re
from arm_rag.config import CONFIG


class Chunking:
    def __init__(self, type):
        self.chunk_size = CONFIG['document']['chunk_size']
        self.type = type


    def simple_splitter(self, text):
        chunks = []
        words = text.strip().split(" ")
        for i in range(0, len(words), self.chunk_size):
            chunks.append(" ".join(words[i:i+self.chunk_size]))
        return chunks
    
    
    def recursive_splitter(self, text):
        sentences = re.split(r"(?<=[։:])", text)
        chunks = []
        current_chunk = []
        current_length = 0
        for sentence in sentences:
            words = sentence.strip().split()
            if current_length + len(words) > self.chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_length = 0
            current_chunk.append(sentence)
            current_length += len(words)
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        return chunks
    

    def splitter(self, text):
        if self.type == 'simple':
            return self.simple_splitter(text)
        elif self.type == 'recursive':
            return self.recursive_splitter(text)
        else:
            raise ValueError("Invalid split type")
    