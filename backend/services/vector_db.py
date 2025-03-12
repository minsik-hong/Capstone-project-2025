# 벡터DB 구축

import faiss
import numpy as np
import pickle
import os

class VectorDB:
    def __init__(self, db_path="data/vector_db"):
        self.db_path = db_path
        self.index = None
        self.load()

    def load(self):
        """벡터 DB 로드 또는 생성"""
        if os.path.exists(self.db_path):
            with open(self.db_path, "rb") as f:
                self.index = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(512)  # 512차원 벡터
            self.save()

    def save(self):
        """벡터 DB 저장"""
        with open(self.db_path, "wb") as f:
            pickle.dump(self.index, f)

    def add_vector(self, vector):
        """새로운 뉴스 벡터 추가"""
        self.index.add(np.array([vector], dtype=np.float32))
        self.save()

    def search(self, query_vector, top_k=5):
        """유사한 뉴스 검색"""
        distances, indices = self.index.search(np.array([query_vector], dtype=np.float32), top_k)
        return indices[0]
