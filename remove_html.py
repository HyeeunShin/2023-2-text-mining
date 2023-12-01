from distutils.log import error
from itertools import count
import os
import csv
import argparse
import sys

from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
map = {'title':'법령명','article':'본문','article_title':'본문제목'}
parser.add_argument('--text',type=str,help='추출할 항목, title : 법령명, article : 본문, article_title : 본문 제목',default='title,article,article_title')
parser.add_argument('--output',type=str,help='결과 저장 파일명(csv포맷)',default='result.csv')
parser.add_argument('--input',type=str,help='html 파일이 존재하는 상위 폴더명',default='.')
parser.add_argument('--patherr',type=int,help='존재하지 않는 경로 혹은 파일 에러 발생시 1설정',default=0)
args = parser.parse_args()
files = []
def search(dirname):
    # os.chdir(dirname)/
    global files
    try:
        filenames = os.listdir(dirname)
        for index,filename in enumerate(filenames):
            full_filename = os.path.join(dirname, filename)

            if os.path.isdir(full_filename):
                search(full_filename)
                # print(full_filename)
            else:
                    ext = os.path.splitext(full_filename)[-1]
                    if ext == '.html': 
                        # print(full_filename)
                        files.append(full_filename)
    except PermissionError:
        pass

def search_remove_err(dirname,flag=False):
    global files
    
    count = 1
    try:
        if not flag:
            filenames = os.listdir(dirname)
            for index,filename in enumerate(filenames):
                full_filename = os.path.join(dirname, filename)
                
                if os.path.isdir(full_filename):
                    if '·' in full_filename or 'ㆍ' in full_filename or '·' in full_filename:
                        os.rename(full_filename,full_filename.replace('·','-').replace('ㆍ','-').replace('·','-'))
            

        filenames = os.listdir(dirname)
        for index,filename in enumerate(filenames):
            full_filename = os.path.join(dirname, filename)

            if os.path.isdir(full_filename):
                search_remove_err(full_filename,flag=True)
                # print(full_filename)
            else:
                ext = os.path.splitext(full_filename)[-1]
                ext2 = full_filename.split('\\')#os.path.splitext(full_filename)
                # print(ext2)
                if ext == '.html': 
                    os.chdir('\\'.join(ext2[:-1]))
                    # print(os.listdir())
                    # print('\\'.join(ext2[:-1]))
                    full_filename2 = '\\'.join(ext2[2:])
                    # print(full_filename2)
                    if '·' in full_filename2 or 'ㆍ' in full_filename2 or '·' in full_filename2:
                        # print(ext)
                        # print('fff','\\'.join(ext[:-3]))
                        fp = '\\'.join(ext2[2:])
                        os.rename(full_filename2,fp.replace('·','-').replace('ㆍ','-').replace('·','-'))
                        full_filename2 = fp.replace('·','-').replace('ㆍ','-').replace('·','-')
                        ext2[-1] = full_filename2
                    # print(full_filename2)
                    # ext3 = full_filename2.split('\\')#os.path.splitext(full_filename) 
                    # print(os.getcwd())   
                    if len(ext2[-1]) > 200:
                        # print(os.listdir())
                        # print(os.getcwd())  
                        ext2[-1] = ext2[-1][:100]+'.html'
                        fp = '\\'.join(ext2[2:])
                        # print(full_filename2)
                        os.rename(full_filename2,fp)
                        # os.chdir('..')
                    os.chdir('..')
    except PermissionError:
        pass

if args.patherr == 1:
    count = 0
    # while count == 0 or count == None:
    os.chdir(args.input)
    # print(os.listdir())
    search_remove_err('.')
    
        # print(count)
    print('patherr 처리 완료')
    search('.')
else:
    search(args.input)
# print(os.listdir())
# print(os.getcwd())

# print(os.getcwd())
# sys.exit()
# print(files)
# sys.exit()
# files = os.listdir()
# print(files)
# csv_f = open('total.csv','w',encoding='utf-8',newline='')
# csv_writer = csv.writer(csv_f)
# csv_writer.writerow(['법령명 영어','법령명 한국어','article_title_eng','article_title_kor','article_eng','article_kor'])
import re
p = re.compile('제[0-9]+장')
# print(args.text)

csv_f = open(args.output,'w',newline='')
csv_writer = csv.writer(csv_f)

text_args = args.text
text_args = text_args.split(',')

column = ['파일명']

column_temp = []
for index,cl in enumerate(text_args):
    column_temp.append(cl+'_eng')
    column_temp.append(cl+'_kor')
column_temp = sorted(column_temp)
column = column + column_temp
# column = [c[1:] for c in column]
csv_writer.writerow(column)
print(column)
error_file = open('none_error.txt','w')
# csv_writer.writerow(['법령명 eng','법령명 kor','article_title_eng','article_title_kor','article_eng','article_kor'])
for file in files:
    if file.endswith('html'):
        res = None
        with open(file,encoding='utf-8') as html:

            soup = BeautifulSoup(html.read(),'html.parser')
            title_eng = soup.select_one('body > div > table > tbody > tr:nth-of-type(1) > td:nth-of-type(1)')
            title_kor = soup.select_one('body > div > table > tbody > tr:nth-of-type(1) > td:nth-of-type(2)')
            print(file)
            res = title_eng
            
            if res != None:
                title_eng_txt = title_eng.text.strip().replace('\r\n','')
                title_kor_txt = title_kor.text.strip().replace('\r\n','')

                # article_title_eng = soup.select('body > div > table > tbody > tr > td:nth-of-type(1) .articletitle')
                # # for title in article_title_eng: 
                # #     print('eng_article_title',title.text.strip().replace('\n',''))
                
                # article_title_kor = soup.select('body > div > table > tbody > tr > td:nth-of-type(2) .articletitle')
                # # for title in article_title_kor: 
                # #     print('kor_article_title',title.text.strip().replace('\n',''))
                
                # article_eng = soup.select('body > div > table > tbody > tr > td:nth-of-type(1) .articletitle + div')
                # # for article in article_eng:
                # #     print('eng_article',article.text.strip().replace('\n',''))

                # article_kor = soup.select('body > div > table > tbody > tr > td:nth-of-type(2) .articletitle + div')
                # # for article in article_kor:
                # #     print('kor_article',article.text.strip().replace('\n',''))

                # for a_title_e,a_title_k,a_e,a_k in zip(article_title_eng,article_title_kor,article_eng,article_kor):
                #     csv_writer.writerow([title_eng_txt,title_kor_txt,a_title_e.text.strip().replace('\r\n',''),a_title_k.text.strip().replace('\r\n',''),a_e.text.strip().replace('\r\n',''),a_k.text.strip().replace('\r\n','')])
                
                

                arti_title_kor = soup.select('body > div > table > tbody > tr > td:nth-of-type(2) > div:nth-of-type(1)')
                arti_title_eng = soup.select('body > div > table > tbody > tr > td:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1)')
                arti_kor = soup.select('body > div > table > tbody > tr > td:nth-of-type(2) > div:nth-of-type(2)')
                arti_eng = soup.select('body > div > table > tbody > tr > td:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(2)')
                
                kor_title = []
                for article in arti_title_kor:
                    # print('addenda',article.text.strip().replace('\n',''))
                    kor_title.append(article.text)
                    # if p.match(article.text):
                    #     print(article.text)
                eng_title = []
                for article in arti_title_eng:
                    # print('addenda',article.text.strip().replace('\n',''))
                    eng_title.append(article.text)
                
                kor_title_temp = kor_title
                # for index,kt in enumerate(kor_title):
                #     if p.match(kt):
                #         kor_title_temp[index] = kor_title_temp[index]+' : '+kor_title_temp[index+1]
                #         del kor_title_temp[index+1]
                #         # print(kor_title_temp[index])
                
                eng_title_temp = eng_title
                # for index,et in enumerate(eng_title):
                #     et = et.strip()
                #     if et.startswith('CHAPTER'):
                #         eng_title_temp[index] = eng_title_temp[index]+' : '+eng_title_temp[index+1]
                #         del eng_title_temp[index+1]
                #         # print(eng_title_temp[index])
                if len(column) == 3 and 'title_eng' in column and 'title_kor' in column:
                    row = [file,title_eng_txt,title_kor_txt]
                    csv_writer.writerow(row)
                    # print('땡')
                    continue
                for e_t,k_t,a_e,a_k in zip(eng_title_temp,kor_title_temp,arti_eng,arti_kor):
                    row = [file]
                    if 'article_eng' in column and 'article_kor' in column:
                        row.append(a_e.text.replace('\n',''))
                        row.append(a_k.text.replace('\n',''))
                    if 'article_title_kor' in column and 'article_title_eng' in column:
                        row.append(e_t)
                        row.append(k_t)
                    if 'title_eng' in column and 'title_kor' in column:
                        row.append(title_eng_txt)
                        row.append(title_kor_txt)
                    # print(row)
                    csv_writer.writerow(row)
                # addenda_eng = soup.select('body > div > table > tbody > tr > td:nth-of-type(2) > div:nth-of-type(2)')
                # for article in addenda_eng:
                    # print('addenda',article.text.strip())
                # article_kor = soup.select('body > div > table > tbody > tr > td:nth-of-type(2) .addenda + div')
        if res == None:
            os.rename(file,file+'.error')
            error_file.write(file+'.error'+'\n')
error_file.close()
csv_f.close()