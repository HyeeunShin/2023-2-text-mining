법령 크롤링 관련해서 자동화 프로그램

직접 코드로 접근하는 방법 에러 사항이 많아
Selenium이라는 라이브러리를 이용해 직접 Chrome 브라우저를 실행해서
코드상에서 브라우저를 조작하여 법령 내용을 크롤링 하였습니다.
 
****필요 라이브러리****
pip install beautifulsoup4 
pip install selenium
pip install webdriver-manager
chrome 최근버전
**********************

해당 페이지 진입시 페이지가 빈페인것을 확인하실수 있을겁니다.
16편 평생교육법 시행령 
https://elaw.klri.re.kr/kor_service/lawView.do?hseq=52012&lang=ENG 
38편 고령친화산업 진흥법 시행령
https://elaw.klri.re.kr/kor_service/lawView.do?hseq=55963&lang=ENG

==============
법령데이터의 항목별 추출 코드와 추출결과를 공유 드립니다.
 
또한 이전에 보내드린 크롤링데이터에서 오류가 발생하는 파일이있어 해당파일들을 수정하거나 제외하였습니다.
( 법령사이트에 html코드가 비어있는것을 확인 하였습니다.)
 
- 코드의 사용방법은
코드를 법령 html 데이터가 있는 상위 폴더에 위치시키고
 
아래와 같이 실행합니다.
 
python  .\remove_html.py --input 법령분야별 --output 법령분야별_article,title.csv --text article,title 
 
- Input : html 크롤링 데이터가있는 폴더 명이며
- output : 결과파일을 저장할 파일명입니다.
- text : 추출할 항목입니다. ( title : 법령명, article : 본문 추출, article_title 본문제목 ( 여러개 사용시 ',' 로 구분 ex)title,article or article_title, article )
