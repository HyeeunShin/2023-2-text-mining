import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_similar_documents(base_folder, target_keyword, num_top_similar=10):
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
    cosine_similarities = cosine_similarity(tfidf_matrix)

    target_index = document_titles.index(target_keyword)
    similar_indices = cosine_similarities[target_index].argsort()[:-num_top_similar-1:-1]
    similar_documents = [(document_titles[i], cosine_similarities[target_index][i]) for i in similar_indices if i != target_index]

    return similar_documents

def main():
    base_folder = "output"
    target_keyword = "인사청문회법"
    num_top_similar = 10

    similar_documents = find_similar_documents(base_folder, target_keyword, num_top_similar)

    print(f"\n'{target_keyword}' 문서와 가장 유사한 문서 {num_top_similar}개:\n")
    for similar_title, similarity in similar_documents:
        print(f"  - 문서 '{similar_title}' (유사도: {similarity})")

if __name__ == "__main__":
    main()
인사청문회법 CONFIRMATION HEARING ACT_output.csv.csv_tfidf_vector
(유사도: 0.00012478196854531383)
