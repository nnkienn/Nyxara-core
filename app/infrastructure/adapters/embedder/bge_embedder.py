from FlagEmbedding import BGEM3FlagModel

class BGEEmbedder:
    def __init__(self):
        self.model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=False)
        self.dim = 1024


    def embed(self, texts):
        return self.model.encode(texts)['dense_vecs'].tolist()   