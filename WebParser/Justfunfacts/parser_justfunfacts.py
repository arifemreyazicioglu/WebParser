from cmath import nan
from attr import attr
from bs4 import BeautifulSoup
import requests
import pandas as pd
import xlsxwriter

adress = 'C:/Users/arife/Desktop/WhatIsWhat/Information/Justfunfacts/'

with open(adress + 'justfunfacts_url.txt') as f:  #url leri txt dosyasında tutuyoruz. 
                                                     #Txt deki her bir satırı listenin bir elemanı olarak atıyoruz.
    urls = [line.strip() for line in f]
    #print(contents)

category = ['General', 'Life', 'Education', 'Health', 'Culture', 'Arts', 'Technology', 'Entertainment', 'Sports', 'Religious',
 'Politics', 'People', 'Science', 'Nature', 'Animal', 'History', 'Travel', 'OMGFacts', 'For Kids', 'Jokes']

category_id = ''
type_quest = 'I'

id_length = []
type_length = []
question = []
answers = []

i = 0
for url in urls :
  result = url.split(" ")[0] in category
  if result == True :
    category_id = category.index(url.split(" ")[0]) + 1
    print(category_id)
  url = requests.get(url.split(" ")[1])
  soup = BeautifulSoup(url.content, 'html.parser')

  for text_medium in soup.find_all('h1',attrs = {'class': 'title single-title entry-title'}):  #Soruların parse edilidği kısım
      i +=1
      response = text_medium.get_text()
      response = response.replace(';', ',')  #soruların içindeki noktalı virgülleri virgüle çevirdiğimiz kısım
      question.append(response)
      type_length.append(type_quest)
      id_length.append(category_id)

  for answer in soup.find_all('div',attrs = {'class': 'thecontent clearfix'}):
       response = answer.get_text()    
       response = response.replace(';', ',')
       response = response.replace('\n','')
       answers.append(response)    

workbook = xlsxwriter.Workbook(adress + 'Justfunfacts_Information.xlsx')
worksheet = workbook.add_worksheet()

# Tablodaki sütün başlıkları oluşturuldu.

worksheet.write('A1', 'WHAT/SORU')
worksheet.write('B1', 'DETAY/UZUN')
worksheet.write('C1', 'TYPE(Q, P, I)')
worksheet.write('D1', 'CATEGORY ID')

row_q = 1
row_a = 1
row_t = 1
row_c = 1

for item in question :  #Sorular sütunu dolduruyoruz.

     worksheet.write(row_q, 0, item)

     row_q += 1

for item in answers :  # type sütunu
     worksheet.write(row_a, 1, item)

     row_a +=1

for item in type_length :  # type sütunu
     worksheet.write(row_t, 2, item)

     row_t += 1

for item in id_length :   # id sütunu
    worksheet.write(row_c, 3, item)
 
    row_c += 1  

workbook.close()

# WHAT/SORU sütunundaki aynı olan hücrelerin bulunduğu satırları tamamen siliyoruz.

data = pd.read_excel(adress + 'Justfunfacts_Information.xlsx')
data.sort_values('WHAT/SORU',ascending=True)
data.drop_duplicates(subset ="WHAT/SORU",keep = 'last', inplace = True)
print(data)

ds = pd.DataFrame(data)
ds.to_excel(adress + 'Justfunfacts_Information.xlsx', sheet_name='Sheet1', index=False)

