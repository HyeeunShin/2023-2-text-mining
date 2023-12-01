import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
title = []
def iframe():
    # selenium 생성
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    # driver = webdriver.Chrome(os.path.abspath('chromedriver'))
    driver.get('https://elaw.klri.re.kr/kor_service/lawAllSearch.do?pCode=01')
    
    # tab list 가져오기
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    tree = soup.select('#tree_1_ul li')
    for i in range(len(tree)):
        result = soup.select_one('#tree_'+str(i+2)+'_span')
        title.append(result.text.replace('\t','_'))
    
    # tab list 기반으로 크롤링
    for i in range(len(tree)):
        if i != 0:
            driver.switch_to.parent_frame()
            # driver.get('https://elaw.klri.re.kr/kor_service/lawAllSearch.do?pCode=01')
        time.sleep(5)
        # tab 메뉴 클릭
        menu = driver.find_element(By.CSS_SELECTOR,'#tree_'+ str(i+2) + '_a')
        driver.implicitly_wait(10)
        ActionChains(driver).move_to_element(menu).click(menu).perform()
        time.sleep(10)
        
        # 탭 목록으로 프레임 전환 
        driver.switch_to.frame('indexFrame')
        html_sub = driver.page_source
        soup2 = BeautifulSoup(html_sub,'html.parser')
 
        test = soup2.select('.ui-widget-content.jqgrow.ui-row-ltr')
        
        page = list(range(2,20))
        while True:
            for t in test:
                # 목록 선택
                test_id = t['id']
                menu2 = driver.find_element(By.CSS_SELECTOR,'tr[id="'+test_id+'"] > td:nth-child(2) > p > a')
                menu2.send_keys(Keys.ENTER)#click()
                tk = soup2.select_one('tr[id="'+test_id+'"]')
                
                # 새창으로 이동
                title_doc = tk.select_one('td:nth-of-type(2)')['title']
                driver.switch_to.window(driver.window_handles[1])
                # 한국어 번역 탭 클릭
                driver.find_element(By.CSS_SELECTOR,"input[type='radio'][value='KOR']").click()
                time.sleep(3)
                # 법령 콘텐츠로 프레임 이동
                driver.switch_to.frame('lawViewContent')
                if not os.path.isdir(title[i]):
                    os.makedirs(title[i])
                if len(title_doc) > 197:
                    title_doc = title_doc[:200] + '...'
                # 법령 크롤링
                with open(title[i]+'/'+title_doc+'.html','w',encoding='utf-8') as f:
                    f.write(driver.page_source)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(3)
                driver.switch_to.frame('indexFrame')
            time.sleep(3)
            if len(test) < 20 or len(page) == 0:
                break
            # 페이지 이동
            driver.execute_script("goPage("+str(page[0])+");")
            print(page[0])
            del page[0]    
            time.sleep(3)
 
            html_sub = driver.page_source
            soup2 = BeautifulSoup(html_sub,'html.parser')
            test = None
            test = soup2.select('.ui-widget-content.jqgrow.ui-row-ltr')

    driver.close()

iframe()
