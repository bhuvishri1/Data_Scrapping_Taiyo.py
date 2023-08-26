import pandas as pd
import numpy as np
import bs4
from bs4 import BeautifulSoup
import requests


url = "https://www.earthdata.nasa.gov/engage/open-data-services-and-software/api"
response = requests.get(url)
a= response.text

soup = BeautifulSoup(a,'html.parser')
text = soup.get_text()

main_content = soup.find("main")
paragraph = main_content.select('p')

for word in paragraph:
    print(word.get_text())


text_data = soup.find_all("div",class_="clearfix text-formatted field field--name-field-text-content field--type-text-long field--label-hidden field__item")
strn =""
for element in text_data:
    strn = strn+element.get_text()
print(strn)

import csv
import re

data_chunks = strn.split("\n")
extracted_data = []
title = None

for entry in data_chunks:
    if entry.endswith("(APIs)"):
        if title:
            extracted_data.append((title,""))
        title = entry
        description = ""
    else:
        description += entry + "\n"

if title:
    extracted_data.append((title, description)) 

for i, (title, description) in enumerate(extracted_data):
    api_sentences = re.findall(r'\b.*?APIs.*?(?=[.!?])', description)
    for sentence in api_sentences:
        title += " " + sentence
        description = description.replace(sentence, "")
    extracted_data[i] = (title, description)  

csv_rows = []
for title, description in extracted_data:
    csv_rows.append([title, description])

file = "Nasa_Earth_data.csv"
with open(file,'w',newline ='',encoding = "utf-8" )as csvfile:
    csv_writer = csv.writer(csvfile)

    csv_writer.writerow(['Title','Description'])
    
    for row in csv_rows:
        csv_writer.writerow(row)

    
print(f"csvfile '{file}' created successfully.")

df =pd.read_csv("Nasa_Earth_data.csv")
df