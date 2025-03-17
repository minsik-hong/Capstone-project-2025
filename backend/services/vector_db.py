# 벡터DB 구축

import faiss  # 벡터 검색을 위한 라이브러리
import numpy as np  # 수치 계산을 위한 라이브러리
import pickle  # 객체 직렬화를 위한 라이브러리
import os  # 파일 및 디렉토리 작업을 위한 라이브러리

class VectorDB:
    def __init__(self, db_path="data/vector_db"):
        self.db_path = db_path  # 벡터 DB 파일 경로
        self.index = None  # 벡터 인덱스 초기화
        self.load()  # 벡터 DB 로드

    def load(self):
        """벡터 DB 로드 또는 생성"""
        if os.path.exists(self.db_path):  # DB 파일이 존재하면
            with open(self.db_path, "rb") as f:
                self.index = pickle.load(f)  # 파일에서 벡터 인덱스 로드
        else:
            self.index = faiss.IndexFlatL2(512)  # 512차원 L2 거리 기반 벡터 인덱스 생성
            self.save()  # 새로 생성된 인덱스를 저장

    def save(self):
        """벡터 DB 저장"""
        with open(self.db_path, "wb") as f:
            pickle.dump(self.index, f)  # 벡터 인덱스를 파일에 저장

    def add_vector(self, vector):
        """새로운 뉴스 벡터 추가"""
        self.index.add(np.array([vector], dtype=np.float32))  # 벡터를 인덱스에 추가
        self.save()  # 변경된 인덱스를 저장

    def search(self, query_vector, top_k=5):
        """유사한 뉴스 검색"""
        distances, indices = self.index.search(np.array([query_vector], dtype=np.float32), top_k)  
        # 쿼리 벡터와 유사한 상위 K개의 벡터 검색
        return indices[0]  # 검색된 벡터의 인덱스 반환