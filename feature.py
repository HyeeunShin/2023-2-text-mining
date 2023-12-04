from konlpy.tag import Okt
from sklearn.feature_extraction.text import TfidfVectorizer
import os
import numpy as np
import pandas as pd

# 형태소 분석기 초기화
okt = Okt()

# 법령 텍스트가 있는 디렉토리 경로 (실제 데이터 경로로 수정해주세요)
base_directory = 'C:/Users/as221/github/2023-2-text-mining/2023-2-text-mining/files'

# 결과를 저장할 디렉토리 경로 (없다면 미리 생성해주세요)
output_directory = 'C:/Users/as221/github/2023-2-text-mining/2023-2-text-mining/output'

# 전역 변수로 성공 및 오류 횟수 초기화
success_count = 0
error_count = 0

# 디렉토리 내 파일을 탐색하고 형태소 분석 및 명사 추출
def process_directory(directory_path):
    global success_count, error_count  # Declare these variables as global
    
    for folder_name in os.listdir(directory_path):
        folder_path = os.path.join(directory_path, folder_name)
        
        if os.path.isdir(folder_path):
            # 각 폴더마다 output 폴더에 저장할 디렉토리 생성
            output_folder_path = os.path.join(output_directory, folder_name)
            os.makedirs(output_folder_path, exist_ok=True)
            
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                
                if os.path.isfile(file_path):
                        try:
                            with open(file_path, 'r', encoding='utf-8') as file:
                                law_text = file.read()
                                success_count += 1

                        except UnicodeDecodeError:
                            # UTF-8로 읽기 실패하면 cp949로 시도
                            with open(file_path, 'r', encoding='cp949') as file:
                                law_text = file.read()


                        # 형태소 분석 및 명사 추출
                        nouns = okt.nouns(law_text)
                        
                        # 명사들을 공백으로 구분하여 하나의 문자열로 결합
                        document = " ".join(nouns)
                        
                        # Check if the document is not empty
                        if document:
                            # TF-IDF 벡터 생성
                            vectorizer = TfidfVectorizer()
                            tfidf_vector = vectorizer.fit_transform([document])
                            
                            # TF-IDF 벡터를 배열로 변환
                            tfidf_array = tfidf_vector.toarray()
                            
                            # 결과를 데이터프레임으로 변환
                            df = pd.DataFrame(data=np.c_[tfidf_array], columns=vectorizer.get_feature_names_out())
                                                                
                            # 결과를 CSV 파일로 저장
                            output_folder_path = os.path.join(output_directory, folder_name)
                            os.makedirs(output_folder_path, exist_ok=True)

                            # 디렉토리가 없을 경우 먼저 생성
                            os.makedirs(output_folder_path, exist_ok=True)

                            # 결과를 CSV 파일로 저장
                            output_file_path = os.path.join(output_folder_path, f'{file_name}_tfidf_vector.csv')

                            try:
                                df.to_csv(output_file_path, index=False)
                                print(f"TF-IDF 벡터가 저장된 파일 경로: {output_file_path}")
                                success_count += 1
                            except Exception as e:
                                print(f"예외 발생: {e}. {file_name} 파일을 처리하는 중 오류가 발생하였습니다. 해당 파일은 건너뛰고 다음 파일을 처리합니다.")
                                error_count += 1
                                continue
                        else:
                            print(f"Warning: Document is empty. Skipping file: {file_name}")
                            error_count += 1

# 디렉토리 내 파일을 처리
process_directory(base_directory)

print("\nsuccess_count: ", success_count, "\nerror_count: ", error_count)
