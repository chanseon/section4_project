# list JSON 파일을 리스트로 읽기
from pymongo import MongoClient
import json

with open('../data/data_final.json', 'r') as f:
    data = json.load(f)

#리스트여서 딕셔너리로
data_dict ={}
for i in range (len(data)):
    data_dict["data"+str(i)] = data[i]

#연결정보
HOST = 'mydb.ldks5ty.mongodb.net'   
USER = 'pubpcs' 
PASSWORD = '0529'
DATABASE_NAME = 'my_data'   #임의로 설정가능 - DB이름
COLLECTION_NAME = 'youtube_data' #임의로 설정가능 - DB안에 입력될 데이터 이름
MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"
#mongodb+srv://pubpcs:<password>@mydb.ldks5ty.mongodb.net/?retryWrites=true&w=majority

#원격 연결하기 
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]
#collection #연결확인

#데이터 추가
collection.insert_one(data_dict) #데이터가 1개일때
#collection.insert_many(data_dict) #데이터가 다수일때