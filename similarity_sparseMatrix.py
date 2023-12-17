import os
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

# 결과를 텍스트 파일로 저장
output_file_path = "similar_documents_output.txt"
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for i in range(len(cosine_sim_matrix)):
        current_title = titles[i]
        similar_titles = [titles[j] for j in sorted(range(len(cosine_sim_matrix[i])), key=lambda k: cosine_sim_matrix[i][k], reverse=True)[:5] if i != j]
        similarity_values = [cosine_sim_matrix[i][j] for j in sorted(range(len(cosine_sim_matrix[i])), key=lambda k: cosine_sim_matrix[i][k], reverse=True)[:5]]
        
        output_file.write(f"\n-----------------------\n문서 '{current_title}'와 가장 유사한 문서들:\n")
        
        for similar_title, similarity in zip(similar_titles, similarity_values):
            output_file.write(f"{similar_title} (유사도: {similarity})\n")

print(f"결과가 '{output_file_path}' 파일에 저장되었습니다.")
