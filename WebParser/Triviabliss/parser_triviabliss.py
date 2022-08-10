from cmath import nan
from bs4 import BeautifulSoup
import requests
import pandas as pd
import xlsxwriter

adress = 'C:/Users/arife/Desktop/WhatIsWhat/Question/Triviabliss/'

with open(adress + 'triviabliss_url.txt') as f:  #url leri txt dosyasında tutuyoruz. 
                                                     #Txt deki her bir satırı listenin bir elemanı olarak atıyoruz.
    urls = [line.strip() for line in f]
    #print(contents)

category = ['General', 'Life', 'Education', 'Health', 'Culture', 'Arts', 'Technology', 'Entertainment', 'Sports', 'Religious',
 'Politics', 'People', 'Science', 'Nature', 'Animal', 'History', 'Travel', 'OMG Facts', 'For Kids', 'Jokes']

category_id = ''
type_quest = 'Q'

id_length = []
type_length = []
question = []
answer_short = []

for url in urls :
  result = url.split(" ")[0] in category
  if result == True :
    category_id = category.index(url.split(" ")[0]) + 1
    print(category_id)
  url = requests.get(url.split(" ")[1])
  soup = BeautifulSoup(url.content, 'html.parser')

  for text_medium in soup.find_all('a', attrs={'class': 'entry-title-link'}):  #Soruların parse edilidği kısım     
      response = text_medium.get_text()
      response = response.replace(';', ',')  #soruların içindeki noktalı virgülleri virgüle çevirdiğimiz kısım
      question.append(response)
      type_length.append(type_quest)
      id_length.append(category_id)

  for answer_wrap_short in soup.find_all('div', attrs={'class': 'entry-content'}):  #Cevapların parse edilidği kısım
      #print(answer_wrap_short.get_text())
      response = answer_wrap_short.get_text()
      response = response.replace(';', ',')
      response = response.replace('\n', '')
      response = response.split('Show Answer')[1] 
      answer_short.append(response)
       

workbook = xlsxwriter.Workbook(adress + 'Triviabliss_Question.xlsx')
worksheet = workbook.add_worksheet()

# Tablodaki sütün başlıkları oluşturuldu.

worksheet.write('A1', 'WHAT/SORU')
worksheet.write('B1', 'KISA')
worksheet.write('C1', 'DETAY/UZUN')
worksheet.write('D1', 'TYPE(Q, P, I)')
worksheet.write('E1', 'CATEGORY ID')

row_q = 1
row_a = 1
row_t = 1
row_c = 1

for item in question :  #Sorular sütunu dolduruyoruz.

     worksheet.write(row_q, 0, item)

     row_q += 1

for item in answer_short :  #kısa cevaplar sütunu
        
     if len(item) <= 100 :
      worksheet.write(row_a, 1, item)
     else :
      worksheet.write(row_a, 2, item)

     row_a += 1  

for item in type_length :  # type sütunu
     worksheet.write(row_t, 3, item)

     row_t += 1

for item in id_length :   # id sütunu
    worksheet.write(row_c, 4, item)
 
    row_c += 1  

workbook.close()

# WHAT/SORU sütunundaki aynı olan hücrelerin bulunduğu satırları tamamen siliyoruz.

data = pd.read_excel(adress + 'Triviabliss_Question.xlsx')
data.sort_values('WHAT/SORU',ascending=True)
data.drop_duplicates(subset ="WHAT/SORU",keep = 'first', inplace = True)
print(data)

ds = pd.DataFrame(data)
ds.to_excel(adress + 'Triviabliss_Question.xlsx', sheet_name='Sheet1', index=False)

