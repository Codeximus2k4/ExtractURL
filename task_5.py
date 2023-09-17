import re
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import csv 
from mongo import connect_to_mongo
import openai
import os 
import textwrap
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub
from dateutil.parser import parse
load_dotenv()





llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

openai.Model.list()

q = open("questions-form.txt","r",encoding="utf8")
questions =""
for lines in q:
    questions = questions +lines
q.close()

q = open("questions-form2.txt","r",encoding = "utf8")
questions2 =""
for lines in q:
  questions2 = questions2 +lines
q.close()

q = open("questions-form3.txt","r",encoding="utf8")
questions3 =""
for lines in q:
    questions3 = questions3 +lines
q.close()

q = open("questions-form4.txt","r",encoding="utf8")
questions4 =""
for lines in q:
    questions4 = questions4 +lines
q.close()

q = open("questions-form5.txt","r",encoding="utf8")
questions5 =""
for lines in q:
    questions5 = questions5 +lines
q.close()

q = open("questions-form8.txt","r",encoding="utf8")
questions8 =""
for lines in q:
    questions8 = questions8 +lines
q.close()

q =open("assistant.txt","r",encoding = "utf8")
prompt = ""
for lines in q:
   prompt = prompt +lines
q.close()


    

# Start mapping from the top-level tag

rows= []
f =open("url_cucus.txt","r",encoding="utf8")
for lines in f:
   url = lines
   if len(url)<5:
       continue
   headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0"}
   r =requests.get(url, verify=False)
   html = r.text
   soup = BeautifulSoup(html, "html.parser")
   #print(soup.prettify())
   for element in soup(
            ["header", "footer", "nav", "script", "style", "button"]
        ):
            element.extract()
   tag_map={} 
   for each in soup.find_all('li'):
       my_dict = each.attrs
       if len(my_dict)==0 :
           if each.a is None:
               continue
           if each.a.has_attr('href'):
               print(each.a['href'])
   for a_tag in soup.find_all('a'):
       if a_tag.has_attr('href'):
           if a_tag.parent is None:
               continue
           else:
               tag= a_tag.parent
               code=''
               name  = tag.name
               code = code+name
               a_dict = tag.attrs
               for each in list(a_dict.keys()):
                   code= code + ' ' + each 
                   for one in a_dict[each]:
                       code= code + ' ' + one
               if code not in list(tag_map.keys()):
                   tag_map[code]=1
               else :
                   key_num = tag_map[code]+1
                   tag_map[code]=key_num                         
   #print(tag_map)
   max = 0
   my_list = list(tag_map.keys())
   for tags in my_list:
       if tags == my_list[0] or tags == my_list[-1]:
           continue
       if tag_map[tags]>max:
           max=tag_map[tags]
           max_tag = tags
   count=0 
   for tags in my_list:
       if tag_map[tags]== max:
           count= count+1
   if count==1:
       key_tag = max_tag
   else:
       for tags in my_list:
           if tags == my_list[0] or tags ==my_list[-1]:
               continue
           maxspace=0
           if tag_map[tags]==max:
               temp_list = tags.split()
               print
               if len(temp_list)>maxspace:
                   maxspace=len(temp_list)
                   key_tag = tags
   print(key_tag) 

            
             
   """
   for tags in list(tag_map.keys()):
    estimate =5
    if tag_map[tags]<= estimate:
        continue
    print(tags)
    
    tags = soup.find_all(tags)
    containers=[]
    div_with_content=[]
    for tag in tags:
        if len(tag.attrs)==0:
            continue
        else:
            mydict = tag.attrs
            attrs = list(mydict.keys())
            for attr in attrs:
                for each in tag[attr]:
                    if "main" in each.lower() or "content" in each.lower():
                        div_with_content.append(div)
                        continue
                    if "body" in each.lower() or "section" in each.lower():
                        div_with_content.append(div)
                        continue
                    if "article" in each.lower():
                        div_with_content.append(div)
                        continue
    urls=[] 
    for div in div_with_content:
        alist = div.find_all('a')
        for each in alist:
            if each.has_attr('href'):
                    new_url= each['href']
                    if new_url in urls:
                        continue
                    else:
                        urls.append(new_url)           
    for each in urls:
        if lines in each:
            continue
        print(each)                       
         """  
    
           
"""
   #soup = BeautifulSoup(r.content,"html5lib")
   print(soup.prettify())
   text = soup.text 
   print(text)
   #with open("scholarship.txt","w") as f:
   #    f.write(text)
   #f.close()

   #loader = TextLoader('scholarship.txt')
   #documents= loader.load()  
   #text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
   #docs = text_splitter.split_documents(documents) 
   #embeddings  = HuggingFaceEmbeddings()
   #db =  FAISS.from_documents(docs,embeddings)
   #chain = load_qa_chain(llm, chain_type = "stuff")
   

   completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    temperature = 0.5,
    max_tokens = 30,
    messages = [
    {"role": "system", "content": f"Bạn là một bot đang hỗ trợ các lập trình viên để trích xuất thông tin từ một trang web, đây là dữ liệu raw text được crawl về : {text} "},
    {"role": "user", "content": f"\n{questions}"},  
  ]
)
   answers =[]
   response = completion.choices[0].message
   answers= answers+ response["content"].split("\n")
   print(answers)
   if "không" in answers[0].lower():
       continue
   if "có" in answers[1].lower():
       completion = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        temperature = 0.5,
        max_tokens = 200,
        messages = [
        {"role": "system", "content": f"Bạn là một bot đang hỗ trợ các lập trình viên để trích xuất thông tin từ một trang web, đây là dữ liệu raw text được crawl về : {text} "},
        {"role": "user", "content": f"\n{questions8}"},  
    ]
    )
       response = response = completion.choices[0].message
       print(response['content'])
       continue

    

   row =[]
   #row =row + response["content"].split("\n")  

   completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    temperature = 0.5,
    max_tokens = 200,
    messages = [
    {"role": "system", "content": f"Bạn là một bot đang hỗ trợ các lập trình viên để trích xuất thông tin từ một trang web, đây là dữ liệu raw text được crawl về : {text} "},
    {"role": "user", "content": f"(Chỉ đưa ra thông tin được hỏi, không giải thích gì thêm, mỗi câu trả lời viết trên một dòng) : \n{questions2}"},
  ]
) 
   response = completion.choices[0].message
   print(response['content'])
   row =row +response["content"].split("\n")


   completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    temperature = 0.5,
    max_tokens = 750,
    messages = [
    {"role": "system", "content": f"Bạn là một bot đang hỗ trợ các lập trình viên để trích xuất thông tin từ một trang web, đây là dữ liệu raw text được crawl về : {text} "},
    {"role": "user", "content": f"(Chỉ đưa ra thông tin được hỏi,không giải thích gì thêm, mỗi câu trả lời viết trên một dòng) : \n{questions3}"},
      
  ]
)
   response = completion.choices[0].message
   print(response['content'])
   row =row +response["content"].split("\n")

   completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    temperature = 0.5,
    max_tokens = 200,
    messages = [
    {"role": "system", "content": f"Bạn là một bot đang hỗ trợ các lập trình viên để trích xuất thông tin từ một trang web, đây là dữ liệu raw text được crawl về : {text} "},
    {"role": "user", "content": f"(Chỉ đưa ra thông tin được hỏi, không giải thích gì thêm, mỗi câu trả lời viết trên một dòng) : \n{questions4}"},
  ]
) 
   response = completion.choices[0].message
   print(response['content'])
   row =row +response["content"].split("\n")
   
   
   completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    temperature = 0.3,
    max_tokens = 700,
    messages = [
    {"role": "system", "content": f"Bạn là một bot đang hỗ trợ các lập trình viên để trích xuất thông tin từ một trang web, đây là dữ liệu raw text được crawl về : {text} "},
    {"role": "user", "content": f"(Chỉ đưa ra thông tin được hỏi, không giải thích gì thêm, mỗi câu trả lời viết trên một dòng) : \n{questions5}"},
  ]
) 
   response = completion.choices[0].message
   print(response['content'])
   row =row +response["content"].split("\n")
 
   #query = "GPA/CPA requirement (if no information then answer 'None') : "
   #gpa_cpa = chain.run(input_documents=docs, question = query)
   #print("GPA:"+ gpa_cpa)

   row.append(soup.prettify())
   row.append(text)
   row.append("URL:"+ url)
   #row.append(gpa_cpa)

   
   


   rows.append(row)
   print(url + "extracted")

#with open(filename,'w',encoding="utf8") as csvfile:
   # csvwriter = csv.writer(csvfile)
   # csvwriter.writerow(fields)
    #csvwriter.writerows(rows) 


fields = ["title","organization","deadline","type","benefits/value","education_level","majors","link","requirements","address","html_file","raw_text","url","GPA/CPA"]
ScholarshipCollection =[]


for row in rows:
    scholar_dict ={}
    count=0
    for each in row:
            if len(each)<=1:
                continue
            info = each.split(':',maxsplit = 1)[1]
            if (count>13) :
                break
            if fields[count]=="type":
                if "hỗ trợ khó khăn" in info.lower():
                    scholar_dict[fields[count]]=1
                elif "đại học" in info.lower() or "du học" in info.lower():
                    scholar_dict[fields[count]]=2
                elif "doanh nghiệp" in info.lower() or "tổ chức" in info.lower():
                    scholar_dict[fields[count]]=3
                else:
                    scholar_dict[fields[count]]=0
            elif fields[count]=="education_level":
                level=""
                if "trung cấp" in  info.lower():
                    level= level + "1,"
                if "cao đẳng" in info.lower():
                    level = level + "2,"
                if  "đại học" in info.lower() :
                    if "sau đại học" not in info.lower():
                        level = level + "3,"
                    else: 
                        x = info.lower().strip("sau đại học")
                        if "đại học" in x:
                            level = level +"3,"
                if "thạc sĩ" in info.lower():
                    level = level + "4,"
                if "tiến sĩ" in info.lower():
                    if "sau tiến sĩ" not in info.lower():
                        level = level+ "5,"
                    else:
                        level = level + "6,"
                        x= info.lower().strip("sau tiến sĩ")
                        if "tiến sĩ" in x:
                            level = level +"5"
                if len(level)==0:
                    level = level +"0"
                scholar_dict[fields[count]]=level
            elif fields[count]=="majors":
                majors =""
                if "kiến trúc" in info.lower() or "xây dựng" in info.lower():
                    majors = majors + "1,"
                if "kinh doanh" in info.lower() or "thương mại" in info.lower():
                    majors = majors + "2,"
                if "công nghệ" in info.lower() or "thông tin" in info.lower():
                    majors = majors +"3,"
                if "luật" in info.lower() or "nhân văn" in info.lower():
                    majors =majors + "4,"
                if "báo chí" in info.lower() or "khoa học xã hội" in info.lower() or "ngôn ngữ" in info.lower():
                    majors = majors + "5,"
                if "y tế" in info.lower():
                    majors = majors + "6,"
                if "khoa học tự nhiên" in info.lower() or "tự nhiên" in info.lower():
                    majors =majors +"7,"
                if "sư phạm" in info.lower():
                    majors = majors + "8,"
                if "kỹ thuật" in info.lower() or "công nghiệp" in info.lower():
                    majors = majors + "9"
                if len(majors)==0:
                    majors = majors + "0"
                scholar_dict[fields[count]]=majors
            elif fields[count]=="address":
                address =""
                if "miền bắc" in info.lower():
                    address = address+"1,"
                if "miền nam" in info.lower():
                    address = address + "2,"
                if "miền trung" in info.lower():
                    address = address + "3,"
                if "châu á" in info.lower():
                    address = address + "4,"
                if "châu âu" in info.lower():
                    address = address+ "5,"
                if "mỹ" in info.lower() or "canada" in info.lower():
                    address = address + "6,"
                if len(address)==0:
                    address = address + "0"
                scholar_dict[fields[count]]=address
            elif fields[count]=="deadline":
                text = info
# Sử dụng biểu thức chính quy để tìm các ngày tháng năm trong chuỗi
                pattern = r'\d{2}/\d{2}/\d{4}'
                dates = re.findall(pattern, text)
                pattern = r'\d{2}/\d{2}'
                if len(dates)==0:
                    dates= dates+ re.findall(pattern,text)
                if len(dates)==0:
                    scholar_dict[fields[count]]=info
                else :
                    temp=""
                    for each in dates:
                        temp = temp+each + ","
                    scholar_dict[fields[count]]=temp 
            elif fields[count]=="GPA/CPA":
                scholar_dict[fields[count]]=each
            else:
                scholar_dict[fields[count]]=info
            count=count+1
    ScholarshipCollection.append(scholar_dict)


def add_scholarship_to_db():
    db = connect_to_mongo()
    scholarship = db["scholarship"]
    for each in ScholarshipCollection:
        result = scholarship.insert_one(each)
"""
