from cmath import nan
from bs4 import BeautifulSoup
import requests
import pandas as pd
import xlsxwriter

adress = 'C:/Users/arife/Desktop/WhatIsWhat/Question/Usefultrivia/'

with open(adress + 'usefultrivia_url.txt') as f:  #url leri txt dosyasında tutuyoruz. 
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
answer_long = []

for url in urls :
  result = url.split(" ")[0] in category
  if result == True :
    category_id = category.index(url.split(" ")[0]) + 1
    print(category_id)
  url = requests.get(url.split(" ")[1])
  soup = BeautifulSoup(url.content, 'html.parser')

  for text_medium in soup.find_all('h2'):  #Soruların parse edilidği kısım
      
      response = text_medium.get_text()
      response = response.replace(';', ',') #soruların içindeki noktalı virgülleri virgüle çevirdiğimiz kısım
      response = response.replace('\n', '')
      question.append(response)
      type_length.append(type_quest)
      id_length.append(category_id)

  for answer_wrap_short in soup.find_all('a', attrs={'onmousedown': 'ding.play()'}):  #Cevapların parse edilidği kısım
      #print(answer_wrap.get_text())
      response = answer_wrap_short.get_text()
      response = response.replace(';', ',') 
      response = response.replace('\n', '')
      answer_short.append(response)
       

  for answer_wrap_long in soup.find_all('p', attrs={'class': 'blurb'}):  #Cevapların parse edilidği kısım
      #print(answer_wrap.get_text())
      response = answer_wrap_long.get_text()
      response = response.replace(';', ',')  
      answer_long.append(response)   

workbook = xlsxwriter.Workbook(adress + 'Usefultrivia_Question.xlsx')
worksheet = workbook.add_worksheet()

# Tablodaki sütün başlıkları oluşturuldu.

worksheet.write('A1', 'WHAT/SORU')
worksheet.write('B1', 'KISA')
worksheet.write('C1', 'DETAY/UZUN')
worksheet.write('D1', 'TYPE(Q, P, I)')
worksheet.write('E1', 'CATEGORY ID')

row_q = 1
row_a_s = 1
row_a_l = 1
row_t = 1
row_c = 1

for item in question :  #Sorular sütunu dolduruyoruz.
    if ')' in item :
       item = item.split(')')[1] 
    worksheet.write(row_q, 0, item)

    row_q += 1

for item in answer_short :  #kısa cevaplar sütunu
     worksheet.write(row_a_s, 1, item)
  
     row_a_s += 1

for item in answer_long :   #uzun cevaplar sütunu
     worksheet.write(row_a_l, 2, item)

     row_a_l += 1

for item in type_length :  # type sütunu
     worksheet.write(row_t, 3, item)

     row_t += 1

for item in id_length :   # id sütunu
    worksheet.write(row_c, 4, item)
 
    row_c += 1  

workbook.close()

# WHAT/SORU sütunundaki aynı olan hücrelerin bulunduğu satırları tamamen siliyoruz.

data = pd.read_excel(adress + 'Usefultrivia_Question.xlsx')
data.sort_values('WHAT/SORU',ascending=True)
data.drop_duplicates(subset ="WHAT/SORU",keep = 'last', inplace = True)
print(data)

ds = pd.DataFrame(data)
ds.to_excel(adress + 'Usefultrivia_Question.xlsx', sheet_name='Sheet1', index=False)

