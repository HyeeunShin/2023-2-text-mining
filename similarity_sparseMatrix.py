import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 폴더 경로 설정
base_folder = "output"

# 문서 타이틀과 내용을 저장할 딕셔너리
document_contents = {}

# 각 폴더 안의 문서를 읽어와 딕셔너리에 추가
for folder_name in os.listdir(base_folder):
    folder_path = os.path.join(base_folder, folder_name)
    
    if os.path.isdir(folder_path):
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            
            with open(file_path, 'r', encoding='utf-8') as file:
                # 각 문서의 내용을 읽어옴
                content = file.read()
                
                # 문서 타이틀을 추출 (예: 파일명을 사용)
                title = os.path.splitext(file_name)[0]  # 파일명에서 확장자 제거
                document_contents[title] = content

# 문서 타이틀과 내용을 기반으로 TF-IDF 벡터화
titles = list(document_contents.keys())
contents = list(document_contents.values())

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(contents)

# 코사인 유사도 계산
cosine_sim_matrix = cosine_similarity(tfidf_matrix)

# 가장 유사한 10개의 문서 추출
num_top_similar = 10
most_similar_documents = []

for i in range(len(cosine_sim_matrix)):
    # 현재 문서와의 유사도를 튜플로 저장 (문서 타이틀, 유사도)
    similarity_with_current = [(titles[j], cosine_sim_matrix[i][j]) for j in range(len(cosine_sim_matrix)) if i != j]
    
    # 유사도를 기준으로 정렬
    similarity_with_current.sort(key=lambda x: x[1], reverse=True)
    
    # 가장 유사한 문서들의 타이틀을 저장
    top_similar_titles = [title for title, _ in similarity_with_current[:num_top_similar]]
    
    # 현재 문서와 가장 유사한 10개의 문서 타이틀을 저장
    most_similar_documents.append((titles[i], top_similar_titles))


i = 0
# 결과 출력
for current_title, similar_titles in most_similar_documents:
    q = 0
    i += 1
    print(f"\n-----------------------{i}-------------------------------\n문서 '{current_title}'와 가장 유사한 문서들:")
    for similar_title in similar_titles:
        q += 1
        print(f"{q}  - 문서 '{similar_title}' (유사도: {cosine_sim_matrix[titles.index(current_title)][titles.index(similar_title)]})")
