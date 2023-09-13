from typing import Optional
from fastapi import FastAPI
from .db.mongo import connect_to_mongo 
import openai
from bs4 import BeautifulSoup
import requests
def load_questions():
    questions_list =[]
    #loading_questions

    #questions1: verifying whether the url contains scholarship info
    q = open("questions-form.txt","r",encoding="utf8")
    questions =""
    for lines in q:
        questions = questions +lines
    q.close()
    questions_list.append(questions)
    q = open("questions-form2.txt","r",encoding = "utf8")
    #general questions2
    questions2 =""
    for lines in q:
        questions2 = questions2 +lines
    q.close()
    questions_list.append(questions2)
    q = open("questions-form3.txt","r",encoding="utf8")
    questions3 =""
    for lines in q:
        questions3 = questions3 +lines
    q.close()
    questions_list.append(questions3)
    q = open("questions-form4.txt","r",encoding="utf8")
    questions4 =""
    for lines in q:
        questions4 = questions4 +lines
    q.close()
    questions_list.append(questions4)
    q = open("questions-form5.txt","r",encoding="utf8")
    questions5 =""
    for lines in q:
        questions5 = questions5 +lines
    q.close()
    questions_list.append(questions5)
    q = open("questions-form6.txt","r",encoding="utf8")
    return questions_list
def extract_url(url: str):
    # getting the text from url
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0"}
    # avoid 
    r =requests.get(url, verify=False)
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    for element in soup(
            ["header", "footer", "nav", "script", "style", "button"]
        ):
            element.extract()
    return soup 

class ExtractURL():
    title : str
    organization: str
    deadline : Optional[str]
    type: Optional[str]
    benefit: Optional[str]
    edulevel: Optional[str]
    major: Optional[str]
    link: Optional[str]
    requirement: Optional[str]
    def extract_info(url : str):
        mylist = load_questions()
        openai.api_key = "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"
        openai.Model.list()
        soup = extract_url(url)
        text = soup.text
        completion = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            temperature = 0.5,
            max_tokens = 30,
            messages = [
            {"role": "system", "content": f"Bạn là một bot đang hỗ trợ các lập trình viên để trích xuất thông tin từ một trang web, đây là dữ liệu raw text được crawl về : {text} "},
            {"role": "user", "content": f"\n{mylist[0]}"},  
        ]
        )
        response = completion.choices[0].message
        
        if response["content"].lower() == "không":
            return None
        row =[]
        completion = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            temperature = 0.5,
            max_tokens = 200,
            messages = [
            {"role": "system", "content": f"Bạn là một bot đang hỗ trợ các lập trình viên để trích xuất thông tin từ một trang web, đây là dữ liệu raw text được crawl về : {text} "},
            {"role": "user", "content": f"(Chỉ đưa ra thông tin được hỏi, không giải thích gì thêm, mỗi câu trả lời viết trên một dòng) : \n{mylist[1]}"},
        ]
        ) 
        response = completion.choices[0].message
        row =row +response["content"].split("\n")

        completion = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            temperature = 0.5,
            max_tokens = 750,
            messages = [
            {"role": "system", "content": f"Bạn là một bot đang hỗ trợ các lập trình viên để trích xuất thông tin từ một trang web, đây là dữ liệu raw text được crawl về : {text} "},
            {"role": "user", "content": f"(Chỉ đưa ra thông tin được hỏi,không giải thích gì thêm, mỗi câu trả lời viết trên một dòng) : \n{mylist[2]}"},
            
        ]
        )
        response = completion.choices[0].message
        row =row +response["content"].split("\n")

        completion = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            temperature = 0.5,
            max_tokens = 200,
            messages = [
            {"role": "system", "content": f"Bạn là một bot đang hỗ trợ các lập trình viên để trích xuất thông tin từ một trang web, đây là dữ liệu raw text được crawl về : {text} "},
            {"role": "user", "content": f"(Chỉ đưa ra thông tin được hỏi, không giải thích gì thêm, mỗi câu trả lời viết trên một dòng) : \n{mylist[3]}"},
        ]
        ) 
        response = completion.choices[0].message
        row =row +response["content"].split("\n")
        
        completion = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            temperature = 0.5,
            max_tokens = 300,
            messages = [
            {"role": "system", "content": f"Bạn là một bot đang hỗ trợ các lập trình viên để trích xuất thông tin từ một trang web, đây là dữ liệu raw text được crawl về : {text} "},
            {"role": "user", "content": f"(Chỉ đưa ra thông tin được hỏi, không giải thích gì thêm, mỗi câu trả lời viết trên một dòng) : \n{mylist[4]}"},
        ]
        ) 
        response = completion.choices[0].message
        row =row +response["content"].split("\n")
        row.append(soup.prettify())
        row.append(text)
        row.append(url)
        fields = ["title","organization","deadline","type","benefits/value","educationLevel","majors","link","requirements","html_file","raw_text","url"]
        count=0
        scholar_dict ={}
        for each in row:
            if len(each)<=1:
                continue
            info = each.split(':',maxsplit = 1)[1]
            if (count>11) :
                break
            if fields[count]=="type":
                if "hỗ trợ khó khăn" in info.lower():
                    scholar_dict[fields[count]]=1
                elif "đại học" in info.lower() or "du học" in info.lower():
                    scholar_dict[fields[count]]=2
                elif "doanh nghiệp" in info.lower() or "tổ chức" in info.lower():
                    scholar_dict[fields[count]]=3
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
                    level = level +"5"
                scholar_dict[fields[count]]=level
            else:
                scholar_dict[fields[count]]=info
            count=count+1
        return scholar_dict
    
#extract = ExtractURL.extract_info("https://www.hust.edu.vn/vi/su-kien-noi-bat/hop-tac-doi-ngoai-truyen-thong/thong-bao-hoc-bong-erasmus-key-action-1-truong-dh-porto-bo-dao-nha-654608.html")
#print(extract)


app = FastAPI()
@app.get("/scholarship/{full_path:path}")
def extract_and_upload_todb(full_path:str):
    db = connect_to_mongo()
    scholarship = db["scholarship"]
    mydict = ExtractURL.extract_info(full_path)
    result = scholarship.insert_one(mydict)
    return {"taken": full_path}


