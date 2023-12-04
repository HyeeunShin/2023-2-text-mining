import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def extract_document_vectors(base_folder):
    document_contents = {}
    document_titles = []

    for folder_name in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder_name)

        if os.path.isdir(folder_path):
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)

                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    title = os.path.splitext(file_name)[0]
                    document_titles.append(title)
                    document_contents[title] = content

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(document_contents.values())
    document_vectors = tfidf_matrix.toarray()

    return document_titles, document_vectors

def find_most_similar_documents(document_titles, document_vectors, num_top_similar=5):
    similar_documents_dict = {}

    for query_index in range(len(document_titles)):
        query_vector = document_vectors[query_index]
        cosine_similarities = cosine_similarity([query_vector], document_vectors)[0]

        # 현재 문서를 제외하고 가장 유사한 문서 N개 찾기
        similar_indices = cosine_similarities.argsort()[:-num_top_similar-1:-1]
        similar_documents = [(document_titles[i], cosine_similarities[i]) for i in similar_indices if i != query_index]

        similar_documents_dict[document_titles[query_index]] = similar_documents

    return similar_documents_dict

def main():
    base_folder = "output"
    num_top_similar = 5  # 각 문서에 대해 찾을 가장 유사한 문서의 개수

    document_titles, document_vectors = extract_document_vectors(base_folder)
    similar_documents_dict = find_most_similar_documents(document_titles, document_vectors, num_top_similar)

    print(f"각 문서에 대해 가장 유사한 문서 {num_top_similar}개:")
    
    for title, similar_documents in similar_documents_dict.items():
        print(f"\n쿼리 문서: '{title}'")
        print(f"가장 유사한 문서 {num_top_similar}개:")
        
        for similar_title, similarity in similar_documents:
            print(f"  - 문서 '{similar_title}' (유사도: {similarity})")

if __name__ == "__main__":
    main()
